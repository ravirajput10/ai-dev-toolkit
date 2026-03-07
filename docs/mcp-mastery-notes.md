# 📘 MCP Mastery Notes — Foundation to Advanced

> **Purpose:** A complete reference to master MCP. Covers everything from prerequisites to production patterns.
> **How to use:** Read top to bottom the first time. Revisit specific sections when you encounter them in practice.

---

# PART 1 — PREREQUISITES (Things You Need to Know BEFORE MCP)

> These are the building blocks MCP is built on. If you skip these, MCP will feel like magic. If you understand these, MCP is simple.

---

## 1.1 JSON-RPC 2.0

### What is it?

JSON-RPC is a protocol for calling functions remotely using JSON. MCP uses it for all communication.

**Your analogy:** In REST, you call `POST /api/users` with a JSON body. In JSON-RPC, you call a method name with parameters — but it's ALL done through JSON, no URL paths.

### How it works

**A JSON-RPC Request:**
```json
{
  "jsonrpc": "2.0",          // Always "2.0" — protocol version
  "method": "tools/call",    // The "endpoint" — what you want to do
  "params": {                // The "request body" — data you're sending
    "name": "hash_text",
    "arguments": { "text": "hello" }
  },
  "id": 1                    // Request ID — matches request to response
}
```

**A JSON-RPC Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {                // The "response body"
    "content": [{
      "type": "text",
      "text": "Hash: 2cf24dba..."
    }]
  },
  "id": 1                    // Same ID — so you know which request this answers
}
```

**A JSON-RPC Error:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params"
  },
  "id": 1
}
```

### REST vs JSON-RPC — Side by Side

| REST | JSON-RPC |
|---|---|
| `POST /api/hash` with body `{text: "hello"}` | `{method: "tools/call", params: {name: "hash_text", arguments: {text: "hello"}}}` |
| Different URLs for different actions | Same channel, different `method` values |
| HTTP status codes (200, 404, 500) | `result` for success, `error` for failure |
| Works over HTTP | Works over ANY transport (stdio, HTTP, WebSocket) |

### Why MCP uses JSON-RPC (not REST)

1. **Transport-agnostic** — works over stdio (local) AND HTTP (remote)
2. **Bidirectional** — both client and server can send messages
3. **Simple** — no URL routing, no headers, just JSON objects
4. **Notifications** — can send messages without expecting a response

### Key terms you'll encounter

| Term | Meaning |
|---|---|
| **Request** | Message expecting a response (has `id`) |
| **Notification** | Message NOT expecting a response (no `id`) |
| **Method** | The function being called (like `tools/call`, `resources/read`) |
| **Params** | Arguments passed to the method |
| **Result** | Successful response data |
| **Error** | Error response with code and message |

---

## 1.2 stdio (Standard I/O)

### What is it?

Every program has 3 default I/O channels:

```
stdin  (standard input)  → Where the program reads input from
stdout (standard output) → Where the program writes output to  
stderr (standard error)  → Where the program writes error/debug messages
```

### How MCP uses it

When Claude/Cursor starts your MCP server, it runs:
```
python.exe server.py
```

Then it communicates by:
- **Writing JSON-RPC messages to stdin** → your server reads them
- **Reading JSON-RPC responses from stdout** → your server writes them
- **stderr is for logging only** — the client ignores it

```
Client (Claude/Cursor)           Your Server (server.py)
        │                                  │
        │── writes to stdin ──────────►    │ reads from stdin
        │                                  │ processes request
        │◄── reads from stdout ───────     │ writes to stdout
        │                                  │
        │   (stderr = debug logs, ignored by client)
```

### Why this matters to you

**NEVER use `print()` in an MCP server!**

`print()` writes to stdout. But stdout is the channel MCP uses for JSON-RPC responses. If you `print("debugging...")`, the client will try to parse it as JSON and crash.

```python
# ❌ BAD — breaks MCP communication
print("Processing request...")

# ✅ GOOD — writes to stderr, client ignores it
import sys
print("Processing request...", file=sys.stderr)

# ✅ BETTER — use Python logging
import logging
logging.info("Processing request...")
```

---

## 1.3 IPC (Inter-Process Communication)

### What is it?

IPC is how two separate programs talk to each other. MCP is a form of IPC.

**Your analogy from Node.js:** When you run `child_process.spawn()` in Node, the parent process can read/write to the child's stdin/stdout. That's exactly what MCP does.

```javascript
// Node.js — you've seen this pattern
const child = spawn('python', ['server.py']);
child.stdin.write(JSON.stringify(request));    // Send request
child.stdout.on('data', (data) => { ... });   // Read response
```

### MCP IPC methods (transports)

| Transport | How | When |
|---|---|---|
| **stdio** | stdin/stdout of a subprocess | Local servers (what we use) |
| **SSE** (Server-Sent Events) | HTTP connection | Remote servers |
| **Streamable HTTP** | HTTP with streaming | Newer remote option |

---

## 1.4 Decorators in Python

### What is it?

A decorator is a function that wraps another function to add behavior. You've already used them:

```python
@mcp.tool()          # This is a decorator
def hash_text():
    ...
```

### How it works

```python
# What you write:
@mcp.tool()
def hash_text(text: str) -> str:
    """Hash text."""
    return hashlib.sha256(text.encode()).hexdigest()

# What Python actually does:
def hash_text(text: str) -> str:
    """Hash text."""
    return hashlib.sha256(text.encode()).hexdigest()

hash_text = mcp.tool()(hash_text)  # Wraps your function and registers it
```

**The decorator does 3 things:**
1. Reads your function's **name** → becomes the tool name
2. Reads the **type hints** → generates the input schema
3. Reads the **docstring** → becomes the description
4. **Registers** the function in FastMCP's tool registry

### Your Express analogy

```javascript
// Express — this is similar to a decorator pattern
app.post('/hash', hashTextHandler);   // Registers handler for a route

// MCP — the decorator registers the handler
@mcp.tool()   // Registers function as a tool
def hash_text(): ...
```

---

## 1.5 Type Hints & JSON Schema

### Why MCP cares about types

The AI needs to know: *"What arguments does this tool accept? What types are they?"*

MCP auto-generates a **JSON Schema** from your Python type hints:

```python
# Your Python function:
def hash_text(text: str, algorithm: str = "sha256") -> str:

# MCP generates this JSON Schema:
{
  "type": "object",
  "properties": {
    "text": { "type": "string" },
    "algorithm": { "type": "string", "default": "sha256" }
  },
  "required": ["text"]     # "algorithm" is NOT required (has default)
}
```

### Python types → JSON Schema types

| Python Type | JSON Schema Type |
|---|---|
| `str` | `string` |
| `int` | `integer` |
| `float` | `number` |
| `bool` | `boolean` |
| `list[str]` | `array` of `string` |
| `dict` | `object` |
| `Optional[str]` | `string` (nullable) |

---

# PART 2 — MCP CORE CONCEPTS

---

## 2.1 The MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP ECOSYSTEM                        │
│                                                         │
│   HOST APPLICATION (Claude Desktop, Cursor, Antigravity)│
│   ┌─────────────────────────────────────────────────┐   │
│   │              MCP CLIENT                         │   │
│   │  (Built into the host — you don't build this)   │   │
│   │                                                 │   │
│   │  • Discovers servers from config                │   │
│   │  • Starts server processes                      │   │
│   │  • Calls tools/reads resources on behalf of AI  │   │
│   └──────────┬────────────┬────────────┬────────────┘   │
│              │            │            │                 │
│         Transport    Transport    Transport              │
│         (stdio)      (stdio)      (SSE)                 │
│              │            │            │                 │
│   ┌──────────▼──┐ ┌──────▼────┐ ┌─────▼─────┐         │
│   │ MCP SERVER  │ │ MCP SERVER│ │ MCP SERVER│         │
│   │ (your code) │ │ (another) │ │ (remote)  │         │
│   │             │ │           │ │           │         │
│   │ Tools       │ │ Tools     │ │ Tools     │         │
│   │ Resources   │ │ Resources │ │ Resources │         │
│   │ Prompts     │ │           │ │ Prompts   │         │
│   └─────────────┘ └───────────┘ └───────────┘         │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** A host can connect to **multiple MCP servers** simultaneously. Each server provides different capabilities. The AI sees ALL tools from ALL connected servers.

---

## 2.2 The 3 Primitives — Tools, Resources, Prompts

### Tools — "Do Something"

```python
@mcp.tool()
def function_name(param: str) -> str:
    """Description AI reads to decide WHEN to use this tool."""
    # Execute logic
    return "result"
```

**Key rules:**
- Can have parameters (typed)
- Can have side effects (write files, call APIs, etc.)
- AI decides when to call based on docstring
- Always return a string
- Always handle errors with try/except

**When to use:** Generating, calculating, transforming, creating, modifying anything.

---

### Resources — "Read Something"

```python
# Static resource (fixed URI, no params)
@mcp.resource("protocol://path")
def resource_name() -> str:
    """Description of what data this provides."""
    return "read-only data"

# Dynamic resource (parameterized URI)
@mcp.resource("files://{filename}")
def read_file(filename: str) -> str:
    """Read a specific file."""
    return open(filename).read()
```

**Key rules:**
- URI is required (like a URL path)
- Static resources: NO function parameters
- Dynamic resources: parameters MUST match `{placeholders}` in the URI
- Read-only — should NOT modify anything
- No side effects

**When to use:** Exposing data, config, file contents, system info, status.

---

### Prompts — "Template for a Task"

```python
@mcp.prompt()
def prompt_name(param: str) -> str:
    """Description of what task this prompt helps with."""
    return f"Generated prompt template with {param}..."
```

**Key rules:**
- Returns a string (the prompt template)
- Can have parameters
- No side effects
- The AI client presents this to the user as a starting point

**When to use:** Code review templates, debugging helpers, writing assistants.

---

### Decision Matrix

| Question | → Use |
|---|---|
| Does it *do* something? | **Tool** |
| Does it *read* data? | **Resource** |
| Does it *generate a prompt template*? | **Prompt** |
| Does it need parameters AND has side effects? | **Tool** |
| Is it read-only with a fixed URI? | **Resource** (static) |
| Is it read-only but needs a parameter? | **Resource** (dynamic with `{param}` in URI) |

---

## 2.3 The MCP Lifecycle

```
PHASE 1: INITIALIZATION
─────────────────────────────────
Client → Server:  initialize (protocol version, client capabilities)
Server → Client:  server info + server capabilities
Client → Server:  initialized (confirmation)

PHASE 2: DISCOVERY
─────────────────────────────────
Client → Server:  tools/list
Server → Client:  [{name, description, inputSchema}, ...]

Client → Server:  resources/list
Server → Client:  [{uri, name, description}, ...]

Client → Server:  prompts/list
Server → Client:  [{name, description, arguments}, ...]

PHASE 3: USAGE (repeats many times)
─────────────────────────────────
Client → Server:  tools/call {name: "hash_text", arguments: {...}}
Server → Client:  {content: [{type: "text", text: "result"}]}

Client → Server:  resources/read {uri: "system://info"}
Server → Client:  {contents: [{uri: "...", text: "data"}]}

PHASE 4: SHUTDOWN
─────────────────────────────────
Client → Server:  close connection
Server:           exits gracefully
```

---

## 2.4 How the AI Decides Which Tool to Call

This is the most important concept to understand:

```
User says: "What's the SHA256 hash of 'hello'?"
                    │
                    ▼
AI reads all tool descriptions:
  - greet: "Greet someone by name"                    ❌ Not relevant
  - generate_uuid: "Generate a UUID"                  ❌ Not relevant
  - hash_text: "Hash text using a specified algorithm" ✅ MATCH!
  - format_json: "Format JSON string"                 ❌ Not relevant
                    │
                    ▼
AI constructs the call:
  hash_text(text="hello", algorithm="sha256")
                    │
                    ▼
Your function runs → returns result
                    │
                    ▼
AI presents result to user
```

**This is why docstrings are critical.** Bad docstring = AI can't find your tool. Good docstring = AI uses it perfectly.

### Writing Good Docstrings

```python
# ❌ BAD — too vague, AI won't know when to use it
@mcp.tool()
def process(data: str) -> str:
    """Process data."""

# ❌ BAD — describes implementation, not purpose
@mcp.tool()
def hash_text(text: str) -> str:
    """Uses hashlib to create a hex digest."""

# ✅ GOOD — clearly states WHAT it does and WHEN to use it
@mcp.tool()
def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Hash text using a specified algorithm.

    Useful for generating checksums, verifying data integrity,
    or creating content-based identifiers.

    Args:
        text: The text to hash
        algorithm: Hash algorithm to use (md5, sha1, sha256, sha512)
    """
```

---

# PART 3 — ESSENTIAL PATTERNS

---

## 3.1 Error Handling Pattern

**Never let exceptions crash your server.** Return error messages the AI can read.

```python
@mcp.tool()
def risky_tool(data: str) -> str:
    """Do something that might fail."""
    try:
        result = do_something(data)
        return f"✅ Success: {result}"
    except SpecificError as e:
        return f"❌ Specific error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
```

**Why:** If your tool throws an unhandled exception, the AI gets a generic error and can't help the user. If you return a descriptive error string, the AI can understand what went wrong and suggest fixes.

---

## 3.2 Async Tools Pattern

For tools that call external APIs or do I/O:

```python
import httpx

@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            return f"Status: {response.status_code}\n{response.text[:1000]}"
        except httpx.TimeoutException:
            return "❌ Request timed out"
        except Exception as e:
            return f"❌ Error: {str(e)}"
```

**Key:** Use `async def` instead of `def`. FastMCP handles the event loop.

---

## 3.3 Environment Variables Pattern

**Never hardcode secrets. Use env vars.**

```python
import os

@mcp.tool()
async def call_api(query: str) -> str:
    """Call an API that needs an API key."""
    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        return "❌ MY_API_KEY not set. Add it to your .env file."

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/search",
            headers={"Authorization": f"Bearer {api_key}"},
            params={"q": query}
        )
        return response.text
```

---

## 3.4 Input Validation Pattern

Don't trust the AI to always send valid input:

```python
@mcp.tool()
def read_file(filepath: str) -> str:
    """Read a file from the allowed directory."""
    # Security: prevent path traversal attacks
    import os
    allowed_dir = os.path.abspath("/safe/directory")
    full_path = os.path.abspath(filepath)

    if not full_path.startswith(allowed_dir):
        return "❌ Access denied: path outside allowed directory"

    if not os.path.exists(full_path):
        return f"❌ File not found: {filepath}"

    with open(full_path, 'r') as f:
        return f.read()
```

---

## 3.5 Dynamic Resources Pattern

For resources where the URI contains a variable:

```python
# The {filename} in the URI MUST match the function parameter name
@mcp.resource("files://{filename}")
def read_project_file(filename: str) -> str:
    """Read a file from the project directory."""
    safe_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(safe_dir, filename)

    if not os.path.exists(filepath):
        return f"File not found: {filename}"

    with open(filepath, 'r') as f:
        return f.read()
```

**The rule that tripped you up:**
```python
# ❌ WRONG — URI has no params, function has params
@mcp.resource("system://files")
def list_files(directory: str) -> str:

# ✅ RIGHT — no params at all
@mcp.resource("system://files")
def list_files() -> str:

# ✅ RIGHT — param is in the URI
@mcp.resource("files://{directory}")
def list_files(directory: str) -> str:
```

---

# PART 4 — ADVANCED CONCEPTS

---

## 4.1 SSE Transport (Remote MCP Servers)

Run your MCP server as a web service that anyone can connect to:

```python
# Configure host/port on settings, then run
mcp.settings.host = "0.0.0.0"   # Allow network access
mcp.settings.port = 8000        # Choose port

if __name__ == "__main__":
    mcp.run(transport="sse")
```

> **Note:** `host` and `port` are set on `mcp.settings`, NOT passed as args to `mcp.run()`. This is a common gotcha!

**Client config for SSE:**
```json
{
  "mcpServers": {
    "remote-toolkit": {
      "url": "http://your-server:8000/sse"
    }
  }
}
```

---

## 4.2 Context Object

Access MCP's context inside your tools for advanced features:

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def smart_tool(query: str, ctx: Context) -> str:
    """A tool that uses MCP context features."""
    # Report progress to the client
    await ctx.report_progress(0.5, "Halfway done...")

    # Log messages (visible to client)
    await ctx.info("Processing query...")
    await ctx.warning("This might take a while")

    # Read a resource from within a tool
    data = await ctx.read_resource("system://info")

    return f"Done processing: {query}"
```

---

## 4.3 MCP + LangChain Integration

Use MCP servers as tools in LangChain agents:

```python
from langchain_mcp import MCPToolkit

# Connect to your MCP server
toolkit = MCPToolkit(server_params={"command": "python", "args": ["server.py"]})

# Get tools as LangChain tools
tools = toolkit.get_tools()

# Use in a LangChain agent
from langchain.agents import create_openai_tools_agent
agent = create_openai_tools_agent(llm, tools, prompt)
```

---

## 4.4 Multi-Server Architecture

In production, you typically run multiple specialized MCP servers:

```json
{
  "mcpServers": {
    "dev-tools": {
      "command": "python",
      "args": ["dev_toolkit/server.py"]
    },
    "database": {
      "command": "python",
      "args": ["db_server/server.py"]
    },
    "github": {
      "command": "python",
      "args": ["github_server/server.py"]
    }
  }
}
```

**The AI sees all tools from all servers combined** and picks the right one.

---

# PART 5 — DEBUGGING & COMMON MISTAKES

---

## 5.1 Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `spawn uv ENOENT` | `uv` not installed, Inspector defaulting to it | Change Inspector command to your Python path |
| `Mismatch between URI parameters and function parameters` | Resource URI has no `{param}` but function has params | Remove function params OR add `{param}` to URI |
| `timed out after 10 seconds` | Subprocess or API call too slow | Increase timeout or use a Python library instead |
| `print()` breaks the server | `print()` writes to stdout, corrupting MCP | Use `logging` or `print(..., file=sys.stderr)` |
| Tool not appearing in client | Server didn't restart | Restart the MCP server and client |
| `ModuleNotFoundError` | Wrong Python/venv being used | Check that the correct venv Python is in the config |

## 5.2 Debugging Checklist

```
1. ✅ Is venv activated?
2. ✅ Is mcp[cli] installed in the venv?
3. ✅ Does `python server.py` run without errors?
4. ✅ Are there any syntax errors? (Run: python -c "import server")
5. ✅ Did you use print() anywhere? (Remove it!)
6. ✅ Are all Resource URIs matching function params?
7. ✅ Did you restart the server after code changes?
8. ✅ Is the client config pointing to the correct Python path?
```

---

# PART 6 — GLOSSARY

| Term | Definition |
|---|---|
| **MCP** | Model Context Protocol — standard for AI ↔ tool communication |
| **JSON-RPC** | JSON-based remote procedure call protocol — how MCP messages are formatted |
| **stdio** | Standard I/O (stdin/stdout) — how local MCP servers communicate |
| **SSE** | Server-Sent Events — how remote MCP servers communicate |
| **FastMCP** | High-level Python API for building MCP servers (decorator-based) |
| **Transport** | The communication channel (stdio or SSE) |
| **Tool** | A function the AI can call (has side effects) |
| **Resource** | Read-only data the AI can access (no side effects) |
| **Prompt** | A reusable text template for common tasks |
| **URI** | Uniform Resource Identifier — the "address" of a Resource |
| **Schema** | JSON description of a tool's parameters (auto-generated from type hints) |
| **Host** | The application running the MCP client (Claude, Cursor, Antigravity) |
| **Client** | The MCP component inside the host that talks to servers |
| **Server** | Your code that exposes tools/resources/prompts |
| **Inspector** | Browser-based testing tool (`mcp dev server.py`) |
| **Context** | Object available in tools for progress reporting and logging |
| **IPC** | Inter-Process Communication — how separate programs talk to each other |
