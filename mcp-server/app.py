"""
Developer Toolkit MCP Server — App Instance
=============================================
This module creates the shared FastMCP instance.
All tools, resources, and prompts import `mcp` from here.

This is like creating `const app = express()` in a separate file
so that route files can import it without circular dependencies.
"""

from mcp.server.fastmcp import FastMCP

# Create the shared MCP instance
# The name "DevToolkit" shows up when clients connect
mcp = FastMCP("DevToolkit")
