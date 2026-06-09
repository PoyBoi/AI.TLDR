
## 📋 Feature Checklist

### Foundation
- [ ] Local LLM backend wired up
- [ ] CoT prompting implemented
- [ ] Docker Compose multi-service setup

### Retrieval
- [ ] RAG pipeline (ingest → chunk → embed → retrieve)
- [ ] Optimised chunking strategy
- [ ] Re-ranking layer

### Tools & Actions
- [ ] Web search integration
- [ ] Tool call framework
- [ ] MCP server setup
- [ ] Smart skill selection/routing

### Orchestration Frameworks
- [ ] LangChain pipeline(s)
- [ ] LangGraph stateful workflow
- [ ] LlamaIndex integration (optional)

### Multi-Agent
- [ ] Agent orchestrator
- [ ] Sub-agent definitions
- [ ] Shared agentic infra / message bus

### Data Analysis & Visualisation
- [ ] Dataset profiling (distributions, nulls, outliers)
- [ ] Spatial mapping of data
- [ ] Pipeline/retrieval analytics dashboard

### Storage
- [ ] Postgres/Parquet setup
- [ ] Caching layer
- [ ] Long context / history management
- [ ] Ideas store + notification hook

### API & Docs
- [ ] FastAPI REST layer
- [ ] Swagger UI docs

### Safety & Ops
- [ ] Input validation + output filtering
- [ ] Guardrails + permission boundaries
- [ ] Retry logic + timeouts
- [ ] Tracing (OpenTelemetry or LangSmith)
- [ ] Eval harness
- [ ] MLOps pipeline