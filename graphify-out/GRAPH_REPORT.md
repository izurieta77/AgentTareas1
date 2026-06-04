# Graph Report - .  (2026-06-04)

## Corpus Check
- 172 files · ~272,118 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1686 nodes · 4080 edges · 89 communities (74 shown, 15 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_logger.ts|logger.ts]]
- [[_COMMUNITY_code-graph.ts|code-graph.ts]]
- [[_COMMUNITY_symbol-graph-store.ts|symbol-graph-store.ts]]
- [[_COMMUNITY_dagre.min.js|dagre.min.js]]
- [[_COMMUNITY_cytoscape.min.js|cytoscape.min.js]]
- [[_COMMUNITY_forEach()|forEach()]]
- [[_COMMUNITY_watcher.ts|watcher.ts]]
- [[_COMMUNITY_types.ts|types.ts]]
- [[_COMMUNITY_baseClone()|baseClone()]]
- [[_COMMUNITY_constants.ts|constants.ts]]
- [[_COMMUNITY_qdrant.ts|qdrant.ts]]
- [[_COMMUNITY_indexer.test.ts|indexer.test.ts]]
- [[_COMMUNITY_log()|log()]]
- [[_COMMUNITY_baseIteratee()|baseIteratee()]]
- [[_COMMUNITY_context-artifacts.ts|context-artifacts.ts]]
- [[_COMMUNITY_Symbol-level Call Graph (Impact Analysis|Symbol-level Call Graph (Impact Analysis]]
- [[_COMMUNITY_networkSimplex()|networkSimplex()]]
- [[_COMMUNITY_indexer.ts|indexer.ts]]
- [[_COMMUNITY_dependencies|dependencies]]
- [[_COMMUNITY_plugin.json|plugin.json]]
- [[_COMMUNITY_biome.json|biome.json]]
- [[_COMMUNITY_isUndefined()|isUndefined()]]
- [[_COMMUNITY_viewer-app.js|viewer-app.js]]
- [[_COMMUNITY_isObjectLike()|isObjectLike()]]
- [[_COMMUNITY_query-tools.ts|query-tools.ts]]
- [[_COMMUNITY_compilerOptions|compilerOptions]]
- [[_COMMUNITY_Developer Guide|Developer Guide]]
- [[_COMMUNITY_package.json|package.json]]
- [[_COMMUNITY_biome.json|biome.json]]
- [[_COMMUNITY_package.json|package.json]]
- [[_COMMUNITY_compilerOptions|compilerOptions]]
- [[_COMMUNITY_remove-tools.test.ts|remove-tools.test.ts]]
- [[_COMMUNITY_positionX()|positionX()]]
- [[_COMMUNITY_.release-it.json|.release-it.json]]
- [[_COMMUNITY_scripts|scripts]]
- [[_COMMUNITY_projectIdFromPath()|projectIdFromPath()]]
- [[_COMMUNITY_Semantic (LLM) Extraction|Semantic (LLM) Extraction]]
- [[_COMMUNITY_graphify Skill|graphify Skill]]
- [[_COMMUNITY_Management Tools Full Reference|Management Tools Full Reference]]
- [[_COMMUNITY_Incremental Update Mode|Incremental Update Mode]]
- [[_COMMUNITY_graphify query Command|graphify query Command]]
- [[_COMMUNITY_plugin.json|plugin.json]]
- [[_COMMUNITY_plugin.json|plugin.json]]
- [[_COMMUNITY_properties|properties]]
- [[_COMMUNITY_Interactive Graph Viewer (webview)|Interactive Graph Viewer (webview)]]
- [[_COMMUNITY_contributes|contributes]]
- [[_COMMUNITY_Codebase Exploration Skill|Codebase Exploration Skill]]
- [[_COMMUNITY_run()|run()]]
- [[_COMMUNITY_isSymbol()|isSymbol()]]
- [[_COMMUNITY_scripts|scripts]]
- [[_COMMUNITY_SocratiCode MCP Server|SocratiCode MCP Server]]
- [[_COMMUNITY_devDependencies|devDependencies]]
- [[_COMMUNITY_devDependencies|devDependencies]]
- [[_COMMUNITY_server.json|server.json]]
- [[_COMMUNITY_marketplace.json|marketplace.json]]
- [[_COMMUNITY_marketplace.json|marketplace.json]]
- [[_COMMUNITY_gemini-extension.json|gemini-extension.json]]
- [[_COMMUNITY_socraticode.env|socraticode.env]]
- [[_COMMUNITY_socraticode.args|socraticode.args]]
- [[_COMMUNITY_@release-itconventional-changelog|@release-it/conventional-changelog]]
- [[_COMMUNITY_Codebase Context Engine|Codebase Context Engine]]
- [[_COMMUNITY_context-tools.test.ts|context-tools.test.ts]]
- [[_COMMUNITY_qdrant-error-wrapping.test.ts|qdrant-error-wrapping.test.ts]]
- [[_COMMUNITY_repository|repository]]
- [[_COMMUNITY_author|author]]
- [[_COMMUNITY_copy-assets.mjs|copy-assets.mjs]]
- [[_COMMUNITY_manifest.test.ts|manifest.test.ts]]
- [[_COMMUNITY_hooks|hooks]]
- [[_COMMUNITY_esbuild.config.mjs|esbuild.config.mjs]]
- [[_COMMUNITY_engines|engines]]
- [[_COMMUNITY_galleryBanner|galleryBanner]]
- [[_COMMUNITY_glama.json|glama.json]]
- [[_COMMUNITY_hooks|hooks]]
- [[_COMMUNITY_SocratiCode Extension Icon|SocratiCode Extension Icon]]
- [[_COMMUNITY_socraticode|socraticode]]
- [[_COMMUNITY_install-graphify.sh script|install-graphify.sh script]]
- [[_COMMUNITY_Code of Conduct|Code of Conduct]]
- [[_COMMUNITY_Cross-process File Locking (proper-lockf|Cross-process File Locking (proper-lockf]]
- [[_COMMUNITY_bump-plugin-versions.mjs|bump-plugin-versions.mjs]]
- [[_COMMUNITY_viewer-app.test.ts|viewer-app.test.ts]]
- [[_COMMUNITY_GraphML Export|GraphML Export]]
- [[_COMMUNITY_SVG Export|SVG Export]]
- [[_COMMUNITY_Wiki Export|Wiki Export]]
- [[_COMMUNITY_Branch-aware Indexing|Branch-aware Indexing]]
- [[_COMMUNITY_codebase_symbol tool|codebase_symbol tool]]

## God Nodes (most connected - your core abstractions)
1. `forEach()` - 72 edges
2. `projectIdFromPath()` - 45 edges
3. `getEmbeddingConfig()` - 45 edges
4. `logger` - 33 edges
5. `handleGraphTool()` - 32 edges
6. `getClient()` - 28 edges
7. `runLayout()` - 27 edges
8. `updateProjectIndex()` - 27 edges
9. `handleQueryTool()` - 27 edges
10. `has()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Cross-Repo Graph Merge` --semantically_similar_to--> `Cross-project Search (linked projects)`  [INFERRED] [semantically similar]
  .claude/skills/graphify/references/github-and-merge.md → README.md
- `graphify Skill` --semantically_similar_to--> `Codebase Exploration Skill`  [INFERRED] [semantically similar]
  .claude/skills/graphify/SKILL.md → skills/codebase-exploration/SKILL.md
- `graphify Skill` --semantically_similar_to--> `Codebase Context Engine`  [INFERRED] [semantically similar]
  .claude/skills/graphify/SKILL.md → README.md
- `Knowledge Graph` --semantically_similar_to--> `Polyglot Code Dependency Graph`  [INFERRED] [semantically similar]
  .claude/skills/graphify/SKILL.md → README.md
- `God Nodes` --semantically_similar_to--> `Symbol-level Impact Analysis (blast radius)`  [INFERRED] [semantically similar]
  .claude/skills/graphify/SKILL.md → README.md

## Import Cycles
- None detected.

## Communities (89 total, 15 thin omitted)

### Community 0 - "logger.ts"
Cohesion: 0.05
Nodes (55): InfraProgressCallback, EmbeddingConfig, EmbeddingProvider, getEmbeddingConfig(), guessContextLength(), loadEmbeddingConfig(), MODE_DEFAULTS, MODEL_CONTEXT_LENGTHS (+47 more)

### Community 1 - "code-graph.ts"
Cohesion: 0.05
Nodes (76): _dockerAvailable, AstGrepLangModule, awaitGraphBuild(), buildCodeGraph(), DynamicLanguageStatus, ensureDynamicLanguages(), esmRequire, failedDynamicLanguages (+68 more)

### Community 2 - "symbol-graph-store.ts"
Cohesion: 0.06
Nodes (64): getAstGrepLang(), persistSymbolGraph(), AssetCache, ASSETS_DIR, buildInteractiveGraphHtml(), __dirname, escapeHtml(), InteractiveHtmlOptions (+56 more)

### Community 3 - "dagre.min.js"
Cohesion: 0.03
Nodes (42): apply(), arrayIncludes(), arrayPush(), assocIndexOf(), baseFindIndex(), baseFlatten(), baseGetAllKeys(), baseIndexOf() (+34 more)

### Community 4 - "cytoscape.min.js"
Cohesion: 0.05
Nodes (61): a(), Ao(), b(), Ba(), bc(), bl(), cs(), d() (+53 more)

### Community 5 - "forEach()"
Cohesion: 0.05
Nodes (68): addBorderSegments(), addSubgraphConstraints(), adjust(), asNonCompoundGraph(), assignBucket(), assignNodeIntersects(), assignRankMinMax(), barycenter() (+60 more)

### Community 6 - "watcher.ts"
Cohesion: 0.09
Nodes (54): getIndexingInProgressProjects(), getIndexingProgress(), getPersistedIndexingStatus(), getProjectHashes(), indexProject(), isCancellationRequested(), removeProjectIndex(), requestCancellation() (+46 more)

### Community 7 - "types.ts"
Cohesion: 0.08
Nodes (47): SocratiCodeConfig, detectEntryPoints(), detectFrameworkReasons(), SymbolContext, computeUnresolvedPct(), resolveCallSites(), extractCalleeNameJs(), ExtractedSymbols (+39 more)

### Community 8 - "baseClone()"
Cohesion: 0.07
Nodes (45): arrayEach(), assignMergeValue(), assignValue(), baseAssign(), baseAssignIn(), baseAssignValue(), baseClone(), baseIsNative() (+37 more)

### Community 9 - "constants.ts"
Cohesion: 0.11
Nodes (37): resetReadinessCache(), dockerAvailable, doesOllamaContainerExist(), doesQdrantContainerExist(), ensureExternalQdrantReady(), ensureOllamaContainerReady(), ensureQdrantReady(), execFileAsync (+29 more)

### Community 10 - "qdrant.ts"
Cohesion: 0.15
Nodes (36): dockerAvailable, generateQueryEmbedding(), deleteArtifactChunks(), deleteCollection(), deleteContextMetadata(), deleteFileChunks(), deleteGraphData(), deleteProjectMetadata() (+28 more)

### Community 11 - "indexer.test.ts"
Cohesion: 0.14
Nodes (24): dockerAvailable, addFileToFixture(), createFixtureProject(), FixtureProject, isDockerAvailable(), removeFixtureFile(), cleanupTestCollections(), createTestQdrantClient() (+16 more)

### Community 12 - "log()"
Cohesion: 0.12
Nodes (23): indexCurrentWorkspaceCommand(), registerCommands(), activate(), GRAPH_DIR, handleWebviewMessage(), loadGraphHtml(), offerToGenerate(), openInteractiveGraph() (+15 more)

### Community 13 - "baseIteratee()"
Cohesion: 0.10
Nodes (33): arrayLikeKeys(), arraySome(), baseGet(), baseIsEqual(), baseIsEqualDeep(), baseIsMatch(), baseIteratee(), baseMatches() (+25 more)

### Community 14 - "context-artifacts.ts"
Cohesion: 0.19
Nodes (22): dockerAvailable, ArtifactChunk, chunkArtifactContent(), ensureArtifactsIndexed(), generateChunkId(), getArtifactStatusSummary(), hashContent(), indexAllArtifacts() (+14 more)

### Community 15 - "Symbol-level Call Graph (Impact Analysis"
Cohesion: 0.12
Nodes (24): Community Detection, Knowledge Graph, Model Context Protocol (MCP), ast-grep, Code Dependency Graph, codebase_flow (MCP tool), codebase_graph_build (MCP tool), codebase_graph_visualize (MCP tool) (+16 more)

### Community 16 - "networkSimplex()"
Cohesion: 0.09
Nodes (27): assignCutValue(), baseExtremum(), calcCutValue(), dfsAssignLowLim(), enterEdge(), exchangeEdges(), feasibleTree(), findMinSlackEdge() (+19 more)

### Community 17 - "indexer.ts"
Cohesion: 0.13
Nodes (24): createIgnoreFilter(), DEFAULT_IGNORE_PATTERNS, findNestedGitignores(), applyCharCap(), AstRegion, cancellationRequested, chunkByAstRegions(), chunkByCharacters() (+16 more)

### Community 18 - "dependencies"
Cohesion: 0.08
Nodes (26): dependencies, @ast-grep/lang-bash, @ast-grep/lang-c, @ast-grep/lang-cpp, @ast-grep/lang-csharp, @ast-grep/lang-go, @ast-grep/lang-java, @ast-grep/lang-kotlin (+18 more)

### Community 19 - "plugin.json"
Cohesion: 0.08
Nodes (24): author, email, name, url, description, homepage, interface, capabilities (+16 more)

### Community 20 - "biome.json"
Cohesion: 0.08
Nodes (23): noBannedTypes, files, ignoreUnknown, formatter, enabled, indentStyle, indentWidth, lineWidth (+15 more)

### Community 21 - "isUndefined()"
Cohesion: 0.11
Nodes (23): assignOrder(), baseZipObject(), buildLayerGraph(), buildLayerGraphs(), buildLayerMatrix(), cloneDeep(), createRootNode(), crossCount() (+15 more)

### Community 22 - "viewer-app.js"
Cohesion: 0.24
Nodes (20): actionBar(), bfsHighlight(), buildSymbolNeighbourhood(), capturePositions(), clearHighlights(), clearSidebar(), clearSymbolSeed(), closeSidebar() (+12 more)

### Community 23 - "isObjectLike()"
Cohesion: 0.11
Nodes (21): baseGetTag(), baseIsArguments(), baseIsMap(), baseIsSet(), baseIsTypedArray(), dijkstra(), dijkstraAll(), getRawTag() (+13 more)

### Community 24 - "query-tools.ts"
Cohesion: 0.13
Nodes (19): waitForIndexingComplete(), getLastCompleted(), isIndexingInProgress(), clearExternalWatchCache(), ensureWatcherStarted(), isWatchedByAnyProcess(), formatProgressLines(), handleQueryTool() (+11 more)

### Community 25 - "compilerOptions"
Cohesion: 0.10
Nodes (20): compilerOptions, declaration, esModuleInterop, forceConsistentCasingInFileNames, lib, module, moduleResolution, noFallthroughCasesInSwitch (+12 more)

### Community 26 - "Developer Guide"
Cohesion: 0.13
Nodes (20): Changelog, Contributor License Agreement, Biome Linter, CodeRabbit Automated Review, Conventional Commits, Dual Licensing (AGPL-3.0 + Commercial), release-it, Semantic Versioning (+12 more)

### Community 27 - "package.json"
Cohesion: 0.10
Nodes (19): bin, socraticode, bugs, url, description, engines, node, files (+11 more)

### Community 28 - "biome.json"
Cohesion: 0.11
Nodes (18): source, assist, actions, files, includes, formatter, enabled, linter (+10 more)

### Community 29 - "package.json"
Cohesion: 0.11
Nodes (17): activationEvents, bugs, url, categories, description, displayName, homepage, icon (+9 more)

### Community 30 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, declaration, declarationMap, esModuleInterop, forceConsistentCasingInFileNames, module, moduleResolution, outDir (+9 more)

### Community 31 - "remove-tools.test.ts"
Cohesion: 0.12
Nodes (15): mockAwaitGraphBuild, mockGetIndexingProgress, mockIndexProject, mockIsGraphBuildInProgress, mockIsIndexingInProgress, mockIsProjectLocked, mockIsWatching, mockRemoveAllArtifacts (+7 more)

### Community 32 - "positionX()"
Cohesion: 0.18
Nodes (15): alignCoordinates(), balance(), baseForOwn(), castFunction(), debugOrdering(), findSmallestWidthAlignment(), findType1Conflicts(), findType2Conflicts() (+7 more)

### Community 33 - ".release-it.json"
Cohesion: 0.13
Nodes (14): release-it, git, commitMessage, push, requireCleanWorkingDir, tagAnnotation, tagName, github (+6 more)

### Community 34 - "scripts"
Cohesion: 0.13
Nodes (15): scripts, build, dev, lint, lint:fix, prepublishOnly, release, release:dry (+7 more)

### Community 35 - "projectIdFromPath()"
Cohesion: 0.30
Nodes (11): assertValidProjectId(), coreProjectId(), detectGitBranch(), effectiveBaseProjectId(), loadLinkedProjects(), loadSocratiCodeConfig(), projectIdFromPath(), readProjectIdFromConfigFile() (+3 more)

### Community 36 - "Semantic (LLM) Extraction"
Cohesion: 0.18
Nodes (14): Watch Debounce, Folder Watch Mode, Confidence Score Rubric, Hyperedge, Node ID Format Rule, Semantic Similarity Edge, Extraction Subagent Prompt, Image Vision Extraction Rules (+6 more)

### Community 37 - "graphify Skill"
Cohesion: 0.16
Nodes (14): graphifyy PyPI Package, SessionStart Install Hook, Token Reduction Benchmark, Honest Audit Trail (EXTRACTED/INFERRED/AMBIGUOUS), Token Cost Tracker, File Detection Step, Honesty Rules, Interactive HTML Visualization (+6 more)

### Community 38 - "Management Tools Full Reference"
Cohesion: 0.20
Nodes (14): Codebase Management Skill, AST-aware Chunking (ast-grep), Context Artifacts, Polyglot Code Dependency Graph, Live File Watcher, Incremental & Resumable Indexing, codebase_graph_build tool, codebase_graph_circular tool (+6 more)

### Community 39 - "Incremental Update Mode"
Cohesion: 0.17
Nodes (13): graphify add URL Command, URL Ingest, Directed Graph Mode, God Nodes, graphify explain Command, graphify path Command, save-result Feedback Loop, Whisper Video/Audio Transcription (+5 more)

### Community 40 - "graphify query Command"
Cohesion: 0.18
Nodes (13): MCP Stdio Server, Neo4j Cypher Export, GitHub Repo Clone, Cross-Repo Graph Merge, Monorepo Subfolder Merge, Clustering and Cohesion Scoring, Fast Path Existing Graph, graph.json (+5 more)

### Community 41 - "plugin.json"
Cohesion: 0.15
Nodes (12): author, email, name, url, description, homepage, keywords, license (+4 more)

### Community 42 - "plugin.json"
Cohesion: 0.15
Nodes (12): author, email, name, description, homepage, keywords, license, mcpServers (+4 more)

### Community 43 - "properties"
Cohesion: 0.15
Nodes (13): properties, title, configuration, socraticode.command, socraticode.statusBar, default, description, scope (+5 more)

### Community 44 - "Interactive Graph Viewer (webview)"
Cohesion: 0.18
Nodes (12): Cytoscape.js + Dagre (vendored), Interactive Graph Viewer HTML Template, Extension CHANGELOG, Interactive Graph Viewer (webview), SocratiCode VS Code Extension README, SocratiCode VS Code / Open VSX Extension, Call-flow Tracing, Symbol-level Impact Analysis (blast radius) (+4 more)

### Community 45 - "contributes"
Cohesion: 0.17
Nodes (12): contributes, commands, mcpServerDefinitionProviders, menus, views, viewsContainers, viewsWelcome, walkthroughs (+4 more)

### Community 46 - "Codebase Exploration Skill"
Cohesion: 0.31
Nodes (11): codebase-explorer agent, Codebase Exploration Skill, Cross-project Search (linked projects), Hybrid Search (semantic + BM25, RRF-fused), Reciprocal Rank Fusion (RRF), Search Before Reading principle, codebase_context_search tool, codebase_graph_query tool (+3 more)

### Community 47 - "run()"
Cohesion: 0.25
Nodes (11): addBorderNode(), addDummyNode(), components(), dfs(), dfsFAS(), doDfs(), injectEdgeLabelProxies(), normalizeEdge() (+3 more)

### Community 48 - "isSymbol()"
Cohesion: 0.20
Nodes (11): arrayMap(), baseMap(), baseOrderBy(), baseSortBy(), baseToString(), baseUnary(), baseValues(), compareAscending() (+3 more)

### Community 49 - "scripts"
Cohesion: 0.18
Nodes (11): scripts, compile, lint, package, publish:all, publish:ovsx, publish:vsce, test (+3 more)

### Community 50 - "SocratiCode MCP Server"
Cohesion: 0.31
Nodes (8): socraticode-ollama service, socraticode-qdrant service, Docker, SocratiCode MCP Server, Ollama (embeddings), Qdrant Vector Database, Local-by-default Security Model, SocratiCode Security Policy

### Community 51 - "devDependencies"
Cohesion: 0.22
Nodes (9): devDependencies, @biomejs/biome, esbuild, ovsx, tsx, @types/node, @types/vscode, typescript (+1 more)

### Community 52 - "devDependencies"
Cohesion: 0.22
Nodes (9): devDependencies, @biomejs/biome, @release-it/conventional-changelog, tsx, @types/node, @types/proper-lockfile, typescript, vitest (+1 more)

### Community 53 - "server.json"
Cohesion: 0.22
Nodes (8): description, name, packages, repository, source, url, $schema, version

### Community 54 - "marketplace.json"
Cohesion: 0.25
Nodes (7): metadata, description, name, owner, email, name, plugins

### Community 55 - "marketplace.json"
Cohesion: 0.25
Nodes (7): metadata, description, name, owner, email, name, plugins

### Community 56 - "gemini-extension.json"
Cohesion: 0.25
Nodes (7): contextFileName, mcpServers, socraticode, name, args, command, version

### Community 57 - "socraticode.env"
Cohesion: 0.29
Nodes (7): type, socraticode.env, additionalProperties, default, description, scope, type

### Community 58 - "socraticode.args"
Cohesion: 0.29
Nodes (7): type, socraticode.args, default, description, items, scope, type

### Community 59 - "@release-it/conventional-changelog"
Cohesion: 0.29
Nodes (7): plugins, @release-it/conventional-changelog, name, types, header, infile, preset

### Community 60 - "Codebase Context Engine"
Cohesion: 0.33
Nodes (6): Altaire Limited, Codebase Context Engine, JanuScope (sibling MCP policy proxy), SocratiCode README, SocratiCode Cloud, SocratiCode Support Doc

### Community 61 - "context-tools.test.ts"
Cohesion: 0.33
Nodes (5): mockEnsureOllamaReady, mockGetEmbeddingConfig, mockGetEmbeddingProvider, mockIndexAllArtifacts, mockSearchArtifacts

### Community 62 - "qdrant-error-wrapping.test.ts"
Cohesion: 0.33
Nodes (5): mockCreateCollection, mockCreatePayloadIndex, mockGetCollection, mockGetCollections, mockRetrieve

### Community 64 - "repository"
Cohesion: 0.50
Nodes (4): repository, directory, type, url

### Community 65 - "author"
Cohesion: 0.50
Nodes (4): author, email, name, url

### Community 66 - "copy-assets.mjs"
Cohesion: 0.50
Nodes (3): dst, root, src

### Community 67 - "manifest.test.ts"
Cohesion: 0.50
Nodes (3): extensionRoot, manifest, manifestPath

### Community 70 - "engines"
Cohesion: 0.67
Nodes (3): engines, node, vscode

### Community 71 - "galleryBanner"
Cohesion: 0.67
Nodes (3): galleryBanner, color, theme

### Community 74 - "SocratiCode Extension Icon"
Cohesion: 1.00
Nodes (3): SocratiCode Extension Icon, SocratiCode Logo, SocratiCode Logo Thumbnail

## Knowledge Gaps
- **473 isolated node(s):** `install-graphify.sh script`, `SessionStart`, `Extraction Cache`, `GRAPH_REPORT.md`, `Obsidian Vault Export` (+468 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `findCircularDependencies()` connect `code-graph.ts` to `symbol-graph-store.ts`, `run()`?**
  _High betweenness centrality (0.193) - this node is a cross-community bridge._
- **Why does `dfs()` connect `run()` to `networkSimplex()`, `code-graph.ts`, `dagre.min.js`, `forEach()`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **Why does `r()` connect `cytoscape.min.js` to `dagre.min.js`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **What connects `install-graphify.sh script`, `SessionStart`, `Extraction Cache` to the rest of the system?**
  _477 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `logger.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.05168316831683168 - nodes in this community are weakly interconnected._
- **Should `code-graph.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.053534660260809885 - nodes in this community are weakly interconnected._
- **Should `symbol-graph-store.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.057387057387057384 - nodes in this community are weakly interconnected._