# 🏗️ MCP Server Architecture

> How the DevToolkit MCP Server works under the hood.

---

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        MCP CLIENT                            │
│        (Antigravity / Cursor / Claude Desktop)               │
│                                                              │
│  1. User asks: "Generate a UUID for me"                      │
│  2. AI reads tool descriptions → picks generate_uuid         │
│  3. Sends JSON-RPC call via stdin ──────────────┐            │
│  4. Receives result via stdout ◄────────────────┤            │
└─────────────────────────────────────────────────┤────────────┘
                                                  │
                                          stdio (stdin/stdout)
                                                  │
┌─────────────────────────────────────────────────┤────────────┐
│                     MCP SERVER                  │            │
│                 (server.py — Python)             │            │
│                                                  ▼            │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              FastMCP("DevToolkit")                    │    │
│  │                                                      │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐   │    │
│  │  │   greet()   │ │generate_uuid│ │ format_json()│   │    │
│  │  └─────────────┘ └─────────────┘ └──────────────┘   │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐   │    │
│  │  │base64_encode│ │base64_decode│ │  hash_text() │   │    │
│  │  └─────────────┘ └─────────────┘ └──────────────┘   │    │
│  │  ┌─────────────┐ ┌─────────────┐                    │    │
│  │  │ word_count()│ │timestamp    │ ┌──────────────┐   │    │
│  │  └─────────────┘ │_convert()   │ │ regex_test() │   │    │
│  │                  └─────────────┘ └──────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## How MCP Protocol Works

### Communication Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as MCP Client (AI)
    participant Server as MCP Server (Python)

    Note over Client,Server: Connection Phase
    Client->>Server: initialize (protocol version, capabilities)
    Server-->>Client: server info + capabilities

    Note over Client,Server: Discovery Phase
    Client->>Server: tools/list
    Server-->>Client: [greet, generate_uuid, format_json, ...]

    Note over Client,Server: Usage Phase
    User->>Client: "Hash the word hello with SHA256"
    Client->>Client: AI decides: hash_text is the right tool
    Client->>Server: tools/call {name: "hash_text", args: {text: "hello", algorithm: "sha256"}}
    Server->>Server: Execute hash_text("hello", "sha256")
    Server-->>Client: {result: "Algorithm: sha256\nHash: 2cf24d..."}
    Client-->>User: "The SHA256 hash of 'hello' is 2cf24d..."
```

### Protocol: JSON-RPC 2.0

MCP uses JSON-RPC 2.0 over stdio. Every message is a JSON object:

**Client → Server (tool call):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "hash_text",
    "arguments": {
      "text": "hello",
      "algorithm": "sha256"
    }
  },
  "id": 1
}
```

**Server → Client (response):**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{
      "type": "text",
      "text": "Algorithm: sha256\nHash: 2cf24dba..."
    }]
  },
  "id": 1
}
```

---

## Transport Layer: stdio

```
MCP Client (AI IDE)
    │
    │  Spawns subprocess:
    │  python.exe server.py
    │
    ├──stdin──►  JSON-RPC requests
    │
    ◄──stdout──  JSON-RPC responses
    │
    (stderr is for logging only — never read by client)
```

**Why stdio?**
- No ports, no HTTP, no network — just process I/O
- Secure — server runs locally, no external access
- Simple — client starts the server, communicates directly
- Fast — no network overhead

**Alternative:** SSE (Server-Sent Events) transport for remote/HTTP servers.

---

## Tool Registration: How @mcp.tool() Works

```
Your Code                          What MCP Generates
──────────────                     ──────────────────

@mcp.tool()                        Tool Schema:
def hash_text(                     {
    text: str,            ───►       "name": "hash_text",
    algorithm: str = "sha256"        "description": "Hash text using...",
) -> str:                            "inputSchema": {
    """Hash text using a               "type": "object",
    specified algorithm."""            "properties": {
    ...                                  "text": {"type": "string"},
                                         "algorithm": {
                                           "type": "string",
                                           "default": "sha256"
                                         }
                                       },
                                       "required": ["text"]
                                     }
                                   }
```

**FastMCP auto-generates the tool schema from:**
1. **Function name** → `tool.name`
2. **Docstring** → `tool.description` (AI reads this to decide when to use it)
3. **Type hints** → `inputSchema.properties` (types become JSON Schema types)
4. **Default values** → `inputSchema.properties[x].default` + removed from `required`

---

## File Structure

```
mcp-server/
├── server.py              # All tools defined here (single-file for simplicity)
├── TUTORIAL.md            # Step-by-step build guide
├── MCP_LEARNING_NOTES.md  # Concept explanations & analogies
└── venv/                  # Python virtual environment (not in git)
```

### Why Single File?

For a utility toolkit, one file is the right choice:
- Each tool is independent (no shared state)
- Easy to read, easy to add new tools
- No over-engineering for a simple server

**When to split into multiple files:**
- Tools share state or services (e.g., database connections)
- Server has 20+ tools
- Tools need async external API calls with shared clients
- You add Resources or Prompts alongside Tools

---

## Adding a New Tool: Checklist

```python
# 1. Import any needed library (at top of file)
import some_library

# 2. Add the tool (before the if __name__ block)
@mcp.tool()
def my_new_tool(param1: str, param2: int = 10) -> str:
    """Clear description of what this tool does.   ← AI reads this!

    Args:
        param1: What this parameter is for
        param2: What this parameter is for (default: 10)
    """
    try:
        result = some_library.do_something(param1, param2)
        return f"Result: {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"        ← Always handle errors!

# 3. Test with: mcp dev server.py
# 4. Commit and push
```

---

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | FastMCP (not low-level SDK) | Simpler, decorator-based, less boilerplate |
| Transport | stdio (not SSE) | Local server, no network needed |
| Architecture | Single file | Tools are independent, keep it simple |
| Error handling | Return error strings | Don't crash — AI can read errors and retry |
| Output format | Formatted strings with emojis | Human-readable, AI can parse it too |
| No external APIs | All tools use Python stdlib | No API keys, no rate limits, works offline |
