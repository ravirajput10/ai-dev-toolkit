# 🧠 MCP Server — Learning Notes

> These notes cover everything we're building and WHY, so you can revisit anytime.

---

## 📌 What is MCP (Model Context Protocol)?

**Analogy for you:** Think of MCP like a **REST API, but for AI models**.

| Concept | Web World (you know this) | MCP World |
|---|---|---|
| Server | Express / FastAPI server | MCP Server |
| Endpoints | `GET /users`, `POST /orders` | Tools, Resources, Prompts |
| Client | Browser, Postman, React app | Claude Desktop, Cursor, any MCP client |
| Protocol | HTTP / REST | MCP (JSON-RPC over stdio or SSE) |

**In simple terms:**
- An MCP server **exposes capabilities** (tools, resources) that an AI model can use
- The AI model (like Claude) **discovers** these tools automatically
- When the AI needs to do something (like read a file, search the web), it **calls your tool**
- You handle the logic, return the result, and the AI uses it

### The 3 Things an MCP Server Can Expose

| Type | What It Is | Analogy |
|---|---|---|
| **Tools** | Functions the AI can call | `POST` endpoints — they *do* something |
| **Resources** | Read-only data the AI can access | `GET` endpoints — they *return* data |
| **Prompts** | Pre-built prompt templates | Like pre-defined API request templates |

> For this project, we'll focus on **Tools** — they're the most useful and most common.

---

## 📌 What Are We Building?

A **"Developer Toolkit" MCP Server** with these tools:

| Tool | What It Does | Why It's Useful |
|---|---|---|
| `generate_uuid` | Generates a unique UUID | Common dev task |
| `format_json` | Prettifies/validates JSON | Devs use this daily |
| `base64_encode` | Encodes text to Base64 | API debugging |
| `base64_decode` | Decodes Base64 to text | API debugging |
| `hash_text` | Hashes text (MD5, SHA256) | Security, checksums |
| `word_count` | Counts words, chars, lines | Content/writing tasks |
| `timestamp_convert` | Converts timestamps ↔ human dates | Log analysis |
| `regex_test` | Tests a regex pattern against text | Regex debugging |

**Why this project?**
- No API keys needed (everything runs locally)
- Immediately useful — you'll actually use these tools
- Teaches all core MCP concepts (tools, type hints, docstrings)
- Simple enough to build in 30 minutes, impressive enough for your portfolio

---

## 📌 How MCP Communication Works

```
┌─────────────────┐         ┌─────────────────┐
│   MCP Client    │  stdio  │   MCP Server    │
│  (Claude, etc.) │◄───────►│  (your Python)  │
│                 │ JSON-RPC│                 │
│  1. Discovers   │────────►│  Lists tools    │
│     tools       │◄────────│  Returns list   │
│                 │         │                 │
│  2. Calls tool  │────────►│  Executes code  │
│     with args   │◄────────│  Returns result │
└─────────────────┘         └─────────────────┘
```

**Transport options:**
- **stdio** (standard I/O) — used for local servers (what we'll use)
- **SSE** (Server-Sent Events) — used for remote/HTTP servers

---

## 📌 Step-by-Step Build Guide

### STEP 1: Create Project & Virtual Environment

**What:** Set up an isolated Python environment for this project.
**Why:** Virtual environments prevent dependency conflicts between projects (like `node_modules` but for Python).

```powershell
# Navigate to the project directory
cd "d:\My Projects\AI Engineering\MCP server"

# Create a virtual environment (like a local node_modules for Python)
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# You should see (venv) at the start of your prompt
```

> **JS Analogy:** `python -m venv venv` is like `npm init` + creating a local `node_modules`. Activating it is like using `nvm use`.

---

### STEP 2: Install Dependencies

**What:** Install the MCP SDK and any libraries we need.
**Why:** `mcp[cli]` is the official Python SDK for building MCP servers. It includes `FastMCP` — the high-level, decorator-based API.

```powershell
# Install the MCP SDK (with CLI tools for testing)
pip install "mcp[cli]"
```

**What gets installed:**
- `mcp` — the core SDK
- `FastMCP` — the high-level API (like FastAPI for MCP)
- CLI tools like `mcp dev` for testing your server

---

### STEP 3: Create the Server File

**What:** Create `server.py` — our main MCP server.
**Why:** This single file defines all our tools. FastMCP uses decorators (like `@app.get()` in FastAPI).

Create a file called `server.py` and add this code:

```python
"""
Developer Toolkit MCP Server
=============================
A simple MCP server that provides useful developer tools.

Key concepts demonstrated:
- FastMCP: High-level API for building MCP servers (like FastAPI for MCP)
- @mcp.tool(): Decorator to register a function as an MCP tool
- Type hints: MCP uses these to generate tool schemas automatically
- Docstrings: MCP uses these as tool descriptions for the AI
"""

import uuid
import json
import base64
import hashlib
import re
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

# ============================================================
# INITIALIZE THE SERVER
# ============================================================
# This is like: const app = express()  in Node.js
# The name "DevToolkit" appears in the client when connecting
mcp = FastMCP("DevToolkit")


# ============================================================
# TOOL 1: Generate UUID
# ============================================================
# @mcp.tool() is like @app.post("/generate-uuid") in FastAPI
# The docstring becomes the tool description that the AI reads
# The AI uses this description to decide WHEN to call this tool

@mcp.tool()
def generate_uuid() -> str:
    """Generate a random UUID (Universally Unique Identifier).

    Use this when you need to create a unique identifier,
    for example for database records, session tokens, or tracking IDs.
    """
    return str(uuid.uuid4())


# ============================================================
# TOOL 2: Format/Validate JSON
# ============================================================
# Notice the type hint: json_string: str
# MCP automatically creates a schema from this
# The AI knows it needs to pass a string argument

@mcp.tool()
def format_json(json_string: str) -> str:
    """Format and validate a JSON string with proper indentation.

    Pass in a raw JSON string and get back a pretty-printed version.
    If the JSON is invalid, returns an error message explaining what's wrong.

    Args:
        json_string: The raw JSON string to format
    """
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {str(e)}"


# ============================================================
# TOOL 3: Base64 Encode
# ============================================================

@mcp.tool()
def base64_encode(text: str) -> str:
    """Encode text to Base64 format.

    Useful for encoding data for APIs, embedding in URLs,
    or preparing data for transmission.

    Args:
        text: The plain text to encode
    """
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    return f"Encoded: {encoded}"


# ============================================================
# TOOL 4: Base64 Decode
# ============================================================

@mcp.tool()
def base64_decode(encoded_text: str) -> str:
    """Decode a Base64 encoded string back to plain text.

    Args:
        encoded_text: The Base64 encoded string to decode
    """
    try:
        decoded = base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
        return f"Decoded: {decoded}"
    except Exception as e:
        return f"❌ Invalid Base64: {str(e)}"


# ============================================================
# TOOL 5: Hash Text
# ============================================================
# Multiple parameters with a default value — MCP handles this
# The AI can call: hash_text("hello") or hash_text("hello", "sha256")

@mcp.tool()
def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Hash text using a specified algorithm.

    Useful for generating checksums, verifying data integrity,
    or creating content-based identifiers.

    Args:
        text: The text to hash
        algorithm: Hash algorithm to use (md5, sha1, sha256, sha512). Default: sha256
    """
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    algo = algorithm.lower()
    if algo not in algorithms:
        return f"❌ Unknown algorithm: {algorithm}. Use: {', '.join(algorithms.keys())}"

    hash_value = algorithms[algo](text.encode("utf-8")).hexdigest()
    return f"Algorithm: {algo}\nHash: {hash_value}"


# ============================================================
# TOOL 6: Word Count / Text Stats
# ============================================================

@mcp.tool()
def word_count(text: str) -> str:
    """Analyze text and return word count, character count, and line count.

    Useful for content analysis, checking text length limits,
    and general text statistics.

    Args:
        text: The text to analyze
    """
    words = len(text.split())
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    lines = text.count("\n") + 1
    sentences = len(re.split(r"[.!?]+", text)) - 1

    return f"""📊 Text Statistics:
- Words: {words}
- Characters (with spaces): {characters}
- Characters (no spaces): {characters_no_spaces}
- Lines: {lines}
- Sentences: {max(sentences, 0)}"""


# ============================================================
# TOOL 7: Timestamp Converter
# ============================================================

@mcp.tool()
def timestamp_convert(value: str) -> str:
    """Convert between Unix timestamps and human-readable dates.

    - Pass a number (like "1709654400") to convert timestamp → date
    - Pass a date string (like "2024-03-05") to convert date → timestamp

    Args:
        value: Unix timestamp (number) or date string (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
    """
    # Try as Unix timestamp first
    try:
        ts = float(value)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return f"""⏰ Timestamp: {value}
- UTC: {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}
- ISO: {dt.isoformat()}"""
    except ValueError:
        pass

    # Try as date string
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
            return f"""📅 Date: {value}
- Timestamp: {int(dt.timestamp())}
- ISO: {dt.isoformat()}"""
        except ValueError:
            continue

    return f"❌ Could not parse: {value}. Use Unix timestamp or YYYY-MM-DD format."


# ============================================================
# TOOL 8: Regex Tester
# ============================================================

@mcp.tool()
def regex_test(pattern: str, text: str) -> str:
    """Test a regular expression pattern against text.

    Returns all matches found. Useful for debugging regex patterns.

    Args:
        pattern: The regex pattern to test
        text: The text to search in
    """
    try:
        matches = re.findall(pattern, text)
        if not matches:
            return f"🔍 No matches found for pattern: {pattern}"

        result = f"🔍 Pattern: {pattern}\n📝 Matches ({len(matches)}):\n"
        for i, match in enumerate(matches, 1):
            result += f"  {i}. {match}\n"
        return result
    except re.error as e:
        return f"❌ Invalid regex: {str(e)}"


# ============================================================
# RUN THE SERVER
# ============================================================
# This starts the MCP server using stdio transport
# stdio = communication via standard input/output (stdin/stdout)
# This is how Claude Desktop and other local clients connect

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

### STEP 4: Test with MCP Inspector

**What:** Use the built-in MCP Inspector to test your server in a browser UI.
**Why:** Before connecting to Claude or Cursor, we want to verify our tools work.

```powershell
# Make sure venv is activated, then run:
mcp dev server.py
```

This opens a web UI where you can:
- See all your tools listed
- Call each tool with test arguments
- See the responses

---

### STEP 5: Connect to Claude Desktop (Optional)

**What:** Register your MCP server so Claude Desktop can use your tools.
**Why:** This is the real-world use case — your tools become available inside Claude.

1. Open Claude Desktop → Settings → Developer → Edit Config
2. The config file (`claude_desktop_config.json`) location:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add your server:

```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "d:\\My Projects\\AI Engineering\\MCP server\\venv\\Scripts\\python.exe",
      "args": ["d:\\My Projects\\AI Engineering\\MCP server\\server.py"]
    }
  }
}
```

4. Restart Claude Desktop
5. You should see a 🔨 icon showing your tools are available!

---

## 📌 Key Takeaways

### What You Learned

| Concept | What It Means |
|---|---|
| `FastMCP("name")` | Creates an MCP server instance (like `express()`) |
| `@mcp.tool()` | Registers a function as a callable tool (like `@app.post()`) |
| Type hints (`str`, `float`) | MCP auto-generates the input schema from these |
| Docstrings | MCP uses these as the tool description — the AI reads this to decide when to call |
| `mcp.run(transport="stdio")` | Starts the server, communicating via stdin/stdout |
| `mcp dev server.py` | Launches the MCP Inspector for testing |

### Pattern: Every MCP Tool Follows This Structure

```python
@mcp.tool()
def tool_name(param1: str, param2: int = 10) -> str:
    """Description the AI reads to know WHEN to use this tool.

    Args:
        param1: What this parameter is for
        param2: What this parameter is for (default: 10)
    """
    # Your logic here
    return "result string"
```

### How This Maps to Your Express Knowledge

```
Express                          MCP
─────────────────────────────── ──────────────────────────────
const app = express()           mcp = FastMCP("name")
app.post("/route", handler)     @mcp.tool() def handler()
req.body.param                  Function arguments with types
res.json({ result })            return "result string"
app.listen(3000)                mcp.run(transport="stdio")
Postman (testing)               mcp dev server.py (Inspector)
```

---

## 📌 What's Next?

After completing this:
1. ✅ Add more tools (file reader, API caller, etc.)
2. ✅ Try adding **Resources** (read-only data endpoints)
3. ✅ Build a second MCP server for a different use case
4. ✅ Connect it to Cursor or another MCP client
5. ✅ Eventually → Build an **AI Agent** that calls MCP servers
