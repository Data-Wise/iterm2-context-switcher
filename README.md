# aiterm

**Terminal Optimizer for AI-Assisted Development**

Optimize your terminal (iTerm2+) for AI coding with Claude Code and Gemini CLI. Manage profiles, contexts, hooks, commands, and auto-approvals from one powerful CLI.

---

## 🚀 Quick Start

```bash
# Install (coming soon - PyPI)
pip install aiterm

# Interactive setup
aiterm init

# Check your setup
aiterm doctor
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

### Current (v0.1.0-dev)

- [x] **Planning Complete** - Roadmap, architecture, docs ready
- [ ] **Context Detection** - 8 project types (R, Python, Node, etc.)
- [ ] **Profile Management** - Install, list, test terminal profiles
- [ ] **Claude Code Settings** - Manage auto-approvals and configuration
- [ ] **Diagnostics** - `aiterm doctor` health checks

### Coming Soon (v0.2+)

- Hook management system
- Command template library
- MCP server integration
- Gemini CLI support
- Multi-terminal support (Warp, Alacritty, Kitty)
- Web UI configuration builder

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
- **Distribution:** pip/PyPI

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
git clone https://github.com/Data-Wise/iterm2-context-switcher.git
cd iterm2-context-switcher

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Try CLI
aiterm --help
```

### Project Status
**Version:** 0.1.0-dev (Week 1 MVP in progress)
**Status:** Active development
**Target:** DT using daily by end of week

See [ROADMAP.md](ROADMAP.md) for current progress.

---

## 📜 History

**v2.5.0 (Dec 15, 2024):** iterm2-context-switcher
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
- PyPI distribution
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
**Repo:** https://github.com/Data-Wise/iterm2-context-switcher

---

**Status:** 🚧 Active Development (Week 1 MVP)
**Next Milestone:** v0.1.0 - Basic CLI + terminal integration
**See:** [ROADMAP.md](ROADMAP.md) for current tasks
