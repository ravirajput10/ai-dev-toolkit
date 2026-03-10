# ⚡ Phase 6 — Advanced MCP Patterns

> **Goal:** Learn Context object, tool composition, logging & observability, and structured error handling.
> **What you'll build:** Advanced tools that use MCP Context, call other resources, and report progress.
> **Time:** ~30 minutes

---

## 🧠 Before We Start — What Are Advanced Patterns?

So far, your tools are **independent** — each tool does one thing, returns a result, done.
In real-world MCP servers, tools need to:

1. **Report progress** — tell the AI "I'm 50% done"
2. **Log messages** — send info/warning to the client
3. **Read resources** — access data from within a tool
4. **Compose tools** — one tool uses the result of another
5. **Handle errors** — structured, consistent error responses

---

# STEP 1 — The Context Object

## What is Context?

Context (`ctx`) is an object MCP injects into your tool. It gives you access to:

| Feature | What It Does | Express Analogy |
|---|---|---|
| `ctx.info("msg")` | Log info to client | `console.log()` |
| `ctx.warning("msg")` | Log warning to client | `console.warn()` |
| `ctx.report_progress(0.5, "msg")` | Show progress bar | Custom middleware |
| `ctx.read_resource("uri")` | Read a resource from within a tool | Calling another endpoint |
| `ctx.session` | Current client session | `req.session` |
| `ctx.client_id` | Who's calling | `req.ip` |

## How to Use It

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def my_tool(query: str, ctx: Context) -> str:
    """A tool that uses context features."""

    # Log messages (visible to client)
    await ctx.info("Starting to process...")

    # Report progress (progress, total)
    await ctx.report_progress(1, 2)  # Step 1 of 2

    # Read a resource from within this tool
    data = await ctx.read_resource("system://info")

    # Send a warning if something is off
    await ctx.warning("This took longer than expected")

    return f"Done: {query}"
```

### Key Rules:
1. **Add `ctx: Context` as the LAST parameter** — MCP injects it automatically
2. **The function must be `async def`** — because ctx methods are async
3. **The AI never sees `ctx`** — it's hidden from the tool schema
4. **`ctx` is optional** — only add it if you need it

---

# STEP 2 — Build Advanced Tools

We'll create a new file: `tools/advanced_tools.py`

## ▶️ Code — Create `tools/advanced_tools.py`

```python
"""
Advanced Tools — Phase 6
=========================
Tools that demonstrate:
- Context object (logging, progress, reading resources)
- Tool composition (tools using data from resources)
- Structured error handling
"""

from app import mcp
from mcp.server.fastmcp import Context
import json


# ============================================================
# TOOL: System Health Check (Uses Context + Resources)
# ============================================================
# This tool READS RESOURCES from within a tool — tool composition
# It also uses ctx.info() and ctx.report_progress()

@mcp.tool()
async def system_health_check(ctx: Context) -> str:
    """Run a comprehensive system health check.

    Checks system info, installed packages, and environment.
    Reports progress as it goes.
    """
    results = []

    # Step 1: Get system info
    await ctx.info("Checking system information...")
    await ctx.report_progress(1, 5)
    try:
        sys_info = await ctx.read_resource("system://info")
        results.append(f"✅ System Info: Available")
    except Exception as e:
        results.append(f"❌ System Info: {str(e)}")

    # Step 2: Check environment
    await ctx.info("Checking environment variables...")
    await ctx.report_progress(2, 5)
    try:
        env_data = await ctx.read_resource("system://env")
        results.append(f"✅ Environment: Available")
    except Exception as e:
        results.append(f"❌ Environment: {str(e)}")

    # Step 3: Check packages
    await ctx.info("Checking installed packages...")
    await ctx.report_progress(3, 5)
    try:
        packages = await ctx.read_resource("system://packages")
        results.append(f"✅ Packages: Available")
    except Exception as e:
        results.append(f"⚠️ Packages: {str(e)}")

    # Step 4: Check database
    await ctx.info("Checking database...")
    await ctx.report_progress(4, 5)
    try:
        from db.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM notes")
        count = cursor.fetchone()[0]
        conn.close()
        results.append(f"✅ Database: {count} notes stored")
    except Exception as e:
        results.append(f"❌ Database: {str(e)}")

    # Done
    await ctx.report_progress(5, 5)
    await ctx.info("Health check finished!")

    return "🏥 System Health Report\n" + "=" * 30 + "\n" + "\n".join(results)


# ============================================================
# TOOL: Smart Note Search (Uses Context + DB)
# ============================================================
# Demonstrates: Context logging + database interaction + 
# structured results

@mcp.tool()
async def smart_note_search(query: str, ctx: Context) -> str:
    """Search notes with detailed logging and progress.

    Searches both title and content, provides match statistics.

    Args:
        query: Search term to look for in note titles and content
    """
    await ctx.info(f"Searching notes for: '{query}'")

    try:
        from db.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()

        # Search in both title and content
        cursor.execute(
            "SELECT id, title, content, created_at FROM notes WHERE title LIKE ? OR content LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        results = cursor.fetchall()

        # Get total count for context
        cursor.execute("SELECT COUNT(*) FROM notes")
        total = cursor.fetchone()[0]
        conn.close()

        if not results:
            await ctx.warning(f"No notes found matching '{query}'")
            return f"🔍 No notes found matching '{query}' (searched {total} notes)"

        await ctx.info(f"Found {len(results)} matching notes out of {total} total")

        output = f"🔍 Search Results for '{query}'\n"
        output += f"Found {len(results)} of {total} notes\n"
        output += "=" * 40 + "\n"

        for note_id, title, content, created_at in results:
            output += f"\n📝 [{note_id}] {title}\n"
            output += f"   {content[:100]}{'...' if len(content) > 100 else ''}\n"
            output += f"   📅 Created: {created_at}\n"

        return output

    except Exception as e:
        await ctx.warning(f"Search error: {str(e)}")
        return f"❌ Search failed: {str(e)}"


# ============================================================
# TOOL: Bulk Note Creator (Uses Context for Progress)
# ============================================================
# Demonstrates: Progress reporting for batch operations

@mcp.tool()
async def bulk_create_notes(notes_json: str, ctx: Context) -> str:
    """Create multiple notes at once from a JSON array.

    Pass a JSON array of objects with 'title' and 'content' fields.
    Reports progress as each note is created.

    Args:
        notes_json: JSON array like [{"title": "...", "content": "..."}, ...]
    """
    try:
        notes = json.loads(notes_json)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {str(e)}"

    if not isinstance(notes, list):
        return "❌ Expected a JSON array of notes"

    if len(notes) == 0:
        return "❌ Empty array — no notes to create"

    await ctx.info(f"Creating {len(notes)} notes...")
    created = []

    from db.database import get_connection

    for i, note in enumerate(notes):
        title = note.get("title", "")
        content = note.get("content", "")

        if not title or not content:
            await ctx.warning(f"Skipping note {i+1}: missing title or content")
            continue

        await ctx.info(f"Creating note {i+1}/{len(notes)}")
        await ctx.report_progress(i + 1, len(notes))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (title, content)
            )
            conn.commit()
            created.append(f"✅ [{cursor.lastrowid}] {title}")
            conn.close()
        except Exception as e:
            created.append(f"❌ {title}: {str(e)}")

    await ctx.info(f"Done! Created {len(created)} notes")

    return f"📦 Bulk Create Report\n{'=' * 30}\n" + "\n".join(created)
```

---

# STEP 3 — Register the New Tools

Update `server.py` to import the new module.

Add this line after the other tool imports:
```python
from tools import advanced_tools  # 3 advanced tools (Phase 6)
```

---

# STEP 4 — Test in Inspector

```powershell
mcp dev server.py
```

### Test Data

| Tool | Arguments | What to Look For |
|---|---|---|
| `system_health_check` | *(no args)* | Progress bar + ✅/❌ report |
| `smart_note_search` | `query`: `Python` | Matches with stats |
| `bulk_create_notes` | `notes_json`: `[{"title":"Phase 6 Note","content":"Context is powerful"},{"title":"MCP Tip","content":"Always handle errors"}]` | Two notes created with progress |

---

# STEP 5 — Commit & Push

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: Phase 6 - add advanced tools with Context, progress, and tool composition"
git push origin main
```

---

# 📋 Phase 6 Revision Sheet

## Context Object — Quick Reference

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def my_tool(param: str, ctx: Context) -> str:
    """Tool with context."""
    await ctx.info("Info message")               # 📝 Log info
    await ctx.warning("Warning message")         # ⚠️ Log warning
    await ctx.report_progress(1, 2)             # 📊 Progress: step 1 of 2
    data = await ctx.read_resource("uri://...")   # 📖 Read a resource
    return "result"
```

## Rules

| Rule | Why |
|---|---|
| `ctx: Context` must be the **LAST** parameter | MCP injects it — AI doesn't see it |
| Must use `async def` | Context methods are async |
| Context is **optional** | Only add it if you need logging/progress |
| Everything inside Context is `.await` | Even `info()` and `warning()` |

## Tool Composition

```
Before Phase 6:        After Phase 6:
─────────────          ─────────────
Tool A (standalone)    Tool A
Tool B (standalone)      ├── reads Resource X
Resource X               ├── logs progress
                         └── returns combined result
```

## Express Mapping

| Express | MCP Context |
|---|---|
| `console.log()` | `await ctx.info()` |
| `console.warn()` | `await ctx.warning()` |
| `req.session` | `ctx.session` |
| Calling another API route | `await ctx.read_resource()` |
| Custom progress middleware | `await ctx.report_progress()` |

## What You Learned in Phase 6

| Concept | Key Point |
|---|---|
| Context object | Hidden from AI, injected by MCP, must be last param |
| Progress reporting | `report_progress(current, total)` — both numbers |
| Logging | `ctx.info()` and `ctx.warning()` — visible to client |
| Resource reading | Tools can read resources via `ctx.read_resource()` |
| Bulk operations | Use progress reporting for batch processing |
