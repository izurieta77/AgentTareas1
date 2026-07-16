import os
import sys
import json
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para consola Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

# Cargar variables de entorno antes de importar componentes del app
load_dotenv(dotenv_path=ROOT / ".env")

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
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import llm_factory
from ragas.embeddings.google_provider import GoogleEmbeddings

from app.api.dependencies import initialize_pipeline

def run_evaluation(output_csv: str = "playground/evaluation_results.csv"):
    print("======================================================================")
    print("INICIANDO EVALUACIÓN AUTOMATIZADA CON RAGAS Y GOOGLE GEMINI")
    print("======================================================================\n")
    
    # 1. Cargar Golden Dataset
    dataset_path = ROOT / "data" / "golden_dataset.json"
    if not dataset_path.exists():
        print(f"Error: No se encontró el dataset en {dataset_path}")
        sys.exit(1)
        
    with open(dataset_path, "r", encoding="utf-8") as f:
        golden_data = json.load(f)
        
    print(f"Cargado Golden Dataset con {len(golden_data)} preguntas de referencia.\n")
    
    # 2. Inicializar Pipeline RAG en memoria
    print("Inicializando componentes del pipeline RAG y conexiones...")
    pipeline, rag, cache = initialize_pipeline()
    print("Pipeline RAG listo.\n")
    
    # 3. Recopilar predicciones del RAG
    questions = []
    answers = []
    contexts_list = []
    ground_truths = []
    
    print("Ejecutando consultas del dataset contra el RAG Pipeline...")
    for idx, item in enumerate(golden_data, start=1):
        q = item["question"]
        gt = item["ground_truth"]
        
        print(f"[{idx}/{len(golden_data)}] Procesando: '{q[:50]}...'")
        
        # Desactivamos filtros para evaluar de forma general
        start_time = time.perf_counter()
        result = rag.query(q)
        duration = time.perf_counter() - start_time
        
        ans = result["answer"]
        ctxs = result["pipeline_trace"].get("contexts", [])
        
        print(f"    -> Respuesta generada en {duration:.2f}s. Contextos recuperados: {len(ctxs)}")
        
        questions.append(q)
        answers.append(ans)
        contexts_list.append(ctxs)
        ground_truths.append(gt)
        
    print("\nRespuestas recopiladas con éxito.")
    
    # 4. Formatear para RAGAS
    data_dict = {
        "question": questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data_dict)
    
    # 5. Inicializar Evaluadores de Google GenAI
    print("\nInicializando Juez Evaluador y Embeddings de Google Gemini...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY no configurada en el entorno.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    # RAGAS llm_factory detecta el proveedor "google"
    evaluator_llm = llm_factory(
        model="gemini-3.5-flash",
        provider="google",
        client=client
    )
    
    # GoogleEmbeddings de RAGAS para gemini-embedding-2
    evaluator_embeddings = GoogleEmbeddings(
        client=client,
        model="gemini-embedding-2"
    )
    # Hack to resolve AttributeError: 'GoogleEmbeddings' object has no attribute 'embed_query'
    evaluator_embeddings.embed_query = evaluator_embeddings.embed_text
    evaluator_embeddings.embed_documents = evaluator_embeddings.embed_texts
    print("Evaluadores listos.\n")
    
    # 6. Lanzar Evaluación de RAGAS
    print("Ejecutando cálculo de métricas en RAGAS (este paso realiza llamadas al LLM Juez)...")
    try:
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
        
        # 7. Convertir a DataFrame y obtener promedios
        df_results = results.to_pandas()
        
        def format_score(val):
            if val is None or pd.isna(val):
                return "N/A"
            if isinstance(val, (int, float)):
                return f"{val:.4f}"
            return str(val)

        mean_faithfulness = df_results['faithfulness'].mean() if 'faithfulness' in df_results else None
        mean_answer_relevancy = df_results['answer_relevancy'].mean() if 'answer_relevancy' in df_results else None
        mean_context_precision = df_results['context_precision'].mean() if 'context_precision' in df_results else None
        mean_context_recall = df_results['context_recall'].mean() if 'context_recall' in df_results else None

        print("\n======================================================================")
        print("RESULTADOS OBTENIDOS POR RAGAS")
        print("======================================================================")
        print(f"1. Fidelidad (Faithfulness - Cero Alucinación): {format_score(mean_faithfulness)}")
        print(f"2. Relevancia de Respuesta (Answer Relevancy):   {format_score(mean_answer_relevancy)}")
        print(f"3. Precisión del Contexto (Context Precision):    {format_score(mean_context_precision)}")
        print(f"4. Cobertura del Contexto (Context Recall):       {format_score(mean_context_recall)}")
        print("======================================================================\n")
        
        # 8. Exportar resultados detallados a CSV
        csv_path = ROOT / output_csv
        df_results.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"Resultados detallados exportados con éxito a: {csv_path}\n")
        
        # 9. Gatekeeping de Calidad (Seguridad Industrial)
        CRITICAL_HAL_THRESHOLD = 0.95
        
        # Castear de forma segura para la comparación
        try:
            faithfulness_score = float(mean_faithfulness) if mean_faithfulness is not None else 0.0
        except Exception:
            faithfulness_score = 0.0
        
        if faithfulness_score < CRITICAL_HAL_THRESHOLD:
            print(f"[CRITICAL WARNING] FALLO DE VALIDACIÓN: La fidelidad de las respuestas ({format_score(mean_faithfulness)}) está por debajo del límite de seguridad ({CRITICAL_HAL_THRESHOLD:.2f}).")
            print("El despliegue automático ha sido abortado debido al riesgo de alucinaciones en planta.")
            sys.exit(1)
        else:
            print(f"[SUCCESS] VALIDACIÓN COMPLETADA: El pipeline cumple con los estándares de seguridad industrial (Fidelidad >= {CRITICAL_HAL_THRESHOLD:.2f}).")
            sys.exit(0)
            
    except Exception as e:
        print(f"\nError durante la ejecución del proceso de RAGAS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_evaluation()
