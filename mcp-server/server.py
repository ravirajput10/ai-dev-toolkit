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

# server.py — The simplest MCP server possible

from mcp.server.fastmcp import FastMCP

# Tools
import uuid
import json
import base64
import hashlib
import re
from datetime import datetime, timezone
import httpx
# import logging
# import sys

# Logging setup (uncomment to enable debug logging to file)
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     datefmt="%H:%M:%S",
#     filename="debug.log",
#     filemode="w"
# )
# logger = logging.getLogger("DevToolkit")

# Resources
import platform  
import os

# Prompts
from mcp.server.fastmcp.prompts import base  # Needed for prompt messages

# Step A: Create the server instance
# This is like: const app = express()
# The name "DevToolkit" shows up when clients connect
mcp = FastMCP("DevToolkit")


# Step B: Register a tool
# @mcp.tool() is like @app.post("/greet") in FastAPI

# ============================================================
# TOOL 1: Generate UUID
# ============================================================
# @mcp.tool() is like @app.post("/generate-uuid") in FastAPI
# The docstring becomes the tool description that the AI reads
# The AI uses this description to decide WHEN to call this tool

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The person's name to greet
    """
    return f"Hello, {name}! Welcome to MCP! 🎉"

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

            # Log the raw API response to terminal (uncomment to enable)
            # logger.debug(f"GitHub API Status: {response.status_code}")
            # logger.debug(f"GitHub API Response: {json.dumps(data, indent=2)[:1000]}")

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

            # Log the raw API response (uncomment to enable)
            # logger.debug(f"Weather API Status: {response.status_code}")
            # logger.debug(f"Weather API Response: {json.dumps(data, indent=2)[:1000]}")

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

            # Log the response (uncomment to enable)
            # logger.debug(f"URL Fetch Status: {response.status_code}")
            # logger.debug(f"URL Response: {response.text[:500]}")

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

# Resource 2: Environment Variables (Safe Subset)

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

# Resource 3: Project Structure

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

# Resource 4: Python Packages

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

# Resource 5: Current Working Directory

@mcp.resource("system://cwd")
def get_cwd() -> str:
    """Current working directory of the server process."""
    return f"📁 Current Working Directory:\n{os.getcwd()}"

# Resource 6: List Files in Directory

@mcp.resource("system://list-files")
def list_files() -> str:
    """List files in the current working directory."""
    target_dir = os.getcwd()
    try:
        files = os.listdir(target_dir)
        return f"📁 Files in {target_dir}:\n" + "\n".join(files)
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"

# ============================================================
# PROMPT 1: Code Review Template
# ============================================================
# Prompts return a list of messages (like a pre-built chat conversation)
# The AI client shows these to the user as a starting point

# Prompts return a template string that helps the user/AI
# start a specific task. Think of it like a pre-built request

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

Provide detailed feedback and suggestions for improvement."""

### Prompt 2: Explain Code

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
{code}

Use simple language and analogies where helpful."""

# Prompt 3: Debug Helper Template

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
{error_message}
{code_section}

Please:
1. Explain what this error means
2. Identify the likely cause
3. Provide the corrected code
4. Explain how to prevent this in the future"""

# Step C: Start the server

# ============================================================
# RUN THE SERVER
# ============================================================
# This starts the MCP server using stdio transport
# stdio = communication via standard input/output (stdin/stdout)
# This is how Claude Desktop and other local clients connect

if __name__ == "__main__":
    mcp.run(transport="stdio")