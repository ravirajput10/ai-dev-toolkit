"""
Validators — Phase 7 Production Patterns
==========================================
Centralized input validation and sanitization utilities.

Why a separate module?
- Same validation logic used across multiple tools
- Single place to update rules (DRY principle)
- Easy to test independently
- Like Express middleware: validates before the handler runs

Security rules:
- Never trust AI-generated input
- Validate types, lengths, and formats
- Sanitize strings (strip dangerous content)
- Return clear error messages (not stack traces)
"""

import re

# --- Constants ---
MAX_TEXT_LENGTH = 10_000       # Max characters for text input
MAX_TITLE_LENGTH = 200         # Max characters for note titles
MAX_CONTENT_LENGTH = 50_000    # Max characters for note content
MAX_JSON_LENGTH = 100_000      # Max characters for JSON input
MAX_QUERY_LENGTH = 500         # Max characters for search queries
MAX_NOTES_BATCH = 50           # Max notes in bulk create
MAX_URL_LENGTH = 2_000         # Max URL length


class ValidationError(Exception):
    """Custom exception for validation failures.

    Why a custom exception?
    - Distinguishes validation errors from bugs
    - Carries a user-friendly message
    - Like creating a custom Error class in JavaScript:
      class ValidationError extends Error {}
    """
    pass


def validate_not_empty(value: str, field_name: str) -> str:
    """Ensure a string is not empty or whitespace-only.

    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)

    Returns:
        The stripped value

    Raises:
        ValidationError: If the value is empty
    """
    stripped = value.strip()
    if not stripped:
        raise ValidationError(f"❌ {field_name} cannot be empty")
    return stripped


def validate_max_length(value: str, max_length: int, field_name: str) -> str:
    """Ensure a string doesn't exceed max length.

    Args:
        value: The string to validate
        max_length: Maximum allowed length
        field_name: Name of the field (for error messages)

    Returns:
        The value (unchanged)

    Raises:
        ValidationError: If the value is too long
    """
    if len(value) > max_length:
        raise ValidationError(
            f"❌ {field_name} is too long ({len(value)} chars). "
            f"Maximum: {max_length} chars"
        )
    return value


def validate_text_input(value: str, field_name: str = "Input",
                        max_length: int = MAX_TEXT_LENGTH) -> str:
    """Combined validation: not empty + length check + strip.

    This is the most common validation — use it for most text inputs.

    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)
        max_length: Maximum allowed length

    Returns:
        The stripped, validated value

    Raises:
        ValidationError: If validation fails
    """
    value = validate_not_empty(value, field_name)
    value = validate_max_length(value, max_length, field_name)
    return value


def validate_note_title(title: str) -> str:
    """Validate a note title.

    Returns:
        The stripped, validated title

    Raises:
        ValidationError: If validation fails
    """
    return validate_text_input(title, "Title", MAX_TITLE_LENGTH)


def validate_note_content(content: str) -> str:
    """Validate note content.

    Returns:
        The stripped, validated content

    Raises:
        ValidationError: If validation fails
    """
    return validate_text_input(content, "Content", MAX_CONTENT_LENGTH)


def validate_search_query(query: str) -> str:
    """Validate a search query.

    Returns:
        The stripped, validated query

    Raises:
        ValidationError: If validation fails
    """
    return validate_text_input(query, "Search query", MAX_QUERY_LENGTH)


def validate_positive_int(value: int, field_name: str,
                          min_val: int = 1, max_val: int = 1000) -> int:
    """Validate an integer is within a range.

    Args:
        value: The integer to validate
        field_name: Name of the field (for error messages)
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        The validated value

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"❌ {field_name} must be a number")
    if value < min_val or value > max_val:
        raise ValidationError(
            f"❌ {field_name} must be between {min_val} and {max_val}"
        )
    return value


def validate_url(url: str) -> str:
    """Validate a URL is safe and well-formed.

    Security: Prevents file:// and internal network access attempts.

    Args:
        url: The URL to validate

    Returns:
        The validated URL

    Raises:
        ValidationError: If validation fails
    """
    url = validate_text_input(url, "URL", MAX_URL_LENGTH)

    if not url.startswith(("http://", "https://")):
        raise ValidationError("❌ URL must start with http:// or https://")

    # Block internal/private network access
    dangerous_patterns = [
        "localhost", "127.0.0.1", "0.0.0.0",
        "192.168.", "10.", "172.16.",
        "file://", "ftp://",
    ]
    url_lower = url.lower()
    for pattern in dangerous_patterns:
        if pattern in url_lower:
            raise ValidationError(
                f"❌ URL contains blocked pattern: {pattern}"
            )

    return url


def validate_hash_algorithm(algorithm: str) -> str:
    """Validate a hash algorithm name.

    Args:
        algorithm: The algorithm name (md5, sha1, sha256, sha512)

    Returns:
        Lowercase validated algorithm name

    Raises:
        ValidationError: If algorithm is not supported
    """
    allowed = {"md5", "sha1", "sha256", "sha512"}
    algo = algorithm.lower().strip()
    if algo not in allowed:
        raise ValidationError(
            f"❌ Unknown algorithm: '{algorithm}'. "
            f"Use: {', '.join(sorted(allowed))}"
        )
    return algo


def sanitize_for_display(text: str, max_preview: int = 100) -> str:
    """Sanitize text for safe display in output.

    - Truncates long text
    - Strips control characters

    Args:
        text: The text to sanitize
        max_preview: Max chars to show

    Returns:
        Sanitized preview string
    """
    # Remove control characters (except newline and tab)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    if len(cleaned) > max_preview:
        return cleaned[:max_preview] + "..."
    return cleaned
