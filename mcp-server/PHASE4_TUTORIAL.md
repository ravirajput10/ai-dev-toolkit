# 🗄️ Phase 4 — Database-Connected MCP Tools

> **Goal:** Learn to build MCP tools that interact with a database (SQLite).
> **What you'll build:** A "Notes Manager" — CRUD tools to create, read, search, and delete notes.
> **Time:** ~30 minutes

---

## 🧠 Before We Start — Why Database Tools?

Phases 1-3 were **stateless** — tools process input and return output, nothing is saved. Phase 4 is **stateful** — tools save data to a database that persists between sessions.

```
Phase 1-3 (Stateless)              Phase 4 (Stateful)
──────────────────────             ──────────────────────
hash_text("hello") → hash         create_note("title", "body")
  → nothing saved                   → saved to SQLite database
  → same input = same output        → data persists between sessions
```

### Your MERN Analogy

```
Express + MongoDB                  MCP + SQLite
──────────────────                 ──────────────────
app.post("/notes")                 @mcp.tool() create_note()
app.get("/notes")                  @mcp.tool() list_notes()
app.get("/notes/search")           @mcp.tool() search_notes()
app.delete("/notes/:id")           @mcp.tool() delete_note()
mongoose.connect()                 sqlite3.connect()
```

Same CRUD pattern, different tech!

---

## Why SQLite (Not MongoDB/PostgreSQL)?

| Feature | SQLite | MongoDB/PostgreSQL |
|---|---|---|
| Setup | Zero — built into Python | Need separate server |
| Dependencies | None | Need driver package |
| Storage | Single `.db` file | Separate service |
| Perfect for | Local tools, prototyping | Production apps |
| Your use case | ✅ MCP server tools | Overkill for this |

SQLite comes **built into Python** — no `pip install` needed. The entire database is a single file.

---

# STEP 1 — Create the Database Setup

## 🎯 Why This Step?

We need a function that creates the database and table if they don't exist. This runs once when the server starts.

## ▶️ Code — Add to `server.py`

Add `import sqlite3` at the top with other imports, then add the setup function **after your imports but before the tools**:

```python
import sqlite3  # Add at the top — built into Python, no pip install needed

# ============================================================
# DATABASE SETUP
# ============================================================
# SQLite database file — stored in the same directory as server.py
# This is like mongoose.connect() but for a file-based database

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.db")

def init_db():
    """Create the notes table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize database when server starts
init_db()
```

### Line-by-Line Breakdown

| Line | What It Does | MERN Equivalent |
|---|---|---|
| `DB_PATH = ...` | Path to the `.db` file | `MONGO_URI = "mongodb://..."` |
| `sqlite3.connect(DB_PATH)` | Connect to database | `mongoose.connect(uri)` |
| `CREATE TABLE IF NOT EXISTS` | Create table | Mongoose schema definition |
| `id INTEGER PRIMARY KEY AUTOINCREMENT` | Auto-increment ID | MongoDB `_id` |
| `init_db()` | Run on startup | `mongoose.connect()` in `app.js` |

---

# STEP 2 — Tool: Create Note

## ▶️ Code

```python
# ============================================================
# DB TOOL 1: Create Note
# ============================================================
# This tool WRITES to the database — it has side effects
# That's why it's a Tool, not a Resource

@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Create a new note and save it to the database.

    Args:
        title: Title of the note
        content: Content/body of the note
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return f"✅ Note created successfully!\n📝 ID: {note_id}\n📌 Title: {title}"
    except Exception as e:
        return f"❌ Error creating note: {str(e)}"
```

> **Security note:** We use `?` placeholders (parameterized queries), **not** f-strings for SQL. This prevents SQL injection — the same concept as using parameterized queries in MongoDB/Express.
>
> ```python
> # ❌ DANGEROUS — SQL injection vulnerability
> cursor.execute(f"INSERT INTO notes VALUES ('{title}', '{content}')")
>
> # ✅ SAFE — parameterized query
> cursor.execute("INSERT INTO notes VALUES (?, ?)", (title, content))
> ```

---

# STEP 3 — Tool: List Notes

## ▶️ Code

```python
# ============================================================
# DB TOOL 2: List Notes
# ============================================================

@mcp.tool()
def list_notes(limit: int = 10) -> str:
    """List all saved notes, most recent first.

    Args:
        limit: Maximum number of notes to return (default: 10)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
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
            # Truncate content preview to 100 chars
            preview = content[:100] + "..." if len(content) > 100 else content
            result += f"━━━━━━━━━━━━━━━━━━━━\n"
            result += f"📝 ID: {note_id} | {created_at}\n"
            result += f"📌 {title}\n"
            result += f"   {preview}\n\n"

        return result
    except Exception as e:
        return f"❌ Error listing notes: {str(e)}"
```

---

# STEP 4 — Tool: Search Notes

## ▶️ Code

```python
# ============================================================
# DB TOOL 3: Search Notes
# ============================================================

@mcp.tool()
def search_notes(query: str) -> str:
    """Search notes by title or content.

    Args:
        query: Search term to look for in note titles and content
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # LIKE with % does a "contains" search — like MongoDB's $regex
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
            preview = content[:100] + "..." if len(content) > 100 else content
            result += f"━━━━━━━━━━━━━━━━━━━━\n"
            result += f"📝 ID: {note_id} | {created_at}\n"
            result += f"📌 {title}\n"
            result += f"   {preview}\n\n"

        return result
    except Exception as e:
        return f"❌ Error searching notes: {str(e)}"
```

---

# STEP 5 — Tool: Delete Note

## ▶️ Code

```python
# ============================================================
# DB TOOL 4: Delete Note
# ============================================================

@mcp.tool()
def delete_note(note_id: int) -> str:
    """Delete a note by its ID.

    Args:
        note_id: The ID of the note to delete (use list_notes to find IDs)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # First check if note exists
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
```

---

# STEP 6 — Test It!

## ▶️ Run This Now

```powershell
mcp dev server.py
```

### Test Sequence in the Inspector:

1. **Create** → `create_note(title="MCP Learning", content="MCP uses JSON-RPC over stdio")`
2. **Create** → `create_note(title="Python Tips", content="Use type hints for better tooling")`
3. **Create** → `create_note(title="Phase 4 Notes", content="SQLite is built into Python, no install needed")`
4. **List** → `list_notes()` — should show all 3 notes
5. **Search** → `search_notes(query="Python")` — should find note #2
6. **Delete** → `delete_note(note_id=1)` — deletes first note
7. **List** → `list_notes()` — should show only 2 notes now

### Verify the database file exists:

```powershell
ls *.db    # Should show notes.db
```

---

# STEP 7 — Update .gitignore & Push

Add `*.db` to `.gitignore` (database files shouldn't be committed):

Then commit:

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: Phase 4 - add database tools (notes CRUD with SQLite)"
git push origin main
```

---

# 📋 Phase 4 Revision Sheet

## SQLite in MCP — Pattern

```python
import sqlite3

DB_PATH = "notes.db"

@mcp.tool()
def db_tool(param: str) -> str:
    conn = sqlite3.connect(DB_PATH)    # 1. Connect
    cursor = conn.cursor()             # 2. Create cursor
    cursor.execute("SQL ...", (param,)) # 3. Execute (parameterized!)
    conn.commit()                       # 4. Commit (for INSERT/UPDATE/DELETE)
    result = cursor.fetchall()          # 5. Fetch (for SELECT)
    conn.close()                        # 6. Close
    return format(result)
```

## CRUD Mapping

| CRUD | SQL | MongoDB | MCP Tool |
|---|---|---|---|
| **C**reate | `INSERT INTO` | `db.collection.insertOne()` | `create_note()` |
| **R**ead | `SELECT` | `db.collection.find()` | `list_notes()` |
| **R**ead | `SELECT WHERE LIKE` | `db.collection.find({$regex})` | `search_notes()` |
| **D**elete | `DELETE WHERE` | `db.collection.deleteOne()` | `delete_note()` |

## Security: Parameterized Queries

```python
# ❌ SQL INJECTION — never do this
cursor.execute(f"SELECT * FROM notes WHERE title = '{user_input}'")

# ✅ SAFE — always use ? placeholders
cursor.execute("SELECT * FROM notes WHERE title = ?", (user_input,))
```

## Resource vs Tool for Database

| Operation | Use Tool or Resource? |
|---|---|
| Read data (SELECT) | **Could be either**, but Tool is more flexible |
| Write data (INSERT/UPDATE/DELETE) | **Must be Tool** — has side effects |
| We chose Tool for ALL | Simpler, and AI can chain operations |
