"""
Developer Toolkit MCP Server
=============================
Entry point for the MCP server. Imports all tools, resources, and prompts
from their respective modules and starts the server.

Structure:
├── app.py                      → FastMCP instance (shared across modules)
├── tools/
│   ├── dev_tools.py            → Phase 1: greet, uuid, json, base64, hash, etc.
│   ├── api_tools.py            → Phase 3: GitHub search, weather, URL fetch
│   ├── db_tools.py             → Phase 4: Notes CRUD (create, list, search, delete)
│   └── advanced_tools.py       → Phase 6: System health check, smart note search
├── resources/
│   └── system_resources.py     → Phase 2: system info, env, packages, etc.
├── prompts/
│   └── code_prompts.py         → Phase 2: code review, explain code, debug error
├── db/
│   └── database.py             → Database setup and connection helper
├── validators.py               → Phase 7: Input validation and security
└── tests/
    └── test_validators.py      → Phase 7: 37 unit tests
"""

# Import the shared MCP instance
from app import mcp

# Import all modules — decorators register tools/resources/prompts on import
from tools import dev_tools      # 9 sync tools (Phase 1)
from tools import api_tools      # 3 async tools (Phase 3)
from tools import db_tools       # 4 database tools (Phase 4)
from tools import advanced_tools # 3 advanced tools (Phase 6)
from resources import system_resources  # 6 resources (Phase 2)
from prompts import code_prompts       # 3 prompts (Phase 2)

# Initialize the database
from db.database import init_db
init_db()

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")