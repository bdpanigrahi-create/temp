---
name: github-mcp-server
description: Set up a real GitHub MCP server exposed over HTTP.
---

# GitHub MCP Server Skill

This skill provides instructions and a bridge script to run the official GitHub Model Context Protocol (MCP) server and expose it over HTTP, making it accessible to clients that require an HTTP endpoint instead of stdio.

## Why a Bridge is Needed

The official GitHub MCP server (`@modelcontextprotocol/server-github`) communicates over standard I/O (stdio) by default. If your application framework (like `google.adk`) expects an HTTP URL (e.g., `http://localhost:8105/mcp/github`), you need a bridge to translate HTTP requests to stdio.

## Prerequisites

-   Node.js and `npx` installed.
-   A GitHub Personal Access Token (PAT) with appropriate scopes.

## Usage

1.  Set the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable:
    ```bash
    export GITHUB_PERSONAL_ACCESS_TOKEN="your_pat_here"
    ```
2.  Run the bridge script:
    ```bash
    python3 skills/github_mcp_server/scripts/github_http_bridge.py
    ```
3.  The server will be available at `http://localhost:8105`.

## Scripts

### [github_http_bridge.py](file:///usr/local/google/home/bdpanigrahi/a9y/agent_demo/skills/github_mcp_server/scripts/github_http_bridge.py)

The Python script that spawns the Node.js server and acts as an HTTP bridge.
