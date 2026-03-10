# 🛠️ AI Dev Toolkit

> A collection of AI-powered developer tools — MCP servers and AI agents built from scratch.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What Is This?

This repo contains hands-on AI engineering projects built while learning to create MCP servers and AI agents. Each project is thoroughly documented with learning notes explaining the **what, why, and how**.

**Built by:** A full-stack (MERN) developer transitioning into AI Engineering.

---

## 📂 Project Structure

```
ai-dev-toolkit/
├── mcp-server/                  # MCP Server — Developer Toolkit
│   ├── app.py                   # Shared FastMCP instance
│   ├── server.py                # Entry point (stdio transport)
│   ├── server_sse.py            # Entry point (SSE/HTTP transport)
│   ├── validators.py            # Input validation & security
│   ├── tools/
│   │   ├── dev_tools.py         # 9 core tools (Phase 1)
│   │   ├── api_tools.py         # 3 async API tools (Phase 3)
│   │   ├── db_tools.py          # 4 database CRUD tools (Phase 4)
│   │   └── advanced_tools.py    # 3 advanced tools (Phase 6)
│   ├── resources/
│   │   └── system_resources.py  # 6 system resources (Phase 2)
│   ├── prompts/
│   │   └── code_prompts.py      # 3 code prompts (Phase 2)
│   ├── db/
│   │   └── database.py          # SQLite setup & connection
│   ├── tests/
│   │   └── test_validators.py   # 37 unit tests (Phase 7)
│   └── requirements.txt         # Python dependencies
├── docs/
│   ├── mcp-learning-roadmap.md  # Learning roadmap
│   ├── mcp-mastery-notes.md     # Concept reference
│   └── TUTORIAL.md              # Getting started guide
├── AI_ENGINEER_ROADMAP.md       # AI Engineering learning path
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 MCP Server — Developer Toolkit

A Model Context Protocol (MCP) server with **19 tools**, **6 resources**, and **3 prompts** for AI assistants.

### Tools (19)

| Category | Tools | File |
|---|---|---|
| **Core Dev Tools** | `greet`, `generate_uuid`, `format_json`, `base64_encode`, `base64_decode`, `hash_text`, `word_count`, `timestamp_convert`, `regex_test` | `tools/dev_tools.py` |
| **API Tools** | `search_github`, `get_weather`, `fetch_url` | `tools/api_tools.py` |
| **Database Tools** | `create_note`, `list_notes`, `search_notes`, `delete_note` | `tools/db_tools.py` |
| **Advanced Tools** | `system_health_check`, `smart_note_search`, `bulk_create_notes` | `tools/advanced_tools.py` |

### Resources (6)

`system://info`, `system://env`, `system://packages`, `project://structure`, `config://server`, `docs://readme`

### Prompts (3)

`code_review`, `explain_code`, `debug_error`

### Quick Start

```bash
# Clone the repo
git clone https://github.com/ravirajput10/ai-dev-toolkit.git
cd ai-dev-toolkit/mcp-server

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test with MCP Inspector
mcp dev server.py
```

### Run as Remote Server (SSE)

```bash
python server_sse.py                           # Default: localhost:8000
python server_sse.py --host 0.0.0.0 --port 9000 # Custom
```

### Run Unit Tests

```bash
python tests\test_validators.py -v   # 37 tests
```

### Connect to AI Clients

```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "python",
      "args": ["path/to/ai-dev-toolkit/mcp-server/server.py"]
    }
  }
}
```

---

## 🧠 Learning Notes

Each phase includes detailed tutorials with:
- Concept explanations mapped to Express/Node.js analogies
- Step-by-step build guides
- Revision sheets and key patterns

📖 Start with [TUTORIAL.md](mcp-server/TUTORIAL.md) → then Phase 2-7 tutorials.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| MCP SDK (`FastMCP`) | MCP server framework |
| `httpx` | Async HTTP client (API tools) |
| SQLite | Database (notes manager) |
| `unittest` | Unit testing |

---

## 📄 License

MIT License — feel free to use, modify, and learn from this code.
