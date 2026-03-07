"""
Dev Tools — Phase 1 Tools
==========================
Core developer utility tools: greet, UUID, JSON, Base64, hash, word count,
timestamp converter, and regex tester.
"""

import uuid
import json
import base64
import hashlib
import re
from datetime import datetime, timezone

from app import mcp


# ============================================================
# TOOL: Greet
# ============================================================
# @mcp.tool() is like @app.post("/greet") in FastAPI
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
# TOOL: Generate UUID
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
# TOOL: Format/Validate JSON
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
# TOOL: Base64 Encode
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
# TOOL: Base64 Decode
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
# TOOL: Hash Text
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
# TOOL: Word Count / Text Stats
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
# TOOL: Timestamp Converter
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
# TOOL: Regex Tester
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
