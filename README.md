# aiterm

**Terminal Optimizer for AI-Assisted Development**

Optimize your terminal (iTerm2+) for AI coding with Claude Code and Gemini CLI. Manage profiles, contexts, hooks, commands, and auto-approvals from one powerful CLI.

---

## 🚀 Installation

### macOS (Recommended)

```bash
# Install from Homebrew tap
brew install data-wise/tap/aiterm

# Update to latest version
brew upgrade aiterm
```

### All Platforms (uv - fastest)

```bash
# Install uv first (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install aiterm globally
uv tool install aiterm                    # from PyPI (after publish)
uv tool install git+https://github.com/Data-Wise/aiterm
```

### Alternative: pipx

```bash
# Install pipx first (if needed)
brew install pipx && pipx ensurepath

# Install aiterm globally
pipx install aiterm                       # from PyPI (after publish)
pipx install git+https://github.com/Data-Wise/aiterm
```

### From source (development)

```bash
git clone https://github.com/Data-Wise/aiterm.git
cd aiterm
uv tool install .                         # or: pip install -e .
```

### Installation Methods Comparison

| Method | Platform | Speed | Updates | Best For |
|--------|----------|-------|---------|----------|
| **Homebrew** | macOS | Fast | `brew upgrade` | Mac users (recommended) |
| **uv** | All | Fastest | `uv tool upgrade` | All platforms |
| **pipx** | All | Fast | `pipx upgrade` | Python developers |
| **Source** | All | Slow | `git pull` | Contributors |

---

## 🎯 Quick Start

```bash
# Check your setup
ait doctor

# Detect project context
ait detect

# View Claude Code settings
ait claude settings
```

---

## ✨ What It Does

**aiterm** makes your terminal intelligent for AI-assisted development:

### 🎨 Context-Aware Profiles
Automatically switch terminal colors and titles based on your project:

| Context | Icon | Profile | Triggered By |
|---------|------|---------|--------------|
| Production | 🚨 | Red theme | `*/production/*` path |
| AI Sessions | 🤖 | Purple theme | `*/claude-sessions/*` |
| R Packages | 📦 | Blue theme | `DESCRIPTION` file |
| Python | 🐍 | Green theme | `pyproject.toml` |
| Node.js | 📦 | Dark theme | `package.json` |
| Quarto | 📊 | Blue theme | `_quarto.yml` |

### 🛠️ Claude Code Integration
- Manage hooks (session-start, pre-commit, cost-tracker)
- Install command templates (/recap, /next, /focus)
- Configure auto-approvals (safe-reads, git-ops, dev-tools)
- Control MCP servers

### 📊 Status Bar Customization
Build custom status bars with:
- Project icon & name
- Git branch + dirty indicator
- API quota tracking
- Time in context
- Custom components

---

## 💡 Features

### Implemented (v0.1.0-dev)

- [x] **Context Detection** - 8 project types with auto-switching
- [x] **iTerm2 Integration** - Profiles, titles, user variables
- [x] **Claude Code Settings** - View, backup, manage approvals
- [x] **Auto-Approval Presets** - 8 ready-to-use presets
- [x] **Diagnostics** - `aiterm doctor` health checks
- [x] **Short Aliases** - `ait` for quick access

### CLI Commands

```bash
# Core commands
ait --version          # Show version
ait doctor             # Health check
ait detect             # Detect project context
ait switch             # Apply context to terminal

# Context detection
ait context detect     # Show project type, git info
ait context apply      # Apply to iTerm2

# Claude Code settings
ait claude settings    # Show settings
ait claude backup      # Backup settings

# Auto-approvals
ait claude approvals list      # List permissions
ait claude approvals presets   # Show 8 presets
ait claude approvals add <preset>  # Add preset
```

### Coming Soon (v0.2+)

- Hook management system
- Command template library
- MCP server integration
- Gemini CLI support

See [IDEAS.md](IDEAS.md) for full roadmap.

---

## 🏗️ Architecture

### CLI-First Design
```
aiterm/
├── Core Library      # Business logic, testable
├── CLI Layer         # Typer commands
└── Templates         # Profiles, hooks, commands
```

### Tech Stack
- **Language:** Python 3.10+
- **CLI:** Typer (modern, type-safe)
- **Output:** Rich (beautiful tables, colors)
- **Testing:** pytest
- **Distribution:** uv/pipx/PyPI

---

## 📖 Documentation

- **[IDEAS.md](IDEAS.md)** - Feature brainstorm & roadmap
- **[ROADMAP.md](ROADMAP.md)** - Week 1 MVP plan (day-by-day)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design
- **[CLAUDE.md](CLAUDE.md)** - Guidance for Claude Code
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎯 Use Cases

### For R Developers
```bash
cd ~/projects/r-packages/medfit
# Terminal switches to R-Dev profile (blue)
# Title shows: 📦 medfit (main)
# Status bar shows quota usage
```

### For AI Power Users
```bash
aiterm claude approvals add-preset safe-reads
aiterm claude hooks install session-start
aiterm context history  # See where you've been today
```

### For Multi-Project Workflows
```bash
# Automatic profile switching as you navigate
cd ~/production/app          # → Red theme, production warnings
cd ~/claude-sessions/        # → Purple theme, AI optimized
cd ~/projects/research/      # → Default theme, research context
```

---

## 🔧 Development

### Setup
```bash
# Clone repo
git clone https://github.com/Data-Wise/aiterm.git
cd aiterm

# Set up environment (using uv - recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Or traditional pip
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Try CLI
aiterm --help
```

### Project Status
**Version:** 0.1.0-dev (95% complete)
**Tests:** 51 passing, 83% coverage
**Status:** Active development

See [ROADMAP.md](ROADMAP.md) for current progress.

---

## 📜 History

**v2.5.0 (Dec 15, 2024):** aiterm
- zsh-based terminal integration
- 8 context types
- iTerm2 status bar support
- Comprehensive test suite (15 tests)

**v3.0.0 (Dec 15, 2024):** Pivot to **aiterm**
- Python CLI architecture
- Claude Code deep integration
- Multi-tool support (Gemini)
- Expandable plugin system

---

## 🤝 Contributing

Not accepting external contributions yet (MVP phase). Check back at v1.0!

**Target for public release:**
- Multi-terminal support
- Documentation site
- PyPI + uv/pipx distribution
- Community templates

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

Built for AI-assisted development workflows with:
- [Claude Code](https://claude.com/code) - Anthropic's CLI tool
- [Gemini CLI](https://ai.google.dev/) - Google's AI CLI
- [iTerm2](https://iterm2.com/) - macOS terminal emulator

---

## 📧 Contact

**Author:** DT
**Project:** Part of the Data-Wise development toolkit
**Repo:** https://github.com/Data-Wise/aiterm

---

**Status:** 🚧 Active Development (95% complete)
**Tests:** 51 passing, 83% coverage
**See:** [ROADMAP.md](ROADMAP.md) for current tasks
