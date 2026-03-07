"""
Code Prompts — Phase 2 Prompts
================================
Reusable prompt templates: code review, explain code, debug error.
"""

from app import mcp


# ============================================================
# PROMPT: Code Review Template
# ============================================================
# Prompts return a template string that helps the user/AI
# start a specific task. Think of it like a pre-built request.

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


# ============================================================
# PROMPT: Code Explanation Template
# ============================================================

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


# ============================================================
# PROMPT: Debug Error Template
# ============================================================

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
