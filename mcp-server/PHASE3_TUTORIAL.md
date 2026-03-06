# 🌐 Phase 3 — External APIs & Async Tools

> **Goal:** Learn to build MCP tools that call external APIs using async Python.
> **What you'll build:** Add 3 async tools — GitHub repo search, Weather lookup, and URL fetcher.
> **Time:** ~40 minutes

---

## 🧠 Before We Start — What's New in Phase 3?

In Phase 1-2, all your tools used Python's built-in libraries (hashlib, json, etc). They run instantly.

**Phase 3 is different.** You'll call external APIs over the internet — and those take time. That's where `async` comes in.

```
Phase 1-2 Tools              Phase 3 Tools
──────────────────           ──────────────────
hash_text("hello")           search_github("mcp server")
  → instant (CPU)              → waits for GitHub API (network)
  → def (sync)                 → async def (async)
  → no internet needed         → needs internet
```

---

# STEP 1 — Understanding Async in Python

## 🎯 Why Async?

When your tool calls an API, it **waits** for the response. With sync code, the entire server is blocked during that wait. With async, the server can handle other requests while waiting.

### Your JS Analogy

You already know async! It's the same concept as JavaScript:

```javascript
// JavaScript — you've done this 1000 times
const response = await fetch('https://api.github.com/...');
const data = await response.json();
```

```python
# Python — same concept, different syntax
response = await client.get('https://api.github.com/...')
data = response.json()
```

### Key Differences: JS vs Python async

| JavaScript | Python |
|---|---|
| `async function name()` | `async def name()` |
| `await fetch(url)` | `await client.get(url)` |
| `fetch` is built-in | Need `httpx` library (like axios) |
| Promises | Coroutines |
| Auto-runs event loop | FastMCP handles event loop for you |

**Good news:** FastMCP handles all the async complexity. You just write `async def` instead of `def`, and use `await` for API calls.

---

# STEP 2 — Install httpx

## 🎯 Why httpx?

Python's built-in `urllib` is clunky and doesn't support async. `httpx` is the modern choice — like `axios` for Python.

| JS | Python |
|---|---|
| `axios` or `fetch` | `httpx` |

## ▶️ Run This Now

```powershell
# Make sure venv is activated first!
pip install httpx
```

> **What this does:** Installs `httpx` — an HTTP client library that supports both sync and async requests.

## ✅ Verify

```powershell
python -c "import httpx; print(f'httpx {httpx.__version__} installed!')"
```

---

# STEP 3 — Tool 1: GitHub Repository Search

## 🎯 Why This Tool?

This is a practical tool that searches GitHub repos. It teaches:
- `async def` for MCP tools
- Making HTTP requests with `httpx`
- Parsing JSON API responses
- Error handling for network requests

## 📌 What You'll Learn
- `async def` instead of `def`
- `httpx.AsyncClient()` — async HTTP client
- `async with` — Python's async context manager
- Handling API errors (timeouts, rate limits)

## ▶️ Code — Add to `server.py`

Add `import httpx` at the top with other imports, then add this tool:

```python
import httpx  # Add at the top with other imports

# ============================================================
# ASYNC TOOL 1: GitHub Repository Search
# ============================================================
# This is our first ASYNC tool — it calls an external API
# Notice: async def (not def) and await (for network calls)
# FastMCP handles the async event loop — you just write the code

@mcp.tool()
async def search_github(query: str, max_results: int = 5) -> str:
    """Search GitHub repositories by keyword.

    Find open-source projects, libraries, and tools on GitHub.
    Returns repository name, stars, description, and URL.

    Args:
        query: Search query (e.g., "mcp server python")
        max_results: Number of results to return (default: 5, max: 10)
    """
    max_results = min(max_results, 10)  # Cap at 10 to avoid huge responses

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "per_page": max_results, "sort": "stars"},
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            if data["total_count"] == 0:
                return f"🔍 No repositories found for: {query}"

            results = [f"🔍 GitHub Search: '{query}' ({data['total_count']} total results)\n"]
            for i, repo in enumerate(data["items"], 1):
                results.append(
                    f"{i}. ⭐ {repo['stargazers_count']:,} | "
                    f"**{repo['full_name']}**\n"
                    f"   {repo['description'] or 'No description'}\n"
                    f"   🔗 {repo['html_url']}\n"
                )

            return "\n".join(results)

        except httpx.TimeoutException:
            return "❌ Request timed out. GitHub API might be slow — try again."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                return "❌ GitHub API rate limit exceeded. Wait a minute and try again."
            return f"❌ GitHub API error: {e.response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
```

## 🔍 Line-by-Line Breakdown

| Line | What It Does | JS Equivalent |
|---|---|---|
| `async def search_github(...)` | Async function | `async function searchGithub(...)` |
| `async with httpx.AsyncClient()` | Create HTTP client | Creating an axios instance |
| `await client.get(url, ...)` | Make GET request | `await axios.get(url, ...)` |
| `response.raise_for_status()` | Throw on 4xx/5xx | axios does this by default |
| `response.json()` | Parse JSON body | `response.data` in axios |
| `timeout=10.0` | 10 second timeout | `axios.get(url, {timeout: 10000})` |

## ▶️ Test It

```powershell
mcp dev server.py
```

In the Inspector → Tools → `search_github`:
- **query:** `mcp server python`
- **max_results:** `3`

Click "Run Tool" → you should see real GitHub repos with stars! ⭐

---

# STEP 4 — Tool 2: Weather Lookup (Free API)

## 🎯 Why This Tool?

Shows how to use a different API. Uses `wttr.in` — a free weather API that needs no API key.

## ▶️ Code — Add to `server.py`

```python
# ============================================================
# ASYNC TOOL 2: Weather Lookup
# ============================================================
# Uses wttr.in — a free weather API (no API key needed!)
# Demonstrates: async HTTP call with different response format

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city.

    Returns temperature, conditions, humidity, and wind speed.
    Works for any city worldwide.

    Args:
        city: City name (e.g., "London", "New York", "Mumbai")
    """
    async with httpx.AsyncClient() as client:
        try:
            # wttr.in returns JSON when we add ?format=j1
            response = await client.get(
                f"https://wttr.in/{city}",
                params={"format": "j1"},
                headers={"User-Agent": "MCP-DevToolkit"},
                timeout=10.0,
                follow_redirects=True
            )
            response.raise_for_status()
            data = response.json()

            current = data["current_condition"][0]
            location = data["nearest_area"][0]

            city_name = location["areaName"][0]["value"]
            country = location["country"][0]["value"]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]
            feels_like = current["FeelsLikeC"]

            return f"""🌤️ Weather for {city_name}, {country}:

🌡️ Temperature: {temp_c}°C ({temp_f}°F)
🤔 Feels like: {feels_like}°C
☁️ Condition: {desc}
💧 Humidity: {humidity}%
💨 Wind: {wind_kmph} km/h"""

        except httpx.TimeoutException:
            return f"❌ Weather request timed out for '{city}'. Try again."
        except Exception as e:
            return f"❌ Could not get weather for '{city}': {str(e)}"
```

## ▶️ Test It

Inspector → `get_weather`:
- **city:** `Mumbai` or `London` or your city

---

# STEP 5 — Tool 3: URL Content Fetcher

## 🎯 Why This Tool?

Fetches and summarizes content from any URL. Useful for the AI to quickly read a webpage.

## ▶️ Code — Add to `server.py`

```python
# ============================================================
# ASYNC TOOL 3: URL Content Fetcher
# ============================================================
# Fetches text content from a URL — useful for reading docs,
# checking API responses, or grabbing page content

@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch text content from a URL.

    Retrieves the content of a webpage or API endpoint.
    Returns the first 2000 characters to keep responses manageable.

    Args:
        url: The URL to fetch (must start with http:// or https://)
    """
    # Validate URL
    if not url.startswith(("http://", "https://")):
        return "❌ Invalid URL. Must start with http:// or https://"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={"User-Agent": "MCP-DevToolkit/1.0"},
                timeout=10.0,
                follow_redirects=True
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            content = response.text[:2000]  # Limit to 2000 chars

            return f"""🌐 URL: {url}
📊 Status: {response.status_code}
📄 Content-Type: {content_type}
📏 Length: {len(response.text):,} characters

Content (first 2000 chars):
{content}"""

        except httpx.TimeoutException:
            return f"❌ Request timed out for: {url}"
        except httpx.HTTPStatusError as e:
            return f"❌ HTTP Error {e.response.status_code} for: {url}"
        except Exception as e:
            return f"❌ Error fetching URL: {str(e)}"
```

## ▶️ Test It

Inspector → `fetch_url`:
- **url:** `https://api.github.com` (returns GitHub API info)
- **url:** `https://httpbin.org/json` (returns test JSON)

---

# STEP 6 — Update requirements.txt

Add `httpx` to your requirements file:

```
mcp[cli]
httpx
```

---

# STEP 7 — Commit & Push

```powershell
cd "d:\My Projects\AI Engineering\ai-dev-toolkit"
git add -A
git commit -m "feat: Phase 3 - add async tools (GitHub search, weather, URL fetch)"
git push origin main
```

---

# 📋 Phase 3 Revision Sheet

## Sync vs Async Tools

```python
# SYNC — for local, instant operations (Phase 1-2)
@mcp.tool()
def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# ASYNC — for network/API calls (Phase 3)
@mcp.tool()
async def search_github(query: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

## httpx Cheat Sheet (= axios for Python)

```python
import httpx

async with httpx.AsyncClient() as client:
    # GET request
    response = await client.get(url, params={"q": "search"}, timeout=10.0)

    # POST request
    response = await client.post(url, json={"key": "value"})

    # With headers
    response = await client.get(url, headers={"Authorization": "Bearer token"})

    # Check status
    response.raise_for_status()  # Throws on 4xx/5xx

    # Parse response
    data = response.json()       # JSON → dict
    text = response.text         # Raw text
    status = response.status_code  # 200, 404, etc.
```

## JS ↔ Python Async Mapping

| JavaScript (axios) | Python (httpx) |
|---|---|
| `async function fn()` | `async def fn()` |
| `await axios.get(url)` | `await client.get(url)` |
| `response.data` | `response.json()` |
| `response.status` | `response.status_code` |
| `try { } catch (err) { }` | `try: ... except Exception as e:` |
| `axios.create({baseURL})` | `httpx.AsyncClient(base_url=...)` |
| `{timeout: 10000}` (ms) | `timeout=10.0` (seconds) |

## Error Handling Pattern for API Tools

```python
@mcp.tool()
async def api_tool(param: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return format_result(data)
        except httpx.TimeoutException:
            return "❌ Request timed out"
        except httpx.HTTPStatusError as e:
            return f"❌ HTTP {e.response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
```

## What You Learned in Phase 3

| Concept | Key Point |
|---|---|
| `async def` | Use for any tool that does I/O (API calls, file reads) |
| `httpx` | Modern HTTP client for Python, like axios |
| `async with` | Context manager for async resources (auto-cleanup) |
| `await` | Wait for an async operation to complete |
| `timeout` | Always set timeouts for API calls |
| `raise_for_status()` | Throws exception on 4xx/5xx responses |
| Response capping | Limit response size to keep AI context manageable |
