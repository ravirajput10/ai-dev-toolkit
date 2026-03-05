# 🗺️ MCP (Model Context Protocol) — Learning Roadmap

> A structured path to master MCP, from basics to production-grade servers.

---

## 📌 Where You Are Now

After building the DevToolkit MCP server, you already know:
- [x] What MCP is and why it exists
- [x] `FastMCP` — creating a server instance
- [x] `@mcp.tool()` — registering tools
- [x] Type hints → auto-generated schemas
- [x] Docstrings → tool descriptions for AI
- [x] stdio transport
- [x] Testing with MCP Inspector
- [x] Connecting to clients (Antigravity, Cursor, Claude Desktop)

**Now let's go deeper.** 👇

---

## Phase 1 — MCP Core Concepts ✅ (Done)

| Topic | Status | Where You Learned It |
|---|---|---|
| Tools (functions AI can call) | ✅ Done | `server.py` — 8 tools built |
| Type hints + docstrings | ✅ Done | Every tool uses them |
| stdio transport | ✅ Done | `mcp.run(transport="stdio")` |
| MCP Inspector | ✅ Done | `mcp dev server.py` |
| Client configuration | ✅ Done | `mcp_config.json` for Antigravity |

---

## Phase 2 — Resources & Prompts (Next Step)

> Tools let AI *do things*. Resources let AI *read things*. Prompts give AI *templates*.

### 2.1 Resources (Read-only data for AI)

| Topic | Priority |
|---|---|
| What are Resources vs Tools | ✅ Must Learn |
| `@mcp.resource()` decorator | ✅ Must Learn |
| Static resources (fixed URI) | ✅ Must Learn |
| Dynamic resources (parameterized URI) | ✅ Must Learn |
| Resource templates | 🟡 Good to Know |

**Code example:**
```python
@mcp.resource("config://app-settings")
def get_app_settings() -> str:
    """Application configuration settings."""
    return json.dumps({"theme": "dark", "version": "1.0"})

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read a file from the project directory."""
    with open(path, "r") as f:
        return f.read()
```

**Project idea:** Add resources to your DevToolkit that expose system info (OS, Python version, disk space).

---

### 2.2 Prompts (Reusable templates)

| Topic | Priority |
|---|---|
| What are Prompts | 🟡 Good to Know |
| `@mcp.prompt()` decorator | 🟡 Good to Know |
| Parameterized prompts | 🟡 Good to Know |

**Code example:**
```python
@mcp.prompt()
def code_review(code: str, language: str) -> str:
    """Generate a code review prompt."""
    return f"Review this {language} code for bugs, security issues, and best practices:\n\n{code}"
```

---

## Phase 3 — External APIs & Async Tools

> Real-world MCP servers connect to external services.

| Topic | Priority |
|---|---|
| Async tools (`async def`) | ✅ Must Learn |
| HTTP requests with `httpx` | ✅ Must Learn |
| API key management (env variables) | ✅ Must Learn |
| Rate limiting & caching | 🟡 Good to Know |
| Error handling for external APIs | ✅ Must Learn |

**Project idea:** Build an MCP server that:
- Fetches weather data from a free API
- Searches GitHub repos
- Gets latest news headlines
- Translates text using a translation API

**Code pattern:**
```python
import httpx
import os

@mcp.tool()
async def search_github(query: str) -> str:
    """Search GitHub repositories."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "per_page": 5},
            headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
        )
        data = response.json()
        results = []
        for repo in data["items"]:
            results.append(f"⭐ {repo['stargazers_count']} | {repo['full_name']}: {repo['description']}")
        return "\n".join(results)
```

---

## Phase 4 — Database-Connected MCP Servers

> Give AI the ability to query and manage data.

| Topic | Priority |
|---|---|
| SQLite / PostgreSQL tools | ✅ Must Learn |
| CRUD operations via MCP | ✅ Must Learn |
| Read-only vs read-write safety | ✅ Must Learn |
| Connection pooling | 🟡 Good to Know |

**Project idea:** Build a "Notes Manager" MCP server:
- `create_note(title, content)` — save to SQLite
- `search_notes(query)` — search by keyword
- `list_notes()` — list all notes
- `delete_note(id)` — remove a note

This is a mini CRUD app exposed via MCP — combines your backend skills with MCP!

---

## Phase 5 — SSE Transport & Remote Servers

> Run MCP servers remotely, not just locally.

| Topic | Priority |
|---|---|
| SSE (Server-Sent Events) transport | ✅ Must Learn |
| Running MCP over HTTP | ✅ Must Learn |
| Authentication for remote MCP | ✅ Must Learn |
| Deploying MCP server (Docker) | 🟡 Good to Know |

**Code change — just one line:**
```python
# Local (what we use now)
mcp.run(transport="stdio")

# Remote (accessible over HTTP)
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

**Project idea:** Deploy your DevToolkit MCP server to a cloud service, connect from anywhere.

---

## Phase 6 — Advanced Patterns

| Topic | Priority |
|---|---|
| Middleware & lifecycle hooks | 🟡 Good to Know |
| Tool composition (tools calling tools) | 🟡 Good to Know |
| Context & state management | ✅ Must Learn |
| Logging & observability | ✅ Must Learn |
| Multi-server architecture | 🟡 Good to Know |
| MCP + LangChain integration | ✅ Must Learn |
| MCP + AI Agents | ✅ Must Learn |

---

## Phase 7 — Production MCP Servers

| Topic | Priority |
|---|---|
| Error handling best practices | ✅ Must Learn |
| Input validation & sanitization | ✅ Must Learn |
| Security (prevent shell injection, file traversal) | ✅ Must Learn |
| Testing MCP servers (unit tests) | ✅ Must Learn |
| CI/CD for MCP servers | 🟡 Good to Know |
| Publishing to MCP registries | 🟡 Good to Know |

---

## 🏗️ Project Progression

| # | Project | Phase | Skills Practiced |
|---|---|---|---|
| 1 | ✅ **DevToolkit** (done!) | Phase 1 | Tools, types, docstrings, stdio |
| 2 | **System Info Server** | Phase 2 | Resources, dynamic data |
| 3 | **GitHub/API Server** | Phase 3 | Async, external APIs, env vars |
| 4 | **Notes Manager** | Phase 4 | Database, CRUD, read/write safety |
| 5 | **Remote DevToolkit** | Phase 5 | SSE transport, deployment |
| 6 | **AI Agent + MCP** | Phase 6-7 | Agent calls MCP tools, production patterns |

---

## 📚 Resources

| Resource | Type | URL |
|---|---|---|
| MCP Official Docs | Documentation | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| MCP Specification | Spec | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io) |
| FastMCP Documentation | Documentation | [gofastmcp.com](https://gofastmcp.com) |
| MCP Python SDK (GitHub) | Source Code | [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) |
| Awesome MCP Servers | Curated List | [github.com/punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) |
| MCP Example Servers | Examples | [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |

---

## ⏱️ Timeline

| Week | Focus | Deliverable |
|---|---|---|
| Week 1 ✅ | Phase 1 — Core (done!) | DevToolkit MCP server |
| Week 2 | Phase 2 + 3 — Resources & APIs | System Info + GitHub MCP server |
| Week 3 | Phase 4 — Database | Notes Manager MCP server |
| Week 4 | Phase 5 + 6 — Remote + Advanced | Deploy remotely + Agent integration |
