# 🛠️ Phase 2 — MCP Resources & Prompts

> **Goal:** Learn the other two MCP primitives — Resources (read-only data) and Prompts (reusable templates).
> **What you'll build:** Add Resources and Prompts to your existing DevToolkit server.
> **Time:** ~30 minutes

---

## 🧠 Before We Start — The 3 MCP Primitives

You already know Tools. Now let's learn the other two:

```
MCP Server Can Expose 3 Things:
─────────────────────────────────────────────────────────────
TOOLS       →  Functions AI can CALL    →  POST /endpoint
RESOURCES   →  Data AI can READ         →  GET /endpoint
PROMPTS     →  Templates AI can USE     →  Pre-built request templates
─────────────────────────────────────────────────────────────
             You built this ✅           You'll learn these now 👇
```

| Primitive | Analogy (Express) | AI's Perspective |
|---|---|---|
| **Tool** | `app.post("/action")` | "I can *do* something" |
| **Resource** | `app.get("/data")` | "I can *read* something" |
| **Prompt** | Pre-built API request body | "I have a *template* for this task" |

---

# STEP 1 — Understanding Resources

## 🎯 Why Resources?

Tools *do* things (generate, calculate, convert). But sometimes the AI just needs to *read* data — your app config, project structure, environment info, etc.

**Resources are read-only.** The AI can read them but can't change anything.

**When to use Resources vs Tools:**

| Use Case | Use Resource or Tool? |
|---|---|
| Read system info | ✅ Resource |
| Read config file | ✅ Resource |
| List project files | ✅ Resource |
| Generate a UUID | ✅ Tool (creates something) |
| Hash some text | ✅ Tool (processes something) |
| Write to a file | ✅ Tool (changes something) |

**Rule of thumb:** If it's **read-only** → Resource. If it **does something** → Tool.

---

# STEP 2 — Add Resources to Your Server

## ▶️ Code — Add These to `server.py`

Open your `server.py` and add these **after your tool definitions**, but **before** the `if __name__` block:

### Resource 1: System Information

```python
import platform  # Add this at the top with other imports
import os        # Add this at the top (if not already there)

# ============================================================
# RESOURCE 1: System Information
# ============================================================
# @mcp.resource() takes a URI pattern — this is how the AI
# identifies and requests this resource.
# Think of it like a GET endpoint URL.

@mcp.resource("system://info")
def get_system_info() -> str:
    """Current system information including OS, Python version, and machine details."""
    return f"""💻 System Information:
- OS: {platform.system()} {platform.release()}
- OS Version: {platform.version()}
- Machine: {platform.machine()}
- Processor: {platform.processor()}
- Python Version: {platform.python_version()}
- Hostname: {platform.node()}"""
```

> **Notice:** The URI `"system://info"` is like a route path. The AI uses this to request data.
> Unlike Tools, Resources have **no parameters** (they're like GET endpoints with no query params).

### Resource 2: Environment Variables (Safe Subset)

```python
@mcp.resource("system://env")
def get_environment() -> str:
    """Safe environment information (non-sensitive variables only)."""
    safe_vars = ["USERNAME", "COMPUTERNAME", "OS", "PROCESSOR_ARCHITECTURE",
                 "NUMBER_OF_PROCESSORS", "HOMEPATH", "TEMP"]
    env_info = []
    for var in safe_vars:
        value = os.environ.get(var, "Not set")
        env_info.append(f"- {var}: {value}")
    return "🔒 Environment Variables (safe subset):\n" + "\n".join(env_info)
```

> **Security note:** We only expose safe, non-sensitive env vars. Never expose API keys, tokens, or passwords through Resources!

### Resource 3: Project Structure

```python
@mcp.resource("project://structure")
def get_project_structure() -> str:
    """Current project directory structure."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    structure = []

    for root, dirs, files in os.walk(project_dir):
        # Skip venv and __pycache__
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
        level = root.replace(project_dir, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        structure.append(f"{indent}📁 {folder_name}/")
        sub_indent = '  ' * (level + 1)
        for file in files:
            size = os.path.getsize(os.path.join(root, file))
            structure.append(f"{sub_indent}📄 {file} ({size:,} bytes)")

    return "\n".join(structure)
```

### Resource 4: Python Packages

```python
@mcp.resource("system://packages")
def get_installed_packages() -> str:
    """List of installed Python packages in the current environment."""
    try:
        # Using importlib.metadata instead of subprocess — it's instant, no timeout risk
        from importlib.metadata import distributions
        packages = sorted(
            [(d.metadata["Name"], d.metadata["Version"]) for d in distributions()],
            key=lambda x: x[0].lower()
        )
        lines = [f"  {name:30s} {version}" for name, version in packages]
        header = f"📦 Installed Python Packages ({len(packages)} total):\n"
        return header + "\n".join(lines)
    except Exception as e:
        return f"❌ Could not list packages: {str(e)}"
```

> **Why not `subprocess.run(["pip", "list"])`?** We tried that first, but it **timed out** on Windows because `pip list` can be slow. Using `importlib.metadata` reads package info **directly from memory** — instant, no subprocess, no timeout. **Lesson: avoid subprocesses in MCP tools when a Python library can do the job.**

---

## ▶️ Test — Run This Now

```powershell
# Stop the old server (Ctrl+C if running), then:
mcp dev server.py
```

In the MCP Inspector:
1. Click **"Connect"** (use python.exe path as before)
2. Click the **"Resources"** tab (not Tools!)
3. You should see your 4 resources listed
4. Click any resource → click **"Read Resource"**
5. See the data returned!

---

## 🔑 Key Takeaway — Resources
> Resources expose **read-only data** via a URI. No parameters, no side effects. The AI reads them like visiting a URL. Use `@mcp.resource("protocol://path")` to register.

---

# STEP 3 — Understanding Prompts

## 🎯 Why Prompts?

Prompts are **reusable templates** that help users (or AIs) accomplish specific tasks. Think of them as pre-built "recipes" for common workflows.

**Example:** Instead of the user typing a long prompt for code review every time, you provide a `code_review` prompt template that structures the request perfectly.

---

# STEP 4 — Add Prompts to Your Server

### Prompt 1: Code Review

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base  # Needed for prompt messages

# ============================================================
# PROMPT 1: Code Review Template
# ============================================================
# Prompts return a list of messages (like a pre-built chat conversation)
# The AI client shows these to the user as a starting point

@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a thorough code review prompt.

    Args:
        code: The code to review
        language: Programming language (default: python)
    """
    return f"""Please review the following {language} code thoroughly.

Check for:
1. 🐛 Bugs and logic errors
2. 🔒 Security vulnerabilities
3. ⚡ Performance issues
4. 📖 Code readability and naming
5. 🏗️ Architecture and design patterns
6. ✅ Edge cases and error handling

Code to review:
```{language}
{code}
```

Provide specific suggestions with corrected code examples."""
```

### Prompt 2: Explain Code

```python
@mcp.prompt()
def explain_code(code: str, audience: str = "intermediate") -> str:
    """Generate a prompt to explain code clearly.

    Args:
        code: The code to explain
        audience: Target audience level - beginner, intermediate, or expert
    """
    return f"""Explain the following code for a {audience}-level developer.

Break down:
1. What the code does (high-level purpose)
2. How it works (step by step)
3. Key concepts used
4. Any important patterns or techniques

Code:
```
{code}
```

Use simple language and analogies where helpful."""
```

### Prompt 3: Debug Helper

```python
@mcp.prompt()
def debug_error(error_message: str, code: str = "") -> str:
    """Generate a debugging prompt for an error.

    Args:
        error_message: The error message or traceback
        code: The code that caused the error (optional)
    """
    code_section = f"\n\nCode that caused the error:\n```\n{code}\n```" if code else ""

    return f"""I'm getting the following error and need help debugging it.

Error:
```
{error_message}
```{code_section}

Please:
1. Explain what this error means
2. Identify the likely cause
3. Provide the corrected code
4. Explain how to prevent this in the future"""
```

---

## ▶️ Test — Run This Now

```powershell
mcp dev server.py
```

In the MCP Inspector:
1. Click **"Prompts"** tab
2. You should see `code_review`, `explain_code`, `debug_error`
3. Click a prompt → fill in the arguments → click **"Get Prompt"**
4. See the generated prompt template!

---

## 🔑 Key Takeaway — Prompts
> Prompts are **reusable templates** registered with `@mcp.prompt()`. They return structured text that helps users start common tasks. Unlike Tools (which execute logic), Prompts just generate text templates.

---

# STEP 5 — Your Final Updated `server.py`

After adding everything, your imports at the top should look like:

```python
import uuid
import json
import base64
import hashlib
import re
import platform
import os
import subprocess
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
```

And the structure of the file should be:

```
server.py
├── Imports
├── mcp = FastMCP("DevToolkit")
├── TOOLS (8 tools — greet through regex_test)
├── RESOURCES (4 resources — system info, env, project structure, packages)
├── PROMPTS (3 prompts — code review, explain code, debug error)
└── if __name__ == "__main__": mcp.run(transport="stdio")
```

---

# STEP 6 — Commit & Push

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: add MCP resources (system info) and prompts (code review, debug)"
git push origin main
```

---

# 📋 Phase 2 Revision Sheet

## Resources vs Tools vs Prompts

```
                ┌─────────────────────────────────────────┐
                │           MCP Server                    │
                │                                         │
                │  TOOLS       →  "Do something"          │
                │  @mcp.tool()    (generate, hash, calc)  │
                │                                         │
                │  RESOURCES   →  "Read something"        │
                │  @mcp.resource()  (system info, config)  │
                │                                         │
                │  PROMPTS     →  "Template for a task"   │
                │  @mcp.prompt()   (code review, debug)   │
                └─────────────────────────────────────────┘
```

## Pattern Comparison

```python
# TOOL — has params, does work, returns result
@mcp.tool()
def tool_name(param: str) -> str:
    """Description."""
    return do_something(param)

# RESOURCE — has URI, reads data, returns data
@mcp.resource("protocol://path")
def resource_name() -> str:
    """Description."""
    return read_something()

# PROMPT — has params, returns a template string
@mcp.prompt()
def prompt_name(param: str) -> str:
    """Description."""
    return f"Template with {param}..."
```

## Express Analogy

| Express | MCP | Example |
|---|---|---|
| `app.post("/action", handler)` | `@mcp.tool()` | Hash text, generate UUID |
| `app.get("/data", handler)` | `@mcp.resource("uri")` | Read system info |
| Template/Middleware | `@mcp.prompt()` | Code review template |

## What You Learned in Phase 2

| Concept | Key Point |
|---|---|
| Resources | Read-only data exposed via URI, no parameters |
| Prompts | Reusable text templates with parameters |
| Security | Never expose sensitive env vars in resources |
| URI patterns | `"protocol://path"` format for resources |
| All 3 primitives | Tools=DO, Resources=READ, Prompts=TEMPLATE |
