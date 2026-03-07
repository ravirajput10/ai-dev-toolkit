"""
System Resources — Phase 2 Resources
======================================
Read-only data: system info, env vars, project structure, packages, CWD, file listing.
"""

import os
import platform

from app import mcp


# ============================================================
# RESOURCE: System Information
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


# ============================================================
# RESOURCE: Environment Variables (Safe Subset)
# ============================================================

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


# ============================================================
# RESOURCE: Project Structure
# ============================================================

@mcp.resource("project://structure")
def get_project_structure() -> str:
    """Current project directory structure."""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    structure = []

    for root, dirs, files in os.walk(project_dir):
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


# ============================================================
# RESOURCE: Python Packages
# ============================================================

@mcp.resource("system://packages")
def get_installed_packages() -> str:
    """List of installed Python packages in the current environment."""
    try:
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


# ============================================================
# RESOURCE: Current Working Directory
# ============================================================

@mcp.resource("system://cwd")
def get_cwd() -> str:
    """Current working directory of the server process."""
    return f"📁 Current Working Directory:\n{os.getcwd()}"


# ============================================================
# RESOURCE: List Files
# ============================================================

@mcp.resource("system://list-files")
def list_files() -> str:
    """List files in the current working directory."""
    target_dir = os.getcwd()
    try:
        files = os.listdir(target_dir)
        return f"📁 Files in {target_dir}:\n" + "\n".join(files)
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"
