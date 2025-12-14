# Changelog

All notable changes to iterm2-context-switcher will be documented in this file.

## [2.1.0] - 2025-12-14

### Added
- **Dynamic Profiles** - Auto-installed color themes for all project types
  - Dev-Tools: Amber/orange theme 🔧
  - Emacs: Purple/magenta theme ⚡
  - Python-Dev: Green theme 🐍
  - Node-Dev: Dark theme 📦
- **Quarto profile switching** - Uses R-Dev profile (blue theme) 📊
- **MCP profile switching** - Uses AI-Session profile 🔌
- **Emacs profile switching** - New dedicated purple theme ⚡

### Changed
- All project types now have profile + icon switching
- Profiles auto-load via iTerm2 Dynamic Profiles

## [2.0.1] - 2025-12-14

### Added
- **Dev-Tools profile** - New profile for dev-tools projects with 🔧 icon
- **scripts/ detection** - Dev-tools now detected by `scripts/` directory (not just `commands/`)

### Fixed
- **Shared detector bypass** - Skip generic "project" type, use local detection for specifics
- **False positive fix** - Require `.git` for dev-tools detection (prevents `~/scripts` false positive)
- **iTerm2 title setting** - Profiles must use "Session Name" for escape sequences to work

### Changed
- Detection now more specific: dev-tools requires git repo + commands/ or scripts/

## [2.0.0] - 2025-12-14

### Added
- **MkDocs documentation site** - Material theme, dark/light toggle
- **GitHub Pages deployment** - Auto-deploy on push to main
- **Tab title support** - Icons + project names in tab title
- **Profile caching** - Prevents redundant profile switches
- **Hook registration guard** - Prevents duplicate hooks
- **New commands** (in ~/.claude/commands/):
  - `/mkdocs-init` - Create new documentation site
  - `/mkdocs` - Status and actions menu
  - `/mkdocs-preview` - Quick preview

### Changed
- **Removed badges** - Using tab titles instead (more reliable)
- **Simplified detection** - File-based only, no glob patterns
- **OSC 2 for titles** - Window title escape sequence
- **Emacs detection** - Now checks `Cask`, `.dir-locals.el`, `init.el`, `early-init.el`
- **Dev-tools detection** - Checks for `commands/` directory

### Fixed
- Loop issues with badge escape sequences
- OMZ title conflicts (DISABLE_AUTO_TITLE)
- Profile switch escape sequence format (`it2profile -s`)

### Documentation
- 7 documentation pages covering installation, guides, and reference
- Live site: https://data-wise.github.io/iterm2-context-switcher/

## [1.1.0] - 2025-12-13

### Added
- **Git dirty indicator** - Badges now show `✗` when repo has uncommitted changes
- **New context patterns:**
  - Python projects (`pyproject.toml`) → Python-Dev profile
  - Node.js projects (`package.json`) → Node-Dev profile
  - Quarto projects (`_quarto.yml`) → 📊 icon
  - MCP server projects → 🔌 icon
  - Emacs Lisp projects → ⚡ icon
- **Verification script** - `scripts/verify-setup.sh`

### Changed
- Refactored main function with clear priority sections
- Improved code organization with helper functions

## [1.0.0] - 2025-12-13

### Added
- Initial project structure
- Core auto-switching integration (iterm2-integration.zsh)
- Profile creation guide
- Setup guide with verification tests
- ADHD-friendly quick reference

## [Unreleased]

### Planned
- Git branch in tab title (`📦 medfit (main)`)
- iTerm2 triggers for Claude Code notifications
- Status bar integration

---

**Project Status:** Complete (v2.1.0)
**Live Docs:** https://data-wise.github.io/iterm2-context-switcher/
