"""
Advanced Tools — Phase 6
=========================
Tools that demonstrate:
- Context object (logging, progress, reading resources)
- Tool composition (tools using data from resources)
- Structured error handling

Key concept: `ctx: Context` is injected by MCP automatically.
The AI never sees it — it's hidden from the tool schema.
You must add it as the LAST parameter of the function.
"""

from app import mcp
from mcp.server.fastmcp import Context
import json


# ============================================================
# TOOL: System Health Check (Uses Context + Resources)
# ============================================================
# This tool READS RESOURCES from within a tool — tool composition
# It also uses ctx.info() and ctx.report_progress()
# Think of it like an Express route that calls other internal routes

@mcp.tool()
async def system_health_check(ctx: Context) -> str:
    """Run a comprehensive system health check.

    Checks system info, installed packages, and environment.
    Reports progress as it goes.
    """
    results = []

    # Step 1: Get system info
    await ctx.info("Checking system information...")
    await ctx.report_progress(0.2, "Reading system info")
    try:
        sys_info = await ctx.read_resource("system://info")
        results.append(f"✅ System Info: Available")
    except Exception as e:
        results.append(f"❌ System Info: {str(e)}")

    # Step 2: Check environment
    await ctx.info("Checking environment variables...")
    await ctx.report_progress(0.4, "Reading environment")
    try:
        env_data = await ctx.read_resource("system://env")
        results.append(f"✅ Environment: Available")
    except Exception as e:
        results.append(f"❌ Environment: {str(e)}")

    # Step 3: Check packages
    await ctx.info("Checking installed packages...")
    await ctx.report_progress(0.6, "Reading packages")
    try:
        packages = await ctx.read_resource("system://packages")
        results.append(f"✅ Packages: Available")
    except Exception as e:
        results.append(f"⚠️ Packages: {str(e)}")

    # Step 4: Check database
    await ctx.info("Checking database...")
    await ctx.report_progress(0.8, "Testing database")
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
    await ctx.report_progress(1.0, "Health check complete")
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
# Perfect example of when progress is useful — long-running tasks

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

        progress = (i + 1) / len(notes)
        await ctx.report_progress(progress, f"Creating note {i+1}/{len(notes)}")

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
