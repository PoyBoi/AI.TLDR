# AI.TLDR - Skills Showcase

##  I WROTE EVERYTHING - NO AI WAS USED IN THE "CODING" OF THIS PROJECT

> **A proof of skills repository** — demonstrating the full breadth of my current AI/ML engineering capabilities through a single, cohesive, production-grade system.

Every module here is intentionally chosen to showcase a distinct skill: from RAG pipelines and multi-agent orchestration to spatial data analysis, MLOps, and reliability engineering - everything is wired together into a local-first agentic AI.

---

## 🧠 Core Intelligence

- **Chain-of-Thought (CoT) Reasoning** — agent thinks before acting
- **Local LLM Backend** — inference runs on-device; fast and private
- **Multi-Agent Architecture** — coordinated agents via shared agentic infrastructure
- **Smart Skill Selection** — dynamic routing to the right tool or sub-agent
- **Prompt Templates** — structured, reusable prompt management

---

## 🔍 Knowledge & Retrieval

- **RAG (Retrieval-Augmented Generation)** — grounded responses from local/indexed documents
- **Web Search** — live search integration for real-time information
- **Optimised Chunking** — context-aware document splitting for better retrieval
- **Re-Ranking** — post-retrieval scoring to surface the most relevant results

---

## 🔗 Orchestration Frameworks

- **LangChain Pipelines** — composable chains for retrieval, transformation, and generation
- **LangGraph** — stateful, graph-based multi-agent workflows with conditional routing
- **LlamaIndex** *(optional)* — alternative/complementary indexing and query engine layer

---

## 📈 Data Analysis & Visualisation

- **Data Quality Analysis** — profiling datasets: distributions, nulls, outliers, schema drift
- **Spatial Mapping** — geographic/relational mapping of data points; visualising how data clusters and connects across dimensions
- **Pipeline Analytics** — tracking retrieval performance, chunk quality, and embedding drift over time

---

## 🛠️ Tools & Actions

- **Tool Calls + Skills** — extensible action layer the agent can invoke
- **MCP (Model Context Protocol)** — standardised tool/context interface
- **REST API + Endpoint Exposure** — interact with the agent programmatically
- **Swagger UI + Documentation** — auto-generated API docs

---

## 🗃️ Storage & Data

- **PostgreSQL** (preferred) or **Apache Spark** — caching and persistent state
- **Parquet Files** — columnar storage over CSV for efficiency at scale
- **Long History Management** — compressed/summarised context across sessions
- **Ideas Store** — local folder/file (`/ideas`) for capturing and retrieving thoughts; optional push to Notion or messaging app

---

## 🔒 Security & Safety

- **Input Validation** — sanitise and verify all inputs before processing
- **Output Filtering** — block unsafe or unintended outputs
- **Guardrails** — rule-based and model-level safety boundaries
- **Permission Boundaries** — scoped access per agent/tool
- **Containerisation & Sandboxing** — isolated execution environments via Docker

---

## 📦 Infrastructure

- **Docker** — fully compartmentalised services per module
- **Retry Logic & Timeouts** — resilient execution under failure
- **MLOps** — model versioning, deployment pipelines, lifecycle management

---

## 📊 Observability & Evaluation

- **Tracing & Tracking** — full request/action tracing (e.g. LangSmith, OpenTelemetry)
- **Evaluation Framework** — automated evals for response quality and agent behaviour
- **Lean Inference** — optimised for speed; minimal overhead on local hardware

---

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
