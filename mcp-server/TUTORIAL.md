# 🛠️ Build Your First MCP Server — Step-by-Step Tutorial

> **Goal:** By the end of this tutorial, you'll understand how MCP works and be able to build a server from scratch.
> **Time:** ~45 minutes
> **Prerequisites:** Python 3.10+ installed

---

## 🧠 Before We Start — What is MCP?

**MCP (Model Context Protocol)** is a protocol that lets AI models (like Claude) use **your custom tools**.

Think of it like this — you already know REST APIs:

```
REST API World                          MCP World
──────────────────────────────────     ──────────────────────────────────
You build an Express server            You build an MCP server
With routes like POST /hash            With tools like hash_text()
Postman calls your API                 Claude/Cursor calls your tools
You return JSON                        You return a string result
```

**The key difference:** In REST, a *human* decides which endpoint to call. In MCP, the **AI decides** which tool to call based on the tool's description.

That's why **docstrings matter so much** in MCP — they're like API documentation that the AI reads to decide what to do.

---

# STEP 1 — Set Up the Project Environment

## 🎯 Why This Step?

Every Python project needs an **isolated environment** so dependencies don't clash with other projects. This is exactly like how `node_modules` works in Node.js — but Python's approach uses a "virtual environment" folder.

## 📌 What You'll Learn
- Creating Python virtual environments
- Activating environments on Windows
- Installing packages with `pip`

## ▶️ Commands — Run These Now

Open your terminal and run each command one at a time:

```powershell
# 1. Navigate to the project directory
cd "d:\My Projects\AI Engineering\ai-dev-toolkit\mcp-server"
```

```powershell
# 2. Create a virtual environment called "venv"
python -m venv venv
```

> **What this does:** Creates a `venv/` folder containing a copy of Python and an empty `pip`. All packages you install will go here, not globally.
>
> **JS Analogy:** Like running `npm init` — it creates a local space for your project's dependencies.

```powershell
# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

> **What this does:** Tells your terminal "use Python and pip from THIS folder, not the global one."
>
> **How to verify:** You should see `(venv)` at the start of your terminal prompt. If you see it, it's working!

> [!WARNING]
> **Common Mistake:** If you get a "running scripts is disabled" error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

```powershell
# 4. Install the MCP SDK
pip install "mcp[cli]"
```

> **What this does:** Installs:
> - `mcp` — the core SDK for building MCP servers
> - `FastMCP` — the high-level decorator API (like FastAPI, but for MCP)
> - CLI tools — `mcp dev` for testing your server in a browser
>
> **JS Analogy:** Like `npm install express` — installs the framework you'll build on.

## ✅ Verify It Worked

```powershell
python -c "from mcp.server.fastmcp import FastMCP; print('MCP SDK installed successfully!')"
```

If you see `MCP SDK installed successfully!`, you're good!

## 🔑 Key Takeaway
> A virtual environment isolates your project's packages. Always create one per project. Activate it before installing or running anything.

---

# STEP 2 — Create the Simplest Possible MCP Server

## 🎯 Why This Step?

Before building 8 tools, let's understand the **absolute minimum** code needed for an MCP server. We'll build a server with just **1 tool** first.

## 📌 What You'll Learn
- `FastMCP` — the server class
- `@mcp.tool()` — the decorator that registers tools
- Type hints — how MCP auto-generates schemas
- Docstrings — how the AI knows what your tool does

## ▶️ Code — Delete `server.py` and Create It Fresh

Delete the existing `server.py` (we'll rebuild from scratch). Create a new `server.py` with just this:

```python
# server.py — The simplest MCP server possible

from mcp.server.fastmcp import FastMCP

# Step A: Create the server instance
# This is like: const app = express()
# The name "DevToolkit" shows up when clients connect
mcp = FastMCP("DevToolkit")


# Step B: Register a tool
# @mcp.tool() is like @app.post("/greet") in FastAPI
@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The person's name to greet
    """
    return f"Hello, {name}! Welcome to MCP! 🎉"


# Step C: Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## 🔍 Line-by-Line Breakdown

| Line | What It Does | JS Equivalent |
|---|---|---|
| `from mcp.server.fastmcp import FastMCP` | Import the framework | `const express = require('express')` |
| `mcp = FastMCP("DevToolkit")` | Create server instance | `const app = express()` |
| `@mcp.tool()` | Register this function as a tool | `app.post('/greet', handler)` |
| `def greet(name: str) -> str:` | Function with typed params | TypeScript: `(name: string): string` |
| `"""Greet someone..."""` | Docstring = tool description | Swagger/OpenAPI description |
| `mcp.run(transport="stdio")` | Start the server | `app.listen(3000)` |

### Why `transport="stdio"`?

MCP supports two transports:
- **stdio** — communicates via stdin/stdout (for local tools — Claude Desktop, Cursor)
- **sse** — communicates via HTTP/SSE (for remote servers)

We use `stdio` because we're running locally. The AI client starts your Python script as a subprocess and talks to it through stdin/stdout.

### Why Do Docstrings Matter?

When Claude connects to your server, it reads:
1. **Function name** → `greet`
2. **Parameters + types** → `name: str`
3. **Docstring** → "Greet someone by name"

The AI uses this info to decide: *"Should I call this tool right now?"*

**Bad docstring = AI won't know when to use your tool.**

## ▶️ Test It — Run This Now

```powershell
# Make sure you're in mcp-server/ with venv activated
mcp dev server.py
```

> **What this does:** Launches the **MCP Inspector** — a browser-based testing UI.
> It'll open a page (usually http://localhost:6274) where you can:
> 1. See your registered tools
> 2. Call them with test arguments
> 3. See the responses

### In the Inspector:
1. Click **"Connect"** (top left)
2. Click **"Tools"** tab
3. You should see `greet` listed
4. Click on it → enter a name → click **"Run Tool"**
5. You should see: `Hello, [name]! Welcome to MCP! 🎉`

> [!WARNING]
> **Common Mistake:** If `mcp dev` command is not found, make sure your venv is activated. Run `.\venv\Scripts\Activate.ps1` first.

**Press `Ctrl+C` in the terminal to stop the server when done testing.**

## 🔑 Key Takeaway
> An MCP server is just: **create instance → register tools → run**. The AI reads your function names, type hints, and docstrings to know what tools are available and when to use them.

---

# STEP 3 — Add Real Tools (One at a Time)

## 🎯 Why This Step?

Now that you understand the pattern, let's add real, useful tools. We'll add them **one at a time** so you see the pattern clearly.

## 📌 What You'll Learn
- Adding multiple tools to one server
- Using Python standard libraries
- Error handling in tools
- Default parameters

## ▶️ Code — Add These Tools to `server.py`

Keep the `greet` tool and add these below it (before the `if __name__` block):

### Tool 1: Generate UUID

```python
import uuid  # Add this at the top of the file with other imports

@mcp.tool()
def generate_uuid() -> str:
    """Generate a random UUID (Universally Unique Identifier).

    Use this when you need to create a unique identifier,
    for example for database records, session tokens, or tracking IDs.
    """
    return str(uuid.uuid4())
```

> **Why this tool?** Generating UUIDs is a common dev task. Notice: **no parameters** — a tool can have zero args.

### Tool 2: Format JSON

```python
import json  # Add this at the top

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
```

> **What's new here?** **Error handling.** When the AI sends invalid JSON, we return a friendly error instead of crashing. Always handle errors gracefully in MCP tools — the AI will read the error message and may try again.

### Tool 3: Base64 Encode & Decode

```python
import base64  # Add this at the top

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
```

> **Pattern so far:** Every tool follows the exact same pattern:
> 1. `@mcp.tool()` decorator
> 2. Function with type hints
> 3. Docstring describing what it does
> 4. Try/except for error handling
> 5. Return a string result

### Tool 4: Hash Text (with default parameter)

```python
import hashlib  # Add this at the top

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
```

> **What's new?** **Default parameters.** `algorithm="sha256"` means the AI can call `hash_text("hello")` without specifying the algorithm. MCP handles defaults automatically — just like Express route parameters.

## ▶️ Test — Run This Now

```powershell
mcp dev server.py
```

In the Inspector, you should now see **5 tools** (greet + 4 new ones). Test each one!

**Test suggestions:**
- `generate_uuid` → just click run (no args needed)
- `format_json` → try `{"name":"test","age":25}` and also try `{broken json`
- `base64_encode` → try `Hello World`
- `hash_text` → try text=`password123`, algorithm=`md5`

**Press `Ctrl+C` when done.**

## 🔑 Key Takeaway
> Every MCP tool is the same pattern: **decorator → typed function → docstring → error handling → return string**. Default parameters work automatically. Always handle errors gracefully.

---

# STEP 4 — Add Advanced Tools

## 🎯 Why This Step?

Let's add tools that are more complex — text analysis, timestamp conversion, and regex testing. These show how tools can do real work.

## ▶️ Code — Add These to `server.py`

### Tool 5: Word Count / Text Stats

```python
import re  # Add this at the top

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
```

### Tool 6: Timestamp Converter

```python
from datetime import datetime, timezone  # Add at the top

@mcp.tool()
def timestamp_convert(value: str) -> str:
    """Convert between Unix timestamps and human-readable dates.

    - Pass a number (like "1709654400") to convert timestamp to date
    - Pass a date string (like "2024-03-05") to convert date to timestamp

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
```

> **What's interesting here?** The tool **auto-detects** the input format. If you pass a number, it converts to a date. If you pass a date, it converts to a timestamp. The AI doesn't need to know which direction — it just calls the tool.

### Tool 7: Regex Tester

```python
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
```

## ▶️ Test — Run This Now

```powershell
mcp dev server.py
```

**Test suggestions:**
- `word_count` → paste any paragraph of text
- `timestamp_convert` → try `1709654400` and also `2024-03-05`
- `regex_test` → pattern=`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`, text=`Contact us at hello@example.com or support@test.org`

## 🔑 Key Takeaway
> MCP tools can be as simple or complex as you want. The AI will figure out when to use them based on the docstring. Multiple parameters, auto-detection logic, formatted output — all work great.

---

# STEP 5 — Your Final Complete `server.py`

## 🎯 Why This Step?

Let's verify your final file has everything in the right order with all imports at the top.

## ▶️ Your Final File Should Look Like This

```python
"""
Developer Toolkit MCP Server
=============================
A simple MCP server that provides useful developer tools.
"""

import uuid
import json
import base64
import hashlib
import re
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

# Create the server
mcp = FastMCP("DevToolkit")


@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The person's name to greet
    """
    return f"Hello, {name}! Welcome to MCP! 🎉"


@mcp.tool()
def generate_uuid() -> str:
    """Generate a random UUID (Universally Unique Identifier).

    Use this when you need to create a unique identifier,
    for example for database records, session tokens, or tracking IDs.
    """
    return str(uuid.uuid4())


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


@mcp.tool()
def base64_encode(text: str) -> str:
    """Encode text to Base64 format.

    Args:
        text: The plain text to encode
    """
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    return f"Encoded: {encoded}"


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


@mcp.tool()
def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Hash text using a specified algorithm.

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


@mcp.tool()
def word_count(text: str) -> str:
    """Analyze text and return word count, character count, and line count.

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


@mcp.tool()
def timestamp_convert(value: str) -> str:
    """Convert between Unix timestamps and human-readable dates.

    - Pass a number (like "1709654400") to convert timestamp to date
    - Pass a date string (like "2024-03-05") to convert date to timestamp

    Args:
        value: Unix timestamp (number) or date string (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
    """
    try:
        ts = float(value)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return f"""⏰ Timestamp: {value}
- UTC: {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}
- ISO: {dt.isoformat()}"""
    except ValueError:
        pass
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
            return f"""📅 Date: {value}
- Timestamp: {int(dt.timestamp())}
- ISO: {dt.isoformat()}"""
        except ValueError:
            continue
    return f"❌ Could not parse: {value}. Use Unix timestamp or YYYY-MM-DD format."


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


# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## ▶️ Final Test

```powershell
mcp dev server.py
```

You should see **8 tools** in the Inspector. Test them all! 🎉

---

# STEP 6 — Connect to Claude Desktop (Optional)

## 🎯 Why This Step?

Testing with the Inspector is great for development. But the real power is when **Claude uses your tools in a real conversation**. This step connects your server to Claude Desktop.

## ▶️ Steps

### 1. Find your config file

```powershell
# This opens the folder where the config file should be
explorer "$env:APPDATA\Claude"
```

### 2. Edit (or create) `claude_desktop_config.json`

Add this content (replace the paths with your actual Python path):

```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "d:\\My Projects\\AI Engineering\\ai-dev-toolkit\\mcp-server\\venv\\Scripts\\python.exe",
      "args": ["d:\\My Projects\\AI Engineering\\ai-dev-toolkit\\mcp-server\\server.py"]
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. Look for a 🔨 (hammer) icon — that means your tools are connected!

### 4. Test It

Ask Claude: *"Generate a UUID for me"* or *"Hash the text 'hello world' with SHA256"*

Claude will call your tools and show the results! 🎉

## 🔑 Key Takeaway
> Claude Desktop reads the config file to know which MCP servers to start. It runs your Python script as a subprocess and communicates via stdin/stdout. No HTTP, no ports — just stdin/stdout.

---

# STEP 7 — Git Commit Your Work

## ▶️ Run These Now

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: add 8 developer tools to MCP server"
```

---

# 📋 REVISION CHEAT SHEET

## MCP Server Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ServerName")        # 1. Create server

@mcp.tool()                        # 2. Register tool
def tool_name(param: str) -> str:  # 3. Typed params
    """Description for AI."""      # 4. Docstring = AI reads this
    return "result"                # 5. Return string

if __name__ == "__main__":
    mcp.run(transport="stdio")     # 6. Start server
```

## Express ↔ MCP Mapping

| Express | MCP |
|---|---|
| `const app = express()` | `mcp = FastMCP("name")` |
| `app.post("/route", fn)` | `@mcp.tool() def fn()` |
| `req.body.param` | Function arguments |
| `res.json(result)` | `return "result"` |
| `app.listen(3000)` | `mcp.run(transport="stdio")` |
| Postman | `mcp dev server.py` |

## Key Commands

| Command | What It Does |
|---|---|
| `python -m venv venv` | Create virtual environment |
| `.\venv\Scripts\Activate.ps1` | Activate venv (Windows) |
| `pip install "mcp[cli]"` | Install MCP SDK |
| `mcp dev server.py` | Launch Inspector for testing |
| `Ctrl+C` | Stop the server |

## 3 Rules for Good MCP Tools

1. **Clear docstring** — The AI uses this to decide WHEN to call your tool
2. **Type hints** — MCP auto-generates the schema from your types
3. **Error handling** — Always try/except, return friendly error messages

## Common Mistakes

| Mistake | Fix |
|---|---|
| `mcp dev` not found | Activate venv first: `.\venv\Scripts\Activate.ps1` |
| Script execution disabled | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Tool not showing in Inspector | Check for syntax errors: `python server.py` |
| Claude can't connect | Check paths in `claude_desktop_config.json`, restart Claude |
| `print()` breaks stdio | Never use `print()` — use `logging` or `sys.stderr` instead |
