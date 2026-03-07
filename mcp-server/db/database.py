"""
Database Setup
===============
SQLite database configuration and initialization for the Notes Manager.
"""

import os
import sqlite3

# Database file path — stored in the mcp-server directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notes.db")


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


def get_connection():
    """Get a database connection. Use this in tools for consistent access."""
    return sqlite3.connect(DB_PATH)
