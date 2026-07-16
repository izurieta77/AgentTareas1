import time
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import (
    QueryRequest, QueryResponse, 
    IngestRequest, IngestResponse, 
    HealthResponse, SourceNode, PipelineTrace,
    SyncDirRequest, SyncDirResponse,
    EvaluationRequest, EvaluationResponse, MetricScores
)
from app.api.dependencies import get_rag_pipeline, get_ingestion_pipeline, get_semantic_cache
from app.retrieval.agentic_pipeline import AgenticRAGPipeline
from app.ingestion.pipeline import IngestionPipeline
from app.retrieval.cache import SemanticCache
from app.ingestion.sync.orchestrator import IncrementalSyncOrchestrator


router = APIRouter()

@router.post(
    "/query", 
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar el motor de RAG Agéntico",
    description="Procesa una pregunta utilizando enrutamiento inteligente, recuperación híbrida y generación con citas estrictas."
)
async def query_rag(
    request: QueryRequest,
    rag: AgenticRAGPipeline = Depends(get_rag_pipeline),
    cache: SemanticCache = Depends(get_semantic_cache)
):
    try:
        # 1. Comprobar caché semántica
        cache_hit = cache.check(request.query)
        if cache_hit is not None:
            cached_result = cache_hit["response"]
            similarity = cache_hit["similarity"]
            
            # Re-mapear las fuentes a la estructura de SourceNode de Pydantic
            sources = [
                SourceNode(
                    id=s["id"],
                    document=s["document"],
                    heading=s.get("heading"),
                    content_snippet=s["content_snippet"],
                    compressed=s["compressed"]
                )
                for s in cached_result.get("sources", [])
            ]
            
            trace = PipelineTrace(
                retrieved_chunks=cached_result["pipeline_trace"]["retrieved_chunks"],
                use_hyde=cached_result["pipeline_trace"]["use_hyde"],
                use_multiquery=cached_result["pipeline_trace"]["use_multiquery"],
                compression_applied=cached_result["pipeline_trace"]["compression_applied"],
                cache_hit=True,
                cache_similarity=similarity
            )
            
            return QueryResponse(
                query=request.query,
                category=cached_result["category"],
                answer=cached_result["answer"],
                sources=sources,
                pipeline_trace=trace
            )
            
        # 2. Cache Miss: Ejecutar consulta a través del orquestador agéntico
        result = rag.query(request.query, filters=request.filters)
        
        # Mapear las fuentes a la estructura de SourceNode de Pydantic
        sources = [
            SourceNode(
                id=s["id"],
                document=s["document"],
                heading=s.get("heading"),
                content_snippet=s["content_snippet"],
                compressed=s["compressed"]
            )
            for s in result.get("sources", [])
        ]
        
        # Mapear la traza de ejecución
        trace = PipelineTrace(
            retrieved_chunks=result["pipeline_trace"]["retrieved_chunks"],
            use_hyde=result["pipeline_trace"]["use_hyde"],
            use_multiquery=result["pipeline_trace"]["use_multiquery"],
            compression_applied=result["pipeline_trace"]["compression_applied"],
            cache_hit=False,
            cache_similarity=None
        )
        
        # 3. Registrar en la caché semántica para futuras consultas
        # (solo respuestas válidas: cachear errores del LLM envenenaría la caché)
        if not result.get("generation_failed"):
            cache.update(request.query, result)
        
        return QueryResponse(
            query=result["query"],
            category=result["category"],
            answer=result["answer"],
            sources=sources,
            pipeline_trace=trace
        )

        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en el RAG Pipeline: {str(e)}"
        )

@router.post(
    "/ingest/sync",
    response_model=IngestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingestar un nuevo documento en caliente",
    description="Procesa, segmenta y vectoriza un archivo local (.pdf, .docx) en la base de datos vectorial de manera síncrona."
)
async def ingest_file(
    request: IngestRequest,
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline)
):
    try:
        # Construir metadatos a partir del request
        base_metadata = {}
        if request.project_id:
            base_metadata["project_id"] = request.project_id
        if request.doc_type:
            base_metadata["doc_type"] = request.doc_type
        if request.confidentiality:
            base_metadata["confidentiality"] = request.confidentiality
            
        # Ejecutar la ingesta
        result = pipeline.process_file(request.file_path, base_metadata=base_metadata)
        
        if result.get("status") != "ok":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fallo en la ingesta del archivo: {result.get('status')}"
            )
            
        return IngestResponse(
            file_path=result["file_path"],
            n_parents=result["n_parents"],
            n_children=result["n_children"],
            duration_seconds=result["duration_seconds"],
            status=result["status"]
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error crítico en el proceso de ingesta: {str(e)}"
        )

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Chequeo de salud del sistema",
    description="Verifica la conectividad de la base de datos Qdrant y la cantidad de vectores indexados."
)
async def health_check(
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline)
):
    qdrant_connected = False
    vector_count = 0
    collection_name = pipeline.vector_store.collection_name
    
    try:
        # Comprobar estado de la colección
        info = pipeline.get_collection_info()
        if info:
            qdrant_connected = True
            vector_count = info.get("points_count", 0)
    except Exception:
        # No levantamos excepción HTTP aquí para que el JSON de respuesta contenga el estado detallado
        pass
        
    return HealthResponse(
        status="ok" if qdrant_connected else "degraded",
        qdrant_connected=qdrant_connected,
        collection_name=collection_name,
        vector_count=vector_count
    )

@router.post(
    "/ingest/sync_dir",
    response_model=SyncDirResponse,
    status_code=status.HTTP_200_OK,
    summary="Sincronizar directorio de forma incremental",
    description="Analiza un directorio completo, detecta cambios mediante ledger SQLite, y actualiza de manera eficiente vector store y doc store."
)
async def sync_directory_endpoint(
    request: SyncDirRequest,
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline)
):
    try:
        base_metadata = {}
        if request.project_id:
            base_metadata["project_id"] = request.project_id
        if request.doc_type:
            base_metadata["doc_type"] = request.doc_type
        if request.confidentiality:
            base_metadata["confidentiality"] = request.confidentiality
            
        orchestrator = IncrementalSyncOrchestrator(pipeline=pipeline)
        report = orchestrator.sync_directory(
            directory_path=request.directory_path,
            base_metadata=base_metadata
        )
        
        return SyncDirResponse(
            directory=report["directory"],
            added_count=len(report["added"]),
            updated_count=len(report["updated"]),
            deleted_count=len(report["deleted"]),
            skipped_count=report["skipped_count"],
            status=report["status"]
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al sincronizar directorio: {str(e)}"
        )

@router.post(
    "/eval/run",
    response_model=EvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Ejecutar evaluación con RAGAS",
    description="Corre el golden dataset de preguntas técnicas contra el pipeline RAG y calcula métricas de fidelidad y cobertura usando Gemini."
)
async def run_evaluation_endpoint(
    request: EvaluationRequest,
    rag: AgenticRAGPipeline = Depends(get_rag_pipeline)
):
    start_time = time.perf_counter()
    try:
        # Importaciones locales diferidas
        import os
        import json
        import pandas as pd
        from pathlib import Path
        import sys
        import types
        try:
            from langchain_google_vertexai import ChatVertexAI
            mod = types.ModuleType("vertexai")
            mod.ChatVertexAI = ChatVertexAI
            sys.modules["langchain_community.chat_models.vertexai"] = mod
        except ImportError:
            pass
        from google import genai
        from datasets import Dataset
        from ragas import evaluate
        from ragas.llms import llm_factory
        from ragas.embeddings.google_provider import GoogleEmbeddings
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

        # 1. Rutas
        ROOT = Path(__file__).parent.parent.parent
        ds_path = ROOT / (request.golden_dataset_path or "data/golden_dataset.json")
        csv_out_path = ROOT / (request.output_csv_path or "playground/evaluation_results.csv")

        if not ds_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el Golden Dataset en la ruta especificada: {ds_path}"
            )

        # 2. Cargar Golden Dataset
        with open(ds_path, "r", encoding="utf-8") as f:
            golden_data = json.load(f)

        # 3. Recopilar respuestas
        questions, answers, contexts_list, ground_truths = [], [], [], []

        for item in golden_data:
            q = item["question"]
            gt = item["ground_truth"]
            
            # Ejecutar consulta en pipeline
            result = rag.query(q)
            
            questions.append(q)
            answers.append(result["answer"])
            contexts_list.append(result["pipeline_trace"].get("contexts", []))
            ground_truths.append(gt)

        # 4. Construir Dataset
        data_dict = {
            "question": questions,
            "answer": answers,
            "contexts": contexts_list,
            "ground_truth": ground_truths
        }
        dataset = Dataset.from_dict(data_dict)

        # 5. Inicializar evaluadores
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Variable GEMINI_API_KEY no configurada en el entorno."
            )

        client = genai.Client(api_key=api_key)
        evaluator_llm = llm_factory(
            model="gemini-3.5-flash",
            provider="google",
            client=client
        )
        evaluator_embeddings = GoogleEmbeddings(
            client=client,
            model="gemini-embedding-2"
        )
        # Hack to resolve AttributeError: 'GoogleEmbeddings' object has no attribute 'embed_query'
        evaluator_embeddings.embed_query = evaluator_embeddings.embed_text
        evaluator_embeddings.embed_documents = evaluator_embeddings.embed_texts

        # 6. Evaluar
        results = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        )

        # 7. Guardar en CSV
        df_results = results.to_pandas()
        df_results.to_csv(csv_out_path, index=False, encoding="utf-8")

        duration = time.perf_counter() - start_time

        def safe_float(val) -> float:
            try:
                if val is None or pd.isna(val):
                    return 0.0
                return float(val)
            except Exception:
                return 0.0

        scores = MetricScores(
            faithfulness=safe_float(df_results["faithfulness"].mean() if "faithfulness" in df_results else 0.0),
            answer_relevancy=safe_float(df_results["answer_relevancy"].mean() if "answer_relevancy" in df_results else 0.0),
            context_precision=safe_float(df_results["context_precision"].mean() if "context_precision" in df_results else 0.0),
            context_recall=safe_float(df_results["context_recall"].mean() if "context_recall" in df_results else 0.0)
        )

        # Gatekeeping check
        CRITICAL_HAL_THRESHOLD = 0.95
        if scores.faithfulness < CRITICAL_HAL_THRESHOLD:
            return EvaluationResponse(
                status="failed",
                message=f"Fallo de validación de calidad: fidelidad ({scores.faithfulness:.4f}) por debajo de {CRITICAL_HAL_THRESHOLD:.2f}",
                scores=scores,
                output_file=str(csv_out_path),
                duration_seconds=duration
            )

        return EvaluationResponse(
            status="success",
            message="Evaluación de RAGAS completada exitosamente. El pipeline cumple los criterios de calidad.",
            scores=scores,
            output_file=str(csv_out_path),
            duration_seconds=duration
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la ejecución de la evaluación de RAGAS: {str(e)}"
        )

