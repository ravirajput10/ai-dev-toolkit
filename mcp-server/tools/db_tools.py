"""
DB Tools — Phase 4 Tools (Production-hardened in Phase 7)
===========================================================
Database CRUD tools for the Notes Manager: create, list, search, delete notes.
All inputs are validated before processing.
"""

from app import mcp
from db.database import get_connection
from validators import (
    validate_note_title,
    validate_note_content,
    validate_search_query,
    validate_positive_int,
    ValidationError,
    sanitize_for_display,
)


# ============================================================
# TOOL: Create Note
# ============================================================
# This tool WRITES to the database — it has side effects
# That's why it's a Tool (not a Resource). Resources are read-only.

@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Create a new note and save it to the database.

    Args:
        title: Title of the note
        content: Content/body of the note
    """
    try:
        # Phase 7: Validate inputs BEFORE touching the database
        title = validate_note_title(title)
        content = validate_note_content(content)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return f"✅ Note created successfully!\n📝 ID: {note_id}\n📌 Title: {title}"
    except ValidationError as e:
        return str(e)
    except Exception as e:
        return f"❌ Error creating note: {str(e)}"


# ============================================================
# TOOL: List Notes
# ============================================================

@mcp.tool()
def list_notes(limit: int = 10) -> str:
    """List all saved notes, most recent first.

    Args:
        limit: Maximum number of notes to return (default: 10)
    """
    try:
        # Phase 7: Validate limit
        limit = validate_positive_int(limit, "Limit", min_val=1, max_val=100)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        notes = cursor.fetchall()
        conn.close()

        if not notes:
            return "📭 No notes found. Create one with the create_note tool!"

        result = f"📋 Notes ({len(notes)} found):\n\n"
        for note_id, title, content, created_at in notes:
            preview = sanitize_for_display(content)
            result += f"━━━━━━━━━━━━━━━━━━━━\n"
            result += f"📝 ID: {note_id} | {created_at}\n"
            result += f"📌 {title}\n"
            result += f"   {preview}\n\n"

        return result
    except ValidationError as e:
        return str(e)
    except Exception as e:
        return f"❌ Error listing notes: {str(e)}"


# ============================================================
# TOOL: Search Notes
# ============================================================

@mcp.tool()
def search_notes(query: str) -> str:
    """Search notes by title or content.

    Args:
        query: Search term to look for in note titles and content
    """
    try:
        # Phase 7: Validate search query
        query = validate_search_query(query)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, created_at FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC",
            (f"%{query}%", f"%{query}%")
        )
        notes = cursor.fetchall()
        conn.close()

        if not notes:
            return f"🔍 No notes found matching: '{query}'"

        result = f"🔍 Search results for '{query}' ({len(notes)} found):\n\n"
        for note_id, title, content, created_at in notes:
            preview = sanitize_for_display(content)
            result += f"━━━━━━━━━━━━━━━━━━━━\n"
            result += f"📝 ID: {note_id} | {created_at}\n"
            result += f"📌 {title}\n"
            result += f"   {preview}\n\n"

        return result
    except ValidationError as e:
        return str(e)
    except Exception as e:
        return f"❌ Error searching notes: {str(e)}"


# ============================================================
# TOOL: Delete Note
# ============================================================

@mcp.tool()
def delete_note(note_id: int) -> str:
    """Delete a note by its ID.

    Args:
        note_id: The ID of the note to delete (use list_notes to find IDs)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()

        if not note:
            conn.close()
            return f"❌ Note with ID {note_id} not found"

        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return f"🗑️ Deleted note: '{note[0]}' (ID: {note_id})"
    except Exception as e:
        return f"❌ Error deleting note: {str(e)}"
