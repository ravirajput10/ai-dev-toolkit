"""
SSE (Server-Sent Events) Entry Point
======================================
Runs the MCP server over HTTP instead of stdio.
This allows remote clients to connect over the network.

Usage:
    python server_sse.py                              # Default: localhost:8000
    python server_sse.py --host 0.0.0.0 --port 9000   # Custom host/port

Endpoints created automatically:
    GET  /sse       → Opens SSE stream (server → client)
    POST /messages  → Client sends JSON-RPC requests
"""

import sys
from app import mcp

# Import all modules — registers tools/resources/prompts
from tools import dev_tools, api_tools, db_tools
from tools import advanced_tools  # 3 advanced tools (Phase 6)
from resources import system_resources
from prompts import code_prompts
from db.database import init_db

# Initialize database
init_db()

# Parse command line arguments for custom host and port
# host/port live on mcp.settings (not on mcp.run())
for i, arg in enumerate(sys.argv[1:], 1):
    if arg == "--host" and i < len(sys.argv) - 1:
        mcp.settings.host = sys.argv[i + 1]
    elif arg == "--port" and i < len(sys.argv) - 1:
        mcp.settings.port = int(sys.argv[i + 1])

if __name__ == "__main__":
    host = mcp.settings.host
    port = mcp.settings.port
    print(f"🚀 Starting MCP SSE server on http://{host}:{port}/sse")
    print(f"   Press Ctrl+C to stop")
    mcp.run(transport="sse")
