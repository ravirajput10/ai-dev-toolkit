# 🛠️ AI Dev Toolkit

> A collection of AI-powered developer tools — MCP servers and AI agents built from scratch.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What Is This?

This repo contains hands-on AI engineering projects built while learning to create MCP servers and AI agents. Each project is thoroughly documented with learning notes explaining the **what, why, and how**.

**Built by:** A full-stack (MERN) developer transitioning into AI Engineering.

---

## 📂 Project Structure

```
ai-dev-toolkit/
├── mcp-server/              # MCP Server — Developer Toolkit
│   ├── server.py            # 8 developer tools exposed via MCP
│   └── MCP_LEARNING_NOTES.md # Detailed learning notes
├── agent/                   # AI Agent (coming soon)
│   └── ...
├── docs/                    # Architecture docs & diagrams
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 MCP Server — Developer Toolkit

A Model Context Protocol (MCP) server that provides 8 useful developer tools to AI assistants like Claude, Cursor, and others.

### Tools Available

| Tool | Description |
|---|---|
| `generate_uuid` | Generate a random UUID |
| `format_json` | Prettify and validate JSON strings |
| `base64_encode` | Encode text to Base64 |
| `base64_decode` | Decode Base64 to plain text |
| `hash_text` | Hash text using MD5, SHA1, SHA256, or SHA512 |
| `word_count` | Get word count, character count, and line count |
| `timestamp_convert` | Convert between Unix timestamps and dates |
| `regex_test` | Test regex patterns against text |

### Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-dev-toolkit.git
cd ai-dev-toolkit

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test with MCP Inspector
mcp dev mcp-server/server.py
```

### Connect to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "python",
      "args": ["path/to/ai-dev-toolkit/mcp-server/server.py"]
    }
  }
}
```

---

## 🤖 AI Agent (Coming Soon)

An AI agent that uses tools, memory, and planning to accomplish developer tasks autonomously.

---

## 🧠 Learning Notes

Each project includes detailed learning notes with:
- Concept explanations mapped to Express/Node.js analogies
- Step-by-step build guides
- Key takeaways and patterns

📖 [MCP Server Notes](mcp-server/MCP_LEARNING_NOTES.md)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| MCP SDK (`FastMCP`) | MCP server framework |
| Claude / Cursor | MCP clients for testing |

---

## 📄 License

MIT License — feel free to use, modify, and learn from this code.
