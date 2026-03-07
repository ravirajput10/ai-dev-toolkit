# 🌐 Phase 5 — SSE Transport & Remote MCP Server

> **Goal:** Learn to run your MCP server over HTTP so it's accessible remotely (not just locally via stdio).
> **What you'll build:** A remote version of your DevToolkit server using SSE transport.
> **Time:** ~30 minutes

---

## 🧠 Before We Start — stdio vs SSE

You've been using **stdio** transport — the client starts your server as a subprocess and communicates via stdin/stdout. This only works locally.

**SSE (Server-Sent Events)** runs your server as a web service on a port — any client on the network can connect.

```
STDIO (What you've been using)        SSE (What you'll learn)
─────────────────────────────         ─────────────────────────────
Client starts server as subprocess    Server runs independently on a port
Only works locally                    Works over network/internet
Client ←stdin/stdout→ Server          Client ←HTTP→ Server
No URL, no port                       Has URL: http://localhost:8000/sse
One client at a time                  Multiple clients can connect
```

### Your Express Analogy

```javascript
// STDIO = like running a script
node script.js              // Process runs, does work, exits

// SSE = like running an Express server
app.listen(8000)            // Server stays running, listens for requests
// Anyone can connect to http://localhost:8000
```

---

# STEP 1 — Create a Remote Server Entry Point

We'll keep the existing `server.py` (stdio) and create a **separate entry point** for SSE.

## ▶️ Code — Create `server_sse.py` in `mcp-server/`

```python
"""
SSE (Server-Sent Events) Entry Point
======================================
Runs the MCP server over HTTP instead of stdio.
This allows remote clients to connect over the network.

Usage:
    python server_sse.py                              # Default: localhost:8000
    python server_sse.py --host 0.0.0.0 --port 9000   # Custom host/port
"""

import sys
from app import mcp

# Import all modules (same as server.py)
from tools import dev_tools, api_tools, db_tools
from resources import system_resources
from prompts import code_prompts
from db.database import init_db

# Initialize database
init_db()

# Parse command line arguments for custom host and port
# host/port live on mcp.settings (not on mcp.run())
for i, arg in enumerate(sys.argv[1:], 1):
    if arg == "--host" and i < len(sys.argv) - 1:
        mcp.settings.host = sys.argv[i + 1]
    elif arg == "--port" and i < len(sys.argv) - 1:
        mcp.settings.port = int(sys.argv[i + 1])

if __name__ == "__main__":
    host = mcp.settings.host
    port = mcp.settings.port
    print(f"🚀 Starting MCP SSE server on http://{host}:{port}/sse")
    print(f"   Press Ctrl+C to stop")
    mcp.run(transport="sse")
```

### Key Differences from `server.py`

```python
# server.py (local)
mcp.run(transport="stdio")

# server_sse.py (remote) — host/port live on mcp.settings
mcp.settings.host = "127.0.0.1"  # or "0.0.0.0" for network access
mcp.settings.port = 8000
mcp.run(transport="sse")
```

| Setting | What It Does |
|---|---|
| `transport="sse"` | Use HTTP-based SSE instead of stdin/stdout |
| `mcp.settings.host = "127.0.0.1"` | Only accept local connections |
| `mcp.settings.host = "0.0.0.0"` | Accept connections from any IP (for network access) |
| `mcp.settings.port = 8000` | HTTP port to listen on |

> **⚠️ Important:** `host` and `port` go on `mcp.settings`, NOT as args to `mcp.run()`. This is a common gotcha!

---

# STEP 2 — Run the SSE Server

## ▶️ Run This Now

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit\mcp-server"
.\venv\Scripts\python.exe server_sse.py
```

You should see:
```
🚀 Starting MCP SSE server on http://127.0.0.1:8000/sse
   Press Ctrl+C to stop
```

**The server is now running as a web service!** It stays running like an Express server.

---

# STEP 3 — Test with MCP Inspector

Open a **new terminal** and run:

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit\mcp-server"
.\venv\Scripts\Activate.ps1
npx @modelcontextprotocol/inspector
```

In the Inspector:
1. Change **Transport Type** to **SSE** (dropdown at the top)
2. Set **URL** to: `http://127.0.0.1:8000/sse`
3. Click **Connect**
4. Test your tools — they all work the same!

---

# STEP 4 — Connect from Client Config (SSE)

### Antigravity / Claude Desktop Config

For stdio (what you had):
```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "python.exe",
      "args": ["server.py"]
    }
  }
}
```

For SSE (remote):
```json
{
  "mcpServers": {
    "dev-toolkit-remote": {
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Notice:** No `command` or `args` — the client doesn't start the server. You start it yourself, and the client just connects to the URL.

---

# STEP 5 — Understanding the SSE Flow

```
STDIO Flow:
───────────────────────────────────────────
Client starts server → stdin/stdout → Server exits when client disconnects

SSE Flow:
───────────────────────────────────────────
1. You start server:    python server_sse.py
2. Server listens on:   http://localhost:8000/sse
3. Client connects:     GET /sse  (opens SSE stream)
4. Client sends:        POST /messages  (JSON-RPC requests)
5. Server responds:     via the SSE stream
6. Server keeps running even if client disconnects
```

### Your Express Analogy

```javascript
// SSE in Express — you've done this!
app.get('/sse', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Connection', 'keep-alive');
    // Server sends events to client over this open connection
});

// MCP uses the same pattern — SSE for server→client, POST for client→server
```

---

# STEP 6 — When to Use stdio vs SSE

| Scenario | Use |
|---|---|
| Local development | ✅ stdio |
| AI client on same machine | ✅ stdio |
| Server on a remote machine | ✅ SSE |
| Multiple clients connecting | ✅ SSE |
| Deploying to cloud (AWS, Railway, etc.) | ✅ SSE |
| Team sharing one MCP server | ✅ SSE |
| Simple personal use | ✅ stdio |

---

# STEP 7 — Commit & Push

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: Phase 5 - add SSE transport entry point for remote MCP server"
git push origin main
```

---

# 📋 Phase 5 Revision Sheet

## Two Ways to Run Your Server

```python
# LOCAL (stdio) — client starts the server
mcp.run(transport="stdio")
# Client config: {"command": "python.exe", "args": ["server.py"]}

# REMOTE (SSE) — you start the server, clients connect
mcp.settings.host = "0.0.0.0"   # host/port go on settings
mcp.settings.port = 8000
mcp.run(transport="sse")
# Client config: {"url": "http://your-server:8000/sse"}
```

## SSE Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/sse` | GET | Opens SSE stream (server → client) |
| `/messages` | POST | Client sends JSON-RPC requests |

## Host Values

| Value | Who Can Connect |
|---|---|
| `127.0.0.1` | Only this machine (safe for dev) |
| `0.0.0.0` | Any IP on the network (needed for remote/cloud) |

## Express Mapping

| Express | MCP SSE |
|---|---|
| `app.listen(8000)` | `mcp.settings.port = 8000; mcp.run(transport="sse")` |
| `app.get('/sse', handler)` | Auto-created by FastMCP |
| `app.post('/messages', handler)` | Auto-created by FastMCP |
| Client visits `http://localhost:8000` | Client connects to `http://localhost:8000/sse` |

## What You Learned in Phase 5

| Concept | Key Point |
|---|---|
| SSE Transport | HTTP-based, server runs independently |
| `host` parameter | `127.0.0.1` = local only, `0.0.0.0` = network |
| Two entry points | `server.py` (stdio) and `server_sse.py` (SSE) |
| Client config | SSE uses `"url"` instead of `"command"` |
| When to use which | Local dev → stdio, remote/cloud → SSE |
