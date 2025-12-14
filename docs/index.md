# iTerm2 Context Switcher

**Smart context switching for iTerm2 with auto-profile switching and tab titles.**

**Version:** 2.1.0

---

## What It Does

Automatically switches iTerm2 profiles (colors) and sets tab titles based on your current directory:

| Context | Icon | Profile | Theme |
|---------|------|---------|-------|
| Production | 🚨 | Production | Red |
| AI Sessions | 🤖 | AI-Session | Purple |
| R Package | 📦 | R-Dev | Blue |
| Python | 🐍 | Python-Dev | Green |
| Node.js | 📦 | Node-Dev | Dark |
| Quarto | 📊 | R-Dev | Blue |
| MCP Server | 🔌 | AI-Session | Purple |
| Emacs | ⚡ | Emacs | Purple |
| Dev-Tools | 🔧 | Dev-Tools | Amber |

---

## Features

- ✅ Auto-switch profiles by directory context
- ✅ Tab titles with icons (📦 medfit, 🐍 myproject)
- ✅ Production environment warnings (🚨)
- ✅ Dynamic profiles auto-installed (no manual setup)
- ✅ Caches state to prevent redundant switches
- ✅ No conflicts with other shell hooks
- ✅ Zero configuration after setup

---

## Quick Start

```bash
# Add to ~/.config/zsh/.zshrc (before Oh-My-Zsh loads)
DISABLE_AUTO_TITLE="true"

# At end of .zshrc
source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

**Important:** Set each iTerm2 profile's Title to "Session Name" in Preferences.

Then reload your shell:

```bash
source ~/.config/zsh/.zshrc
```

See the [Installation Guide](getting-started/installation.md) for detailed setup.

---

## How It Works

When you `cd` into a directory, the integration:

1. **Detects context** - Checks for project files (DESCRIPTION, pyproject.toml, etc.)
2. **Switches profile** - Changes iTerm2 colors via escape sequence
3. **Sets title** - Updates tab title with icon + project name

All changes are cached to prevent redundant switches.

---

## Dynamic Profiles

Color profiles are automatically installed via iTerm2 Dynamic Profiles:

- **Dev-Tools** - Amber/orange theme for shell tools
- **Emacs** - Purple/magenta theme for Emacs configs
- **Python-Dev** - Green theme for Python projects
- **Node-Dev** - Dark theme for Node.js projects

See [Profiles Guide](guide/profiles.md) for customization.
