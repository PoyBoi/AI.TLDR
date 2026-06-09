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