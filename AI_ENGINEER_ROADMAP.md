# 🚀 THE DEFINITIVE AI ENGINEER ROADMAP — Merged & Final

> **Identity:** "A Full-Stack Developer who builds production-ready AI applications using LLMs, RAG, and AI Agents."
> **Target Role:** AI Engineer / LLM Engineer / Agentic AI Developer
> **NOT:** ❌ Data Scientist ❌ ML Researcher ❌ Kaggle competitor
> **Timeline:** 4 months aggressive | 6 months comfortable
> **Market:** India + Remote

---

## Legend

| Tag | Meaning |
|---|---|
| ✅ **(Must Learn)** | Non-negotiable — you will be tested on this |
| 🟡 **(Good to Know)** | Boosts your profile in senior rounds |
| ❌ **(Skip)** | Don't spend a single hour on this |

---

# PHASE 1 — PYTHON FOR AI (Weeks 1–2)

> **Mindset:** You're not learning Python from scratch. You're *translating* your JS mental model.

### Mental Model Mapping

| You Already Know (JS) | Learn the Python Equivalent |
|---|---|
| `npm` / `package.json` | `pip` / `requirements.txt` / `pyproject.toml` |
| `nvm` | `venv` / `conda` |
| Express | FastAPI |
| Middleware | Dependency Injection |
| Joi / Zod | Pydantic |
| `async/await` | `asyncio` / `await` |
| TypeScript types | Type hints |

### What to Learn

| Topic | Priority | Notes |
|---|---|---|
| Core syntax, list comprehensions, f-strings | ✅ Must Learn | 2–3 days max coming from JS |
| Virtual environments (`venv`) | ✅ Must Learn | Create one for every project |
| `pip`, `requirements.txt`, dependency management | ✅ Must Learn | Your `npm install` equivalent |
| Type hints + Pydantic | ✅ Must Learn | Used everywhere — FastAPI, LangChain, structured outputs |
| OOP (classes, inheritance, dunder methods) | ✅ Must Learn | LangChain & frameworks use OOP heavily |
| Decorators & context managers | ✅ Must Learn | `@app.get()` is a decorator |
| Async/await in Python | 🟡 Good to Know | You already understand the concept |
| File handling (read/write, CSV, JSON) | ✅ Must Learn | Data ingestion basics |

### Resources
- [Python for JavaScript Developers](https://www.valentinog.com/blog/python-for-js/) — read first
- *Automate the Boring Stuff* — Chapters 1–8 (free online)
- FastAPI official tutorial (you already studied this!)

### 🎯 Phase 1 Project: Rewrite Your Node API in FastAPI
- Pick any Express API you've built → rebuild it in FastAPI
- Use Pydantic for validation, dependency injection for auth
- This one project teaches you 80% of the Python you'll need

### ✅ Milestone
> Can write Python fluently, build APIs with FastAPI, and use Pydantic for data validation.

---

# PHASE 2 — AI ENGINEER CORE (Weeks 3–4)

> **Philosophy:** Learn just enough ML to reason about models. Don't become a researcher.

### What to Learn

| Topic | Priority | Why |
|---|---|---|
| What is a model (weights, parameters, inference) | ✅ Must Learn | Foundation for everything |
| Training vs inference | ✅ Must Learn | You'll mostly do inference |
| Embeddings — what they are, how they work | ✅ Must Learn | **THE** most important concept for AI Eng |
| Cosine similarity | ✅ Must Learn | How semantic search works |
| Overfitting / underfitting (conceptual) | ✅ Must Learn | Explains why models fail |
| Evaluation metrics (accuracy, precision, recall, F1) | ✅ Must Learn | Asked in every interview |
| Vectors, matrices, dot product | ✅ Must Learn | Understand embeddings & attention |
| Linear/logistic regression (concept only) | 🟡 Good to Know | 1 hour max |
| Probability basics (Bayes, distributions) | 🟡 Good to Know | Helps with sampling/temperature |
| NumPy basics (arrays, vectorized ops) | ✅ Must Learn | Used under the hood everywhere |
| Pandas basics (DataFrames, cleaning) | 🟡 Good to Know | Useful for dataset prep |

### What to SKIP ❌
- ❌ Calculus proofs, derivatives by hand
- ❌ Building neural networks from scratch
- ❌ CNNs, RNNs, LSTMs in depth
- ❌ scikit-learn classical ML pipeline
- ❌ Kaggle competitions
- ❌ SVMs, Naive Bayes, KNN, PCA
- ❌ TensorFlow

### Resources
- 3Blue1Brown — *Essence of Linear Algebra* (YouTube, 3 hrs) — watch at 1.5x
- 3Blue1Brown — *Neural Networks* series — just the first 3 videos
- StatQuest — Embeddings, Overfitting, Evaluation Metrics (cherry-pick)
- Sentence-Transformers docs — understand embeddings practically

### 🎯 Hands-on Tasks
- Generate embeddings for 100 sentences using Sentence-Transformers → compute cosine similarity
- Implement dot product and cosine similarity from scratch in NumPy
- Use OpenAI embeddings API → compare similar and dissimilar documents

### ✅ Milestone
> Understands models, embeddings, evaluation metrics. Can generate and compare embeddings programmatically.

---

# PHASE 3 — LLMs & GENERATIVE AI ⭐ Main Pillar (Weeks 5–10)

> **This is 60% of your job.** Go deep here.

## 3.1 How LLM Apps Actually Work

| Topic | Priority |
|---|---|
| Tokens & tokenization (BPE, tiktoken) | ✅ Must Learn |
| Context window & token limits | ✅ Must Learn |
| Temperature, top-p, top-k (sampling) | ✅ Must Learn |
| Hallucination — why it happens, how to reduce it | ✅ Must Learn |
| Function calling / tool use | ✅ Must Learn |
| Streaming responses (SSE) | ✅ Must Learn |
| Chat completions API (OpenAI format) | ✅ Must Learn |
| Self-attention & multi-head attention (conceptual) | ✅ Must Learn |
| Transformer architecture (high-level) | ✅ Must Learn |
| Positional encoding | 🟡 Good to Know |

**Resources:**
- Jay Alammar — [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- Andrej Karpathy — *Let's build GPT from scratch* (YouTube) — watch, don't code along
- OpenAI API documentation — read end to end
- 3Blue1Brown — *Attention in Transformers* (YouTube)

---

## 3.2 Prompt Engineering (Production Level)

| Topic | Priority |
|---|---|
| System / user / assistant message roles | ✅ Must Learn |
| Zero-shot & few-shot prompting | ✅ Must Learn |
| Chain-of-thought (CoT) prompting | ✅ Must Learn |
| Structured output (JSON mode) | ✅ Must Learn |
| Prompt chaining (multi-step) | ✅ Must Learn |
| Guardrails & input validation | ✅ Must Learn |
| Prompt injection & safety | ✅ Must Learn |
| ReAct prompting pattern | ✅ Must Learn |
| Prompt templating & versioning | ✅ Must Learn |
| Tree-of-thought | 🟡 Good to Know |

**Resources:**
- OpenAI Prompt Engineering Guide (official)
- Anthropic's Prompt Engineering Guide
- DAIR.AI Prompt Engineering Guide (GitHub)

**🎯 Hands-on Tasks:**
- Build a prompt that extracts structured JSON from unstructured text
- Implement a ReAct loop manually (no framework) with OpenAI function calling
- Create a prompt testing harness — compare outputs across prompting strategies
- Build a prompt that resists injection attacks

---

## 3.3 Embeddings + Vector Databases

| Topic | Priority |
|---|---|
| Text embeddings (OpenAI, Sentence-Transformers, Cohere) | ✅ Must Learn |
| Cosine similarity & semantic search | ✅ Must Learn |
| Chunking strategies (fixed, recursive, semantic) | ✅ Must Learn |
| **PostgreSQL + pgvector** | ✅ Must Learn |
| ChromaDB (for prototyping) | ✅ Must Learn |
| Pinecone (managed, production) | 🟡 Good to Know |
| Indexing strategies (HNSW, IVF) | 🟡 Good to Know |
| Hybrid search (vector + keyword/BM25) | 🟡 Good to Know |

> [!TIP]
> **Start with pgvector.** You already understand PostgreSQL from backend work. One less new technology. Use ChromaDB for quick prototyping, pgvector for production.

**Resources:**
- pgvector documentation & tutorials
- ChromaDB quickstart
- Pinecone Learning Center (free, excellent conceptual material)

---

## 3.4 RAG (Retrieval-Augmented Generation)

| Topic | Priority |
|---|---|
| RAG architecture (retrieve → augment → generate) | ✅ Must Learn |
| Document loading (PDF, web, MD, DOCX) | ✅ Must Learn |
| Chunking strategies & chunk size optimization | ✅ Must Learn |
| Retrieval with source citations | ✅ Must Learn |
| Conversation memory in RAG | ✅ Must Learn |
| Advanced RAG: re-ranking (cross-encoder) | ✅ Must Learn |
| Advanced RAG: query transformation, HyDE | 🟡 Good to Know |
| RAG evaluation (precision@k, MRR, faithfulness) | ✅ Must Learn |
| Multi-modal RAG | 🟡 Good to Know |
| GraphRAG | 🟡 Good to Know |

**Resources:**
- LangChain RAG tutorial (official)
- LlamaIndex RAG documentation
- Ragas documentation (evaluation)

---

## 3.5 Fine-Tuning (Know When & How)

> You won't fine-tune daily, but **you will be asked about it in every interview.**

| Topic | Priority |
|---|---|
| When to fine-tune vs when to prompt-engineer | ✅ Must Learn |
| LoRA & QLoRA (parameter-efficient fine-tuning) | ✅ Must Learn |
| Dataset preparation (format, quality, size) | ✅ Must Learn |
| Hugging Face Transformers + PEFT libraries | ✅ Must Learn |
| Running models locally with Ollama | ✅ Must Learn |
| Full fine-tuning | 🟡 Good to Know |
| RLHF / DPO (concepts only) | 🟡 Good to Know |
| Pre-training from scratch | ❌ Skip |

**Resources:**
- Hugging Face PEFT & LoRA docs
- Hugging Face fine-tuning tutorial
- Ollama documentation

**🎯 Hands-on Task:**
- Fine-tune a small model (Phi-3 or Llama 3 8B) on a custom Q&A dataset with QLoRA
- Compare base vs fine-tuned model outputs side by side

---

## 3.6 LLM Evaluation & Observability

| Topic | Priority |
|---|---|
| LLM-as-a-judge evaluation | ✅ Must Learn |
| Hallucination detection | ✅ Must Learn |
| RAG evaluation with Ragas | ✅ Must Learn |
| Prompt logging & tracing (LangSmith / Langfuse) | ✅ Must Learn |
| Human evaluation frameworks | 🟡 Good to Know |
| Perplexity, BLEU, ROUGE | 🟡 Good to Know |
| Red teaming & safety evaluation | 🟡 Good to Know |

**Resources:**
- Ragas documentation
- LangSmith documentation
- Langfuse documentation (open-source)
- DeepEval library

---

## 🎯 PHASE 3 FLAGSHIP PROJECT — "ChatWithYourData" AI SaaS

> **This project alone makes you interview-ready for most startups.**

**Stack:** FastAPI + React + pgvector + OpenAI/Anthropic + Redis

| Feature | Why It Matters |
|---|---|
| User auth (JWT) | Shows production thinking — you already know this |
| File upload (PDF, DOCX, MD) | Document ingestion pipeline |
| RAG with streaming responses | Core AI Eng skill |
| Source citations | Production RAG requirement |
| Chat history & memory | Conversation management |
| Multi-user / multi-tenant | Shows scalability thinking |
| Prompt logging with Langfuse | Observability |
| Rate limiting | Cost control |

**Architecture:**
```
React Frontend (your strength)
       ↓
FastAPI Backend → Auth, Rate Limiting, Usage Tracking
       ↓
AI Service Layer → LangChain / LlamaIndex
       ↓          ↓             ↓
  pgvector    LLM APIs     PostgreSQL
       ↓
     Redis (caching, memory, queues)
```

### ✅ Phase 3 Milestone
> Can build and deploy a full RAG SaaS product. Understands prompt engineering, embeddings, evaluation, and fine-tuning trade-offs.

---

# PHASE 4 — FRAMEWORKS: LangChain & LlamaIndex (Weeks 8–9)

> **Learn frameworks AFTER you understand the concepts they abstract.** This is critical.

### What to Learn (Focused)

| Framework | What to Learn | What to Skip |
|---|---|---|
| **LangChain** | Chains, Tools, Memory, Output Parsers, Callbacks | Every single integration |
| **LlamaIndex** | Data connectors, indexing, query engines | Advanced node parsers |
| **LangGraph** ⭐ | State machines, agent graphs, checkpointing | — learn deeply |
| **LangSmith** | Tracing, evaluation, prompt management | — |

**Resources:**
- LangChain documentation — Conceptual Guide first, then How-To
- LangGraph documentation — follow the tutorials end to end
- LlamaIndex documentation — focus on RAG pipeline

**🎯 Hands-on Task:**
- Rebuild your RAG project using LangChain, then again with LlamaIndex — compare DX
- Build a stateful conversation agent with LangGraph

### ✅ Milestone
> Can use LangChain, LlamaIndex, and LangGraph effectively. Knows when to use which.

---

# PHASE 5 — AGENTIC AI ⭐ Your Specialization (Weeks 10–13)

> **This is your differentiator.** Most candidates can't build agents. Your backend experience gives you an unfair advantage — agents are essentially complex backend orchestration.

## 5.1 AI Agent Architecture

| Topic | Priority |
|---|---|
| Agent loop: perceive → reason → act | ✅ Must Learn |
| ReAct pattern (Reasoning + Acting) | ✅ Must Learn |
| Tool use & function calling | ✅ Must Learn |
| Structured output for tool invocation | ✅ Must Learn |
| Agent memory (short-term, long-term, episodic) | ✅ Must Learn |
| Planning strategies (task decomposition, reflection) | ✅ Must Learn |
| Human-in-the-loop patterns | ✅ Must Learn |
| Agent guardrails & safety | ✅ Must Learn |
| Agent evaluation & debugging | ✅ Must Learn |

**Resources:**
- Lilian Weng — [LLM-Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) (blog)
- Andrew Ng — *AI Agentic Design Patterns* (DeepLearning.AI, free)
- LangGraph agent tutorials (official)
- OpenAI function calling documentation

**🎯 Hands-on Task:**
- Build a ReAct agent **from scratch** (no framework) using OpenAI function calling
- Add persistent memory using a vector DB
- Add reflection — agent reviews its own output and improves

---

## 5.2 Multi-Agent Systems

| Topic | Priority |
|---|---|
| Multi-agent architectures (supervisor, swarm, hierarchical) | ✅ Must Learn |
| Agent communication patterns | ✅ Must Learn |
| LangGraph multi-agent setup ⭐ | ✅ Must Learn |
| CrewAI | ✅ Must Learn |
| AutoGen | 🟡 Good to Know |
| Orchestration & state management | ✅ Must Learn |

**Resources:**
- LangGraph multi-agent tutorials
- CrewAI documentation
- DeepLearning.AI — *Multi AI Agent Systems* (short course)

---

## 🎯 PHASE 5 FLAGSHIP PROJECT — Multi-Tool AI Agent for Developers

> **This is resume gold.** No other project screams "I understand Agentic AI" louder.

**Concept:** AI coding assistant for your own GitHub repositories

**Tools the agent can use:**

| Tool | What It Does |
|---|---|
| `read_repo` | Clone and read repository structure & files |
| `search_code` | Semantic search across the codebase |
| `explain_code` | Explain a function/file |
| `write_tests` | Generate unit tests for a function |
| `create_pr` | Create a pull request with changes |
| `review_code` | Review a PR and suggest improvements |

**Architecture:** Multi-agent with supervisor

```
User Request
     ↓
Supervisor Agent (orchestrates)
     ↓ ↓ ↓ ↓
  Planner → Coder → Reviewer → PR Creator
     ↓
  Tool Registry (GitHub API, file system, search)
     ↓
  Memory (conversation + project context)
```

**Stack:** LangGraph + FastAPI + OpenAI/Claude + GitHub API + pgvector

### ✅ Phase 5 Milestone
> Can design, build, and debug AI agents and multi-agent systems with tools, memory, and planning.

---

# PHASE 6 — DEPLOYMENT & PRODUCTION (Weeks 14–16)

> **Your full-stack skills shine here.** Most ML engineers can't deploy. You can.

## What to Learn

| Topic | Priority | Your Advantage |
|---|---|---|
| Docker for AI apps | ✅ Must Learn | You've deployed apps before |
| FastAPI for model serving | ✅ Must Learn | Already know FastAPI |
| Streaming responses (SSE) | ✅ Must Learn | Critical for chat UIs |
| WebSockets for real-time chat | ✅ Must Learn | You know this from Node.js |
| Background workers (Celery / ARQ) | ✅ Must Learn | For long-running AI tasks |
| Redis for caching & memory | ✅ Must Learn | Session memory, response caching |
| LLM observability (LangSmith / Langfuse) | ✅ Must Learn | Production requirement |
| Cost optimization (caching, model routing, token tracking) | ✅ Must Learn | Companies obsess over LLM costs |
| Prompt versioning (treat prompts as code) | ✅ Must Learn | — |
| CI/CD with prompt regression tests | ✅ Must Learn | GitHub Actions |
| GPU serving (vLLM, TGI) | 🟡 Good to Know | For self-hosted models |
| Kubernetes | ❌ Skip | Infra team handles this |
| ML pipelines (Airflow, etc.) | ❌ Skip | Data engineering, not AI Eng |

**Cost Optimization Techniques (interviewers love this):**

| Technique | How It Works |
|---|---|
| Semantic caching | Cache responses for similar queries using embedding similarity |
| Model routing | Use cheap models (GPT-4o-mini) for simple tasks, expensive ones only when needed |
| Token tracking | Monitor and limit token usage per user/request |
| Batching | Batch multiple requests for efficiency |
| Prompt optimization | Shorter prompts = fewer tokens = less cost |

**🎯 Hands-on Tasks:**
- Dockerize your RAG SaaS app → deploy to a cloud service
- Set up Langfuse tracing → analyze prompt performance
- Implement semantic caching with Redis + embeddings
- Build a CI pipeline that runs prompt regression tests on every push

### ✅ Milestone
> Can containerize, deploy, monitor, and cost-optimize AI applications in production.

---

# PHASE 7 — 3 FLAGSHIP PROJECTS (Your Portfolio)

> 3 deep projects beat 10 shallow ones. These map directly to AI Engineer job descriptions.

| # | Project | What It Proves |
|---|---|---|
| 🥇 | **ChatWithYourData — Production RAG SaaS** (Phase 3) | "I build production AI products end-to-end" |
| 🥈 | **Multi-Tool AI Agent for Developers** (Phase 5) | "I understand Agentic AI architecture deeply" |
| 🥉 | **AI Feature in Your Existing MERN App** (below) | "I integrate AI into real products" |

### 🥉 Project 3: AI-Powered Feature in a MERN App

Pick one of your existing MERN projects and add a *real* AI feature:

| Idea | What It Adds |
|---|---|
| AI support chatbot | RAG over your app's docs + conversation memory |
| AI-powered search | Semantic search replacing keyword search |
| AI content generator | Generate descriptions, summaries, or reports |
| Smart assistant | Agent that performs actions in your app (e.g., "create an employee record for John") |

> [!IMPORTANT]
> This project is your **killer differentiator**. It shows you're not just building AI demos — you integrate AI into real products. This is exactly what companies hire AI Engineers to do.

---

# PHASE 8 — JOB PREPARATION (Weeks 15–16)

## 8.1 Resume Positioning

**Headline:**
> `AI Engineer | LLM • RAG • AI Agents | FastAPI • React • Node.js`

**Summary Template:**
> AI Engineer with full-stack development background. I build production-ready AI applications using LLMs, RAG, and agentic architectures. Built [ChatWithYourData], a multi-tenant RAG SaaS, and [DevAgent], an autonomous coding assistant. Experienced in FastAPI, LangChain, LangGraph, and React.

**Frame your MERN experience as a strength:**

| MERN Skill | How It Maps to AI Eng |
|---|---|
| React | Build AI product frontends, chat UIs, agent dashboards |
| Node.js / Express | API design → FastAPI transition |
| MongoDB | NoSQL → document storage in RAG |
| Auth (JWT) | User management for AI SaaS |
| Deployment | CI/CD → Docker + AI serving |
| System Design | End-to-end AI system architecture |

---

## 8.2 GitHub Project Structure

```
project-name/
├── README.md              # ⭐ Overview, architecture diagram, demo GIF, setup
├── docs/
│   ├── architecture.md    # System design with diagrams
│   └── api-reference.md
├── src/
│   ├── agents/            # Agent definitions
│   ├── chains/            # LangChain chains
│   ├── api/               # FastAPI routes
│   ├── services/          # Business logic
│   └── utils/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── .github/workflows/     # CI/CD
```

> [!TIP]
> Every repo MUST have: a clean README with architecture diagram, a demo video/GIF, a deployment link, and a `.env.example`. Recruiters spend 30 seconds per repo.

---

## 8.3 Interview Questions by Category

### System Design (Most Common)

| Question | What They're Testing |
|---|---|
| "Design a RAG system for 10M documents" | Chunking, indexing, retrieval at scale, caching |
| "Build a customer support bot" | RAG + agents + escalation + memory |
| "How would you reduce LLM costs by 70%?" | Caching, model routing, prompt optimization |
| "Design a multi-agent workflow system" | Orchestration, state management, error handling |

### LLM & RAG Deep-Dive

| Question | What They're Testing |
|---|---|
| How do transformers / attention work? | Conceptual understanding |
| How do you handle hallucinations? | Grounding, RAG, evaluation |
| Compare chunking strategies | Fixed vs recursive vs semantic, trade-offs |
| When to fine-tune vs prompt-engineer? | Decision framework, cost/benefit |
| How do you evaluate RAG quality? | Metrics: faithfulness, relevance, precision@k |

### Agent-Specific

| Question | What They're Testing |
|---|---|
| Explain the ReAct pattern | Agent architecture |
| How do agents use tools? | Function calling, structured output |
| How would you add memory to an agent? | Short-term vs long-term, vector DB |
| Design a multi-agent system for X | Orchestration, communication, error handling |

### Production & Deployment

| Question | What They're Testing |
|---|---|
| How do you monitor LLM apps? | Observability: LangSmith, Langfuse |
| How do you handle streaming? | SSE, WebSockets, chunked responses |
| How do you version prompts? | Prompt-as-code, regression testing |
| How do you optimize costs? | Caching, routing, batching, token tracking |

---

## 8.4 Where to Apply

### Target Companies (India)

| Category | Companies |
|---|---|
| AI-First Startups | Ema, Sarvam AI, Krutrim, Yellow.ai, Haptik, Observe.AI, Pixis |
| Product Companies | Flipkart, Swiggy, Razorpay, CRED, PhonePe, Meesho |
| Tech Giants | Google, Microsoft, Amazon, Meta (India offices) |
| Consulting | TCS AI, Infosys Topaz, Wipro AI, Accenture AI |

### Target Roles & Salary

| Role | India Salary | Remote Salary |
|---|---|---|
| AI Engineer | ₹12–30 LPA | $80–150K |
| LLM Engineer | ₹15–35 LPA | $90–160K |
| Agentic AI Developer | ₹18–40 LPA | $100–180K |
| AI Application Developer | ₹10–25 LPA | $70–130K |

### Platforms

| Platform | Best For |
|---|---|
| LinkedIn | All roles + networking |
| Wellfound (AngelList) | Startups (India + Remote) |
| Naukri / Instahyre | India-based roles |
| Y Combinator — Work at a Startup | Remote startup roles |
| Toptal / Turing | Remote freelance AI roles |

---

# PHASE 9 — TIMELINES

## ⚡ 4-Month Aggressive Plan (3 hrs/day)

| Month | Focus | Deliverable |
|---|---|---|
| **Month 1** | Python fast-track + AI core + LLM basics | FastAPI app rebuilt, embeddings mastery |
| **Month 2** | RAG + Vector DB + Prompt Eng + Evaluation | 🥇 **Project 1: ChatWithYourData** |
| **Month 3** | Agents + LangGraph + Multi-agent + CrewAI | 🥈 **Project 2: DevAgent** |
| **Month 4** | Deployment + Portfolio + Interview prep | 🥉 **Project 3: AI in MERN app** + resume ready |

## 📅 6-Month Comfortable Plan (2 hrs/day)

| Month | Focus | Deliverable |
|---|---|---|
| **Month 1** | Python + FastAPI | API rebuilt in FastAPI |
| **Month 2** | AI core + LLMs + Prompt Eng | Embeddings, prompt mastery |
| **Month 3** | RAG + Vector DB + Evaluation | 🥇 Project 1 |
| **Month 4** | Frameworks + Fine-tuning | LangChain/LlamaIndex proficiency |
| **Month 5** | Agents + Multi-agent | 🥈 Project 2 |
| **Month 6** | Deployment + Portfolio + Job prep | 🥉 Project 3 + Job ready |

---

# PHASE 10 — DAILY STUDY PLAN

## 2-Hour Plan

| Time | Activity |
|---|---|
| **0:00 – 0:45** | 📖 Learn one focused concept (docs, video) |
| **0:45 – 1:45** | 💻 Build / code / experiment |
| **1:45 – 2:00** | 📝 Commit to GitHub + plan tomorrow |

## 3-Hour Plan

| Time | Activity |
|---|---|
| **0:00 – 0:45** | 📖 Concept study |
| **0:45 – 2:15** | 💻 Project work (the bulk) |
| **2:15 – 2:45** | 🧪 Experiment, debug, optimize |
| **2:45 – 3:00** | 📝 Commit + document + plan tomorrow |

## Weekly Rhythm

| Day | Focus |
|---|---|
| **Mon–Thu** | Learn + Build (concept → code) |
| **Fri** | Polish, refactor, write tests |
| **Sat** | Review week + write one blog post / README update |
| **Sun** | Rest or light reading (AI news, papers, blog posts) |

---

# TECH STACK CHEAT SHEET

| Category | Tools |
|---|---|
| **Language** | Python |
| **API Framework** | FastAPI |
| **LLM Providers** | OpenAI (GPT-4o), Anthropic (Claude), Ollama (local) |
| **LLM Frameworks** | LangChain, LangGraph ⭐, LlamaIndex |
| **Agent Frameworks** | LangGraph ⭐, CrewAI |
| **Vector DB** | pgvector (production), ChromaDB (prototyping) |
| **Embeddings** | OpenAI, Sentence-Transformers |
| **Fine-tuning** | Hugging Face Transformers + PEFT, QLoRA |
| **Observability** | LangSmith, Langfuse |
| **Evaluation** | Ragas, DeepEval |
| **Frontend** | React (your strength) |
| **Deployment** | Docker, GitHub Actions |
| **Caching/Queue** | Redis |
| **Demo UIs** | Streamlit, Gradio |

---

> [!IMPORTANT]
> **Start today. Build Project 1. Push to GitHub daily. In 4 months, you'll have a portfolio that most "AI Engineers" with certificates can't match — because you'll have actually *built* things.**
