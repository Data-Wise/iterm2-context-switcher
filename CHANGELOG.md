# Changelog

All notable changes to iterm2-context-switcher will be documented in this file.

## [2.5.0] - 2025-12-15

### Added
- **Comprehensive test suite** - `scripts/test-context-switcher.sh`
  - Tests all 8 context detection scenarios
  - Validates profile switching and title/badge setting
  - Includes git dirty indicator testing
  - 15 test cases with full coverage
- **Statusline theme alternatives** - `statusline-alternatives/`
  - 3 color theme variants (cool-blues, forest-greens, purple-charcoal)
  - Preview and installation scripts
  - Theme comparison documentation
- **Expanded auto-approvals** - Updated `.claude/settings.local.json`
  - Added 40+ common safe commands (gh, mkdocs, find, grep, jq, etc.)
  - Reduces approval friction for routine operations

## [2.4.0] - 2025-12-14

### Added
- **Status Bar Integration** - Display context in iTerm2 status bar
  - `\(user.ctxIcon)` - Context icon (📦, 🐍, 🔧, etc.)
  - `\(user.ctxName)` - Project name
  - `\(user.ctxBranch)` - Git branch
  - `\(user.ctxProfile)` - Active profile name
- **Status bar documentation** - New docs/guide/status-bar.md with setup guide

### Changed
- Refactored detection to set user variables alongside profile/title
- Variables update on every directory change

## [2.3.0] - 2025-12-14

### Added
- **iTerm2 Triggers for Claude Code** - Auto-notifications in AI-Session profile
  - Bounce Dock Icon when tool approval needed (`Allow .+?`)
  - Highlight errors in red (`Error:|error:|failed`)
  - macOS notification on `/cost` command
  - Highlight success markers in green (`✓|completed`)
- **Trigger documentation** - Updated docs/guide/triggers.md with customization guide

### Changed
- AI-Session profile now includes built-in triggers
- Triggers activate automatically when using AI-Session profile

## [2.2.0] - 2025-12-14

### Added
- **Git branch in title** - Shows current branch: `📦 medfit (main)`
- **Git dirty indicator** - Shows `*` when uncommitted changes: `📦 medfit (main)*`
- **Install script** - `scripts/install-profiles.sh` for easy setup
- **Profiles in repo** - `profiles/context-switcher-profiles.json` for distribution

### Changed
- Titles now include git info for all contexts
- Long branch names truncated (>20 chars)

## [2.1.0] - 2025-12-14

### Added
- **Dynamic Profiles** - Auto-installed color themes for all project types
  - R-Dev: Blue theme 📦
  - AI-Session: Purple theme 🤖
  - Production: Red theme 🚨
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
- Production warning sound/bell
- Smart triggers for test results

---

**Project Status:** Complete (v2.4.0)
**Live Docs:** https://data-wise.github.io/iterm2-context-switcher/
