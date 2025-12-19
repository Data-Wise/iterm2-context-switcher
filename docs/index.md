# aiterm

**Terminal optimizer CLI for AI-assisted development with Claude Code and Gemini CLI.**

![Version](https://img.shields.io/badge/version-0.1.0--dev-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-51%20passing-green)
![Coverage](https://img.shields.io/badge/coverage-83%25-green)

---

## What It Does

**aiterm** optimizes your terminal for AI-assisted development by:

- 🎯 **Smart Context Detection** - Automatically detects project type (Python, R, Node.js, etc.)
- 🎨 **Auto Profile Switching** - Changes iTerm2 colors based on context (production = red!)
- ⚙️ **Claude Code Integration** - Manages settings, hooks, and auto-approvals
- 📊 **Status Bar** - Shows project info, git status, and session metrics
- 🚀 **Fast Setup** - Install in < 5 minutes with `uv` or `pipx`

---

## Quick Example

```bash
# Install with uv (recommended - 10-100x faster!)
uv tool install git+https://github.com/Data-Wise/aiterm

# Or with pipx
pipx install git+https://github.com/Data-Wise/aiterm

# Check health
aiterm doctor

# Detect current project
aiterm detect

# View Claude Code settings
aiterm claude settings

# List auto-approval presets
aiterm claude approvals presets
```

---

## Context Detection

**aiterm** automatically detects 8 project types:

| Context | Icon | Profile | When Detected |
|---------|------|---------|---------------|
| Production | 🚨 | Production | `/production/`, `/prod/` paths |
| AI Session | 🤖 | AI-Session | `/claude-sessions/`, `/gemini-sessions/` |
| R Package | 📦 | R-Dev | `DESCRIPTION` file present |
| Python | 🐍 | Python-Dev | `pyproject.toml` present |
| Node.js | 📦 | Node-Dev | `package.json` present |
| Quarto | 📊 | R-Dev | `_quarto.yml` present |
| Emacs | 🔧 | Dev-Tools | `.spacemacs` file |
| Dev Tools | 🛠️ | Dev-Tools | `.git` + `scripts/` |

---

## Features

### Context Management
- Detect project type from file markers and path patterns
- Apply context to terminal (profile, title, git status)
- Short aliases: `ait detect`, `ait switch`

### Claude Code Integration
- View and backup `~/.claude/settings.json`
- Manage auto-approval permissions with 8 presets:
  - `safe-reads` - Read-only operations
  - `git-ops` - Git commands (status, diff, log)
  - `github-cli` - GitHub CLI operations
  - `python-dev` - Python tools (pytest, pip, uv)
  - `node-dev` - Node.js tools (npm, npx, bun)
  - `r-dev` - R development tools
  - `web-tools` - Web search and fetch
  - `minimal` - Basic shell commands only

### Terminal Integration (iTerm2)
- Profile switching via escape sequences
- Tab title with project name and git branch
- Status bar variables for custom displays

---

## Installation

### Requirements

- **Python:** 3.10+
- **Terminal:** iTerm2 (macOS) - other terminals coming in v0.2.0
- **Optional:** Claude Code CLI, Gemini CLI

### Install with UV (Recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install aiterm
uv tool install git+https://github.com/Data-Wise/aiterm
```

**Why UV?** 10-100x faster than pip, compatible with everything, no lock file confusion.

### Install with pipx

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install aiterm
pipx install git+https://github.com/Data-Wise/aiterm
```

### Verify Installation

```bash
aiterm --version
aiterm doctor
```

---

## Quick Start

### 1. Basic Usage

```bash
# Check installation
aiterm doctor

# Detect current directory
aiterm detect

# Switch to another project
cd ~/my-python-project
aiterm switch    # Applies context to iTerm2
```

### 2. Claude Code Integration

```bash
# View current settings
aiterm claude settings

# Backup settings
aiterm claude backup

# View auto-approvals
aiterm claude approvals list

# Add safe preset
aiterm claude approvals add safe-reads

# Add development presets
aiterm claude approvals add python-dev
aiterm claude approvals add git-ops
```

### 3. Use Short Alias

```bash
ait detect      # Same as: aiterm detect
ait switch      # Same as: aiterm switch
ait doctor      # Same as: aiterm doctor
```

---

## Use Cases

### For Claude Code Users

```bash
# Set up safe auto-approvals
ait claude approvals add safe-reads
ait claude approvals add git-ops
ait claude approvals add python-dev

# Verify configuration
ait claude settings
```

### For Multi-Project Developers

```bash
# Navigate between projects with auto-context
cd ~/projects/my-webapp/
ait switch    # → Node-Dev profile (green)

cd ~/projects/api-service/
ait switch    # → Python-Dev profile (blue)

cd ~/production/live-site/
ait switch    # → Production profile (RED!) 🚨
```

### For R Package Developers

```bash
cd ~/r-packages/mypackage/
ait detect    # Shows: 📦 r-package → R-Dev profile

# Context includes:
# - Package name from DESCRIPTION
# - Git branch and dirty status
# - Profile colors optimized for R work
```

---

## What's Next?

### v0.2.0 (Coming Soon)

- **Hook Management** - Install and manage Claude Code hooks
- **MCP Server Integration** - Configure and test MCP servers
- **StatusLine Builder** - Interactive status bar generator
- **Multi-Terminal Support** - Beyond iTerm2

### Long Term (v1.0.0)

- **Gemini CLI Integration**
- **Profile Templates** - Community-contributed themes
- **Web UI** - Visual configuration tool
- **Plugin System** - Extend with custom contexts

---

## Links

- **Documentation:** [https://data-wise.github.io/aiterm](https://data-wise.github.io/aiterm)
- **Repository:** [https://github.com/Data-Wise/aiterm](https://github.com/Data-Wise/aiterm)
- **Issues:** [https://github.com/Data-Wise/aiterm/issues](https://github.com/Data-Wise/aiterm/issues)

---

## Why aiterm?

**Built for ADHD-friendly workflows:**

- ⚡ Fast commands with clear output
- 🎯 Single-purpose commands (no analysis paralysis)
- 🎨 Visual context cues (production = red!)
- 📝 Comprehensive docs with examples
- 🧪 Well-tested (51 tests, 83% coverage)

**Perfect for:**

- Claude Code power users
- Multi-project developers
- R package maintainers
- Production/staging separation
- ADHD-friendly workflows

---

## License

MIT - see [LICENSE](https://github.com/Data-Wise/aiterm/blob/main/LICENSE) for details.
