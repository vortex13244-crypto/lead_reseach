# MCP (Model Context Protocol) — Knowledge Base

> **Purpose:** Guide to using MCP servers to extend AI agent capabilities.
> **Related:** [CLAUDE.md](../../CLAUDE.md) · [ai.md](ai.md)

---

## Overview

MCP (Model Context Protocol) is an open standard for connecting AI models to external data sources and tools. It allows Claude and other LLMs to securely access files, databases, APIs, and services in a structured way.

---

## Available MCP Servers

### Context7

**Purpose:** Fetches up-to-date documentation for any library or framework.

**Capabilities:**
- Retrieves official docs for 1000+ libraries
- Provides current API references (not trained knowledge which may be outdated)
- Supports version-specific docs

**When to use:**
- Working with a library you're not 100% sure about
- Verifying API signatures and options
- Getting migration guides for version upgrades

**When NOT to use:**
- For well-known, stable APIs (React basics, core Node.js — model already knows these)
- When you need conceptual understanding, not API reference

**Typical scenarios:**
```
"Get the docs for shadcn/ui Button component"
"Show me the TanStack Query v5 migration guide"
"What are the options for next/image in Next.js 14?"
```

---

### Filesystem

**Purpose:** Read and write files on the local filesystem.

**Capabilities:**
- Read file contents
- List directory structure
- Write and create files
- Search within files

**When to use:**
- Analyzing existing codebases
- Reading configuration files
- Writing generated code to files
- Bulk file operations

**When NOT to use:**
- For sensitive operations without user confirmation
- Outside the workspace directory

**Limitations:**
- Restricted to configured directories only
- Cannot execute files, only read/write

**Typical scenarios:**
```
"Read all TypeScript files in src/api/ and identify patterns"
"Write the generated schema to src/types/api.ts"
"List all files changed in the last git commit"
```

---

### GitHub

**Purpose:** Interact with GitHub repositories, issues, PRs, and code.

**Capabilities:**
- Search repositories and code
- Create and read issues
- Create and review pull requests
- Access commit history
- Read file contents from any branch

**When to use:**
- Reviewing PRs and providing feedback
- Creating issues from bugs discovered
- Searching for code examples in public repos
- Checking release notes

**When NOT to use:**
- For private operations without authentication
- For bulk operations that should use the API directly

**Limitations:**
- Rate-limited by GitHub API
- Cannot push code directly (creates PRs instead)

**Typical scenarios:**
```
"Create a GitHub issue for the auth bug we found"
"Search for examples of pgvector usage in TypeScript projects"
"Read the CHANGELOG for shadcn/ui v2.0"
```

---

### Playwright

**Purpose:** Browser automation for testing and web scraping.

**Capabilities:**
- Navigate to URLs
- Click, type, and interact with page elements
- Take screenshots
- Extract content from pages
- Run end-to-end tests

**When to use:**
- Verifying that deployed features work
- Scraping data from websites that require JavaScript
- Debugging UI issues in a real browser
- Automating repetitive web workflows

**When NOT to use:**
- When the content is available via API (use fetch instead)
- For high-volume data extraction (use proper scrapers)

**Limitations:**
- Slower than HTTP requests
- Cannot handle CAPTCHAs
- Some sites detect and block automation

**Typical scenarios:**
```
"Verify that the login page at staging.yourdomain.com shows the correct form"
"Take a screenshot of the dashboard after logging in"
"Check if the pricing page renders correctly on mobile"
```

---

### Docker

**Purpose:** Manage Docker containers, images, and compose services.

**Capabilities:**
- List running containers
- Start/stop/restart containers
- View container logs
- Execute commands in containers
- Build images

**When to use:**
- Checking the status of development services
- Debugging container issues
- Running database migrations inside containers
- Inspecting logs for deployed services

**When NOT to use:**
- For production deployments (use CI/CD)
- Without explicit user authorization for destructive operations

**Limitations:**
- Cannot access containers on remote hosts without explicit configuration
- Build operations require host Docker daemon access

**Typical scenarios:**
```
"Check if the postgres container is healthy"
"Show me the last 100 lines of logs from the api container"
"Restart the redis container"
```

---

### PostgreSQL

**Purpose:** Execute SQL queries against PostgreSQL databases.

**Capabilities:**
- Execute SELECT queries
- Run DML (INSERT, UPDATE, DELETE) with confirmation
- Inspect schema (tables, columns, indices)
- Analyze query plans
- View pg_stat_* views

**When to use:**
- Debugging data issues
- Analyzing database performance
- Verifying migration results
- Exploring schema

**When NOT to use:**
- For destructive operations without explicit backup confirmation
- In production without approval (use staging)

**Limitations:**
- Restricted to configured databases
- Destructive operations require explicit confirmation
- Cannot modify schema without review

**Typical scenarios:**
```
"Show me the 10 most recent users in the database"
"Run EXPLAIN ANALYZE on this query: SELECT ..."
"What indexes exist on the orders table?"
"How many rows are in each table?"
```

---

### Figma

**Purpose:** Access Figma design files and extract design tokens.

**Capabilities:**
- Read design file contents
- Extract colors, typography, and spacing tokens
- Get component specifications
- Export assets

**When to use:**
- Implementing a design from Figma
- Extracting design tokens to add to the codebase
- Verifying that implementation matches design
- Getting exact measurements and colors

**When NOT to use:**
- When you already have the design system implemented
- For generating code from designs (manual review still required)

**Limitations:**
- Read-only access to Figma files
- Requires Figma API token with file access
- Complex components require interpretation

**Typical scenarios:**
```
"Read the color tokens from the design system file"
"What font sizes are used in the marketing page design?"
"Get the spacing values used in the Card component"
```

---

## MCP Configuration

MCP servers are configured in Claude Desktop or your AI IDE:

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

---

## Best Practices

1. **Use Context7 for library docs** — Don't rely on potentially outdated trained knowledge
2. **Confirm before destructive operations** — Always confirm with user before DELETE, DROP, or file deletion
3. **Log MCP operations** — Document what MCP tools were used in memory when making significant changes
4. **Prefer read over write** — When exploring, use read operations first
5. **Chain MCP tools** — Combine Filesystem + GitHub + Context7 for comprehensive code analysis

---

*Related: [ai.md](ai.md) · [CLAUDE.md](../../CLAUDE.md)*
