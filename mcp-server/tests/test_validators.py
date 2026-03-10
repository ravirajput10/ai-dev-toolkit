"""
Unit Tests for Validators — Phase 7
=====================================
Tests for the validators module using Python's built-in unittest.

Run with:
    python -m pytest tests/test_validators.py -v
    OR
    python -m unittest tests/test_validators.py -v

Why test?
- Validators are critical — bugs here = security holes
- Tests catch regressions when you update validation rules
- They serve as documentation of expected behavior
"""

import sys
import os

# Add the parent directory to sys.path so we can import validators
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from validators import (
    validate_not_empty,
    validate_max_length,
    validate_text_input,
    validate_note_title,
    validate_note_content,
    validate_search_query,
    validate_positive_int,
    validate_url,
    validate_hash_algorithm,
    sanitize_for_display,
    ValidationError,
)


class TestValidateNotEmpty(unittest.TestCase):
    """Tests for validate_not_empty."""

    def test_valid_string(self):
        result = validate_not_empty("hello", "Name")
        self.assertEqual(result, "hello")

    def test_strips_whitespace(self):
        result = validate_not_empty("  hello  ", "Name")
        self.assertEqual(result, "hello")

    def test_empty_string_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_empty("", "Name")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_empty("   ", "Name")


class TestValidateMaxLength(unittest.TestCase):
    """Tests for validate_max_length."""

    def test_under_limit(self):
        result = validate_max_length("hello", 10, "Text")
        self.assertEqual(result, "hello")

    def test_at_limit(self):
        result = validate_max_length("12345", 5, "Text")
        self.assertEqual(result, "12345")

    def test_over_limit_raises(self):
        with self.assertRaises(ValidationError):
            validate_max_length("123456", 5, "Text")


class TestValidateTextInput(unittest.TestCase):
    """Tests for validate_text_input (combined validation)."""

    def test_valid_input(self):
        result = validate_text_input("hello world", "Text")
        self.assertEqual(result, "hello world")

    def test_empty_raises(self):
        with self.assertRaises(ValidationError):
            validate_text_input("", "Text")

    def test_too_long_raises(self):
        with self.assertRaises(ValidationError):
            validate_text_input("x" * 101, "Text", max_length=100)


class TestValidateNoteTitle(unittest.TestCase):
    """Tests for validate_note_title."""

    def test_valid_title(self):
        result = validate_note_title("My Note")
        self.assertEqual(result, "My Note")

    def test_empty_title_raises(self):
        with self.assertRaises(ValidationError):
            validate_note_title("")

    def test_too_long_title_raises(self):
        with self.assertRaises(ValidationError):
            validate_note_title("x" * 201)  # MAX_TITLE_LENGTH = 200


class TestValidateNoteContent(unittest.TestCase):
    """Tests for validate_note_content."""

    def test_valid_content(self):
        result = validate_note_content("Some note content")
        self.assertEqual(result, "Some note content")

    def test_empty_content_raises(self):
        with self.assertRaises(ValidationError):
            validate_note_content("")

    def test_too_long_content_raises(self):
        with self.assertRaises(ValidationError):
            validate_note_content("x" * 50_001)  # MAX_CONTENT_LENGTH = 50,000


class TestValidateSearchQuery(unittest.TestCase):
    """Tests for validate_search_query."""

    def test_valid_query(self):
        result = validate_search_query("python")
        self.assertEqual(result, "python")

    def test_empty_query_raises(self):
        with self.assertRaises(ValidationError):
            validate_search_query("")

    def test_too_long_query_raises(self):
        with self.assertRaises(ValidationError):
            validate_search_query("x" * 501)  # MAX_QUERY_LENGTH = 500


class TestValidatePositiveInt(unittest.TestCase):
    """Tests for validate_positive_int."""

    def test_valid_int(self):
        result = validate_positive_int(5, "Limit")
        self.assertEqual(result, 5)

    def test_min_boundary(self):
        result = validate_positive_int(1, "Limit")
        self.assertEqual(result, 1)

    def test_zero_raises(self):
        with self.assertRaises(ValidationError):
            validate_positive_int(0, "Limit")

    def test_negative_raises(self):
        with self.assertRaises(ValidationError):
            validate_positive_int(-5, "Limit")

    def test_over_max_raises(self):
        with self.assertRaises(ValidationError):
            validate_positive_int(1001, "Limit")


class TestValidateUrl(unittest.TestCase):
    """Tests for validate_url."""

    def test_valid_https(self):
        result = validate_url("https://example.com")
        self.assertEqual(result, "https://example.com")

    def test_valid_http(self):
        result = validate_url("http://example.com")
        self.assertEqual(result, "http://example.com")

    def test_no_protocol_raises(self):
        with self.assertRaises(ValidationError):
            validate_url("example.com")

    def test_localhost_blocked(self):
        with self.assertRaises(ValidationError):
            validate_url("http://localhost:8080")

    def test_internal_ip_blocked(self):
        with self.assertRaises(ValidationError):
            validate_url("http://192.168.1.1")

    def test_file_protocol_blocked(self):
        with self.assertRaises(ValidationError):
            validate_url("file:///etc/passwd")


class TestValidateHashAlgorithm(unittest.TestCase):
    """Tests for validate_hash_algorithm."""

    def test_valid_algorithms(self):
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            result = validate_hash_algorithm(algo)
            self.assertEqual(result, algo)

    def test_case_insensitive(self):
        result = validate_hash_algorithm("SHA256")
        self.assertEqual(result, "sha256")

    def test_invalid_algorithm_raises(self):
        with self.assertRaises(ValidationError):
            validate_hash_algorithm("sha999")


class TestSanitizeForDisplay(unittest.TestCase):
    """Tests for sanitize_for_display."""

    def test_short_text(self):
        result = sanitize_for_display("hello")
        self.assertEqual(result, "hello")

    def test_truncation(self):
        result = sanitize_for_display("x" * 200, max_preview=100)
        self.assertEqual(len(result), 103)  # 100 + "..."
        self.assertTrue(result.endswith("..."))

    def test_removes_control_chars(self):
        result = sanitize_for_display("hello\x00world")
        self.assertEqual(result, "helloworld")

    def test_keeps_newlines_and_tabs(self):
        result = sanitize_for_display("hello\nworld\ttab")
        self.assertIn("\n", result)
        self.assertIn("\t", result)


if __name__ == "__main__":
    unittest.main()
