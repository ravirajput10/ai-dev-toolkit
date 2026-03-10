# 🛡️ Phase 7 — Production MCP Patterns

> **Goal:** Make your MCP server production-ready with validation, security, error handling, and tests.
> **What you'll build:** Input validators, security checks, sanitization, and unit tests.
> **Time:** ~30 minutes

---

## 🧠 Before We Start — Why Production Patterns?

Your server works, but it's **not safe**. Right now:

```python
# Phase 4 — No validation!
def create_note(title: str, content: str):
    cursor.execute("INSERT INTO notes ...")  # What if title is empty?
                                              # What if content is 10GB?
```

In production, **never trust AI-generated input**. The AI might send:
- Empty strings
- Extremely long text (crash your server)
- Dangerous URLs (access internal networks)
- Malformed data

### Your Express Analogy

```javascript
// Express BEFORE middleware:
app.post('/notes', (req, res) => {
    db.insert(req.body);  // Dangerous! No validation!
});

// Express AFTER middleware:
app.post('/notes', validateBody, (req, res) => {
    db.insert(req.body);  // Safe — validated first
});
```

Phase 7 adds that `validateBody` middleware to your MCP tools.

---

# STEP 1 — Centralized Validators

## What we created: `validators.py`

A single module with all validation logic:

| Function | What It Checks |
|---|---|
| `validate_not_empty(value, name)` | String is not empty/whitespace |
| `validate_max_length(value, max, name)` | String doesn't exceed length limit |
| `validate_text_input(value, name, max)` | Combined: not empty + length |
| `validate_note_title(title)` | Title ≤ 200 chars, not empty |
| `validate_note_content(content)` | Content ≤ 50,000 chars, not empty |
| `validate_search_query(query)` | Query ≤ 500 chars, not empty |
| `validate_positive_int(value, name)` | Integer within min-max range |
| `validate_url(url)` | Starts with http(s), blocks localhost/internal IPs |
| `validate_hash_algorithm(algo)` | Must be md5/sha1/sha256/sha512 |
| `sanitize_for_display(text)` | Truncates + strips control characters |

### Why Centralized?

```python
# BAD — validation scattered everywhere
def create_note(title, content):
    if not title: return "Error"
    if len(title) > 200: return "Error"
    ...

def search_notes(query):
    if not query: return "Error"
    if len(query) > 500: return "Error"
    ...

# GOOD — centralized validation
def create_note(title, content):
    title = validate_note_title(title)      # One line!
    content = validate_note_content(content)
    ...
```

---

# STEP 2 — Apply Validators to Tools

## The Pattern

```python
from validators import validate_note_title, ValidationError

@mcp.tool()
def create_note(title: str, content: str) -> str:
    try:
        title = validate_note_title(title)        # Step 1: VALIDATE
        content = validate_note_content(content)   # Step 2: VALIDATE
        # Step 3: Only process if validated
        cursor.execute("INSERT INTO notes ...", (title, content))
    except ValidationError as e:
        return str(e)  # Return clean error, don't crash
```

### Before vs After

```python
# BEFORE (Phase 4) — trusts all input
def create_note(title: str, content: str):
    try:
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    except Exception as e:
        return f"Error: {str(e)}"

# AFTER (Phase 7) — validates first!
def create_note(title: str, content: str):
    try:
        title = validate_note_title(title)         # NEW: validates
        content = validate_note_content(content)    # NEW: validates
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    except ValidationError as e:                    # NEW: catch validation errors
        return str(e)
    except Exception as e:
        return f"Error: {str(e)}"
```

---

# STEP 3 — Security: URL Validation

The `fetch_url` tool is especially dangerous — an AI could make it access internal networks:

```python
# DANGEROUS — allows internal network access
await client.get("http://localhost:8080/admin")     # Access your admin panel!
await client.get("http://192.168.1.1/config")       # Access your router!
await client.get("file:///etc/passwd")               # Read system files!
```

Our `validate_url()` blocks these:

```python
def validate_url(url):
    if not url.startswith(("http://", "https://")):
        raise ValidationError("URL must start with http(s)")

    dangerous = ["localhost", "127.0.0.1", "192.168.", "10.", "file://"]
    for pattern in dangerous:
        if pattern in url.lower():
            raise ValidationError(f"Blocked: {pattern}")
```

---

# STEP 4 — Unit Tests

## File: `tests/test_validators.py`

Run tests:

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit\mcp-server"
.\venv\Scripts\python.exe -m pytest tests\test_validators.py -v
```

### Test Structure

```python
class TestValidateNotEmpty(unittest.TestCase):

    def test_valid_string(self):
        result = validate_not_empty("hello", "Name")
        self.assertEqual(result, "hello")           # ✅ Should pass

    def test_empty_string_raises(self):
        with self.assertRaises(ValidationError):    # ✅ Should raise error
            validate_not_empty("", "Name")
```

### Express Analogy

```javascript
// Jest tests — same pattern!
test('valid string passes', () => {
    expect(validateNotEmpty("hello")).toBe("hello");
});

test('empty string throws', () => {
    expect(() => validateNotEmpty("")).toThrow();
});
```

---

# STEP 5 — Commit & Push

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: Phase 7 - add input validation, security, sanitization, and unit tests"
git push origin main
```

---

# 📋 Phase 7 Revision Sheet

## The Validation Pattern

```python
@mcp.tool()
def my_tool(user_input: str) -> str:
    try:
        user_input = validate_text_input(user_input, "Input")  # 1. VALIDATE
        # 2. Process only if valid
        return do_work(user_input)
    except ValidationError as e:
        return str(e)  # 3. Clean error to AI
    except Exception as e:
        return f"Error: {str(e)}"  # 4. Catch-all
```

## Security Checklist

| Check | Where |
|---|---|
| Empty input | `validate_not_empty()` |
| Length limits | `validate_max_length()` |
| URL safety | `validate_url()` — blocks localhost, internal IPs |
| SQL injection | Already handled — parameterized queries (Phase 4) |
| Control characters | `sanitize_for_display()` |
| Algorithm whitelist | `validate_hash_algorithm()` |

## Express Mapping

| Express | MCP Phase 7 |
|---|---|
| `express-validator` middleware | `validators.py` module |
| `req.body` validation | `validate_text_input()` before processing |
| Custom error class | `ValidationError` |
| Jest / Mocha tests | `unittest` / `pytest` |
| `app.use(sanitize)` | `sanitize_for_display()` |

## What You Learned in Phase 7

| Concept | Key Point |
|---|---|
| Input validation | Always validate BEFORE processing |
| Centralized validators | One module, reused everywhere (DRY) |
| Custom exceptions | `ValidationError` separates user errors from bugs |
| URL security | Block internal network access |
| Sanitization | Clean output: truncate + strip control chars |
| Unit tests | Test validators independently with `pytest` |
