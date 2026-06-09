## 🗺️ Architecture Overview

```
User / API
    │
    ▼
REST API Layer (FastAPI + SwaggerUI)
    │
    ▼
Orchestrator Agent (CoT + Skill Router)
    │   [LangGraph stateful graph]
    ├── Sub-Agents (Multi-Agent Infra)
    ├── RAG Pipeline (Chunking → Embed → Rerank → Generate)
    │       └── LangChain / LlamaIndex (optional)
    ├── Web Search Tool
    ├── Tool Calls / MCP Skills
    ├── Data Analysis & Spatial Mapping
    └── Ideas Manager (Local File + Notion/App Push)
    │
    ▼
Local LLM (inference backend)
    │
    ▼
Storage Layer (Postgres / Parquet + History Store)
    │
    ▼
Observability (Tracing, Evals, MLOps)
```

---