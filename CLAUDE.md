# CLAUDE.md

This file provides guidance to Claude Code when working with the aiterm project.

## Project Overview

**aiterm** (formerly aiterm) - Terminal optimizer CLI for AI-assisted development with Claude Code and Gemini CLI.

**What it does:**
- Optimizes terminal setup (iTerm2 primarily) for AI coding workflows
- Manages terminal profiles, context detection, and visual customization
- Integrates with Claude Code CLI (hooks, commands, auto-approvals, MCP servers)
- Supports Gemini CLI integration
- Provides workflow templates for different dev contexts

**Target Users:**
- Primary: DT (power user, R developer, statistician, ADHD-friendly workflows)
- Secondary: Public release (developers using Claude Code/Gemini CLI)

**Tech Stack:**
- **Language:** Python 3.10+
- **CLI Framework:** Typer (modern CLI with type hints)
- **Terminal:** Rich (beautiful terminal output)
- **Prompts:** Questionary (interactive prompts)
- **Testing:** pytest
- **Distribution:** pip/PyPI

---

## Project Status: v0.2.0-dev - Documentation First! 📚

**Current Phase:** Phase 0 - Comprehensive Documentation (Before Feature Expansion)

**NEW PRIORITY (Dec 21, 2025):**
After completing RForge MCP auto-detection documentation (7 docs, ~80 pages, 15 diagrams), we've validated a critical insight:

> **Comprehensive documentation BEFORE feature expansion prevents confusion and accelerates development.**

**Phase 0 Plan (3 weeks):**
- [ ] Complete documentation suite (7 documents, ~100 pages)
- [ ] 20+ Mermaid architecture diagrams
- [ ] 60+ code examples (Python + CLI)
- [ ] Deploy to GitHub Pages
- [ ] Use docs as specification for Phase 1 implementation

**See:**
- `DOCUMENTATION-PLAN.md` - Complete documentation roadmap
- `RFORGE-LEARNINGS.md` - Lessons from RForge success
- `IMPLEMENTATION-PRIORITIES.md` - Updated with documentation-first approach

---

## v0.1.0 Achievements ✅

**Completed (Dec 2024):**
- [x] UV build system and virtual environment
- [x] Python project structure (hatchling, src/ layout)
- [x] Core CLI commands (doctor, detect, switch)
- [x] Terminal integration (iTerm2 escape sequences)
- [x] Claude Code settings management
- [x] Auto-approval presets (8 presets)
- [x] Testing & documentation (51 tests, 83% coverage)
- [x] Basic docs (2,647 lines, deployed to GitHub Pages)
- [x] Repository renamed to "aiterm"

**Links:**
- **Repo:** https://github.com/Data-Wise/aiterm
- **Docs:** https://Data-Wise.github.io/aiterm/
- **Status:** v0.1.0 released, v0.2.0 in planning

---

## Next: Phase 1 Implementation (After Docs)

**After Phase 0 documentation complete:**
- Implement `rforge:plan` (main ideation tool)
- Implement `rforge:plan:quick-fix` (fast iterations)
- 2 weeks to working MVP
- Validate pattern with real usage

---

## Quick Reference

### Common Commands

```bash
# Development
aiterm --help                    # See available commands
aiterm doctor                    # Check installation
python -m pytest                 # Run tests

# Testing existing functionality
cd ~/test-dir
# (zsh integration still works for now)
```

### Key Files

- `IDEAS.md` - Full feature brainstorm
- `ROADMAP.md` - Week 1 day-by-day plan
- `ARCHITECTURE.md` - Technical design
- `.STATUS` - Current progress
- `zsh/` and `scripts/` - Existing code (reference)
- `MCP-MIGRATION-PLAN.md` - Complete MCP organization plan (2025-12-19)

---

## Integration with DT's Existing Setup

**Existing Tools:**
- `~/.claude/statusline-p10k.sh` - Status bar (will integrate)
- `~/.claude/settings.json` - Claude Code config (will manage)
- `~/.config/zsh/functions.zsh` - Shell functions (will complement)

**Workflow Commands:**
- `/recap`, `/next`, `/focus` - ADHD-friendly workflow (will enhance)
- `work`, `finish`, `dash`, `pp` - Project management (will integrate with context)

**MCP Servers (Now Organized!):**
- **Location:** `~/projects/dev-tools/mcp-servers/` (unified, 2025-12-19)
- **Servers:** statistical-research, shell, project-refactor
- **ZSH Tools:** `mcp-list`, `mcp-cd`, `mcp-test`, `mcp-status` (+ 6 more)
- **Aliases:** `ml` (list), `mc` (cd), `mcps` (status), `mcpp` (picker)
- **Index:** `~/projects/dev-tools/_MCP_SERVERS.md`
- **Config:** `~/.claude/settings.json`, `claude-mcp/MCP_SERVER_CONFIG.json`
- **Planned for aiterm v0.2.0:** `aiterm mcp list|test|validate`

**@smart Feature (NEW!):**
- UserPromptSubmit hook: `~/.claude/hooks/prompt-optimizer.sh`
- Optimizes prompts with project context
- Interactive menu: Submit/Revise/Delegate/Cancel
- Docs: `~/.claude/PROMPT-OPTIMIZER-GUIDE.md`

---

## Current Limitations & Next Steps

### MVP Limitations (v0.1.0)
- iTerm2 only (no multi-terminal yet)
- Basic Claude Code integration (settings only, no hooks/commands managed)
- No Gemini integration yet
- No web UI
- Manual installation

### Planned for v0.2.0 (Phase 2)
- Hook management system
- Command template library
- **MCP server integration** (foundation ready: zsh-configuration/zsh/functions/mcp-utils.zsh)
  - `aiterm mcp list` - Show all configured servers
  - `aiterm mcp status` - Check server health
  - `aiterm mcp test <server>` - Validate server runs
  - `aiterm mcp validate` - Check configs are valid
- Advanced status bar builder

---

## Key Constraints

1. **ADHD-Friendly:** Fast commands, clear output, no analysis paralysis
2. **Week 1 MVP:** Ship v0.1.0 in 7 days, DT using daily
3. **No Regressions:** Must work as well as v2.5.0 zsh version
4. **Python 3.10+:** Modern Python, type hints, async-ready
5. **Medium Integration:** Active control, not just config files

---

## Project Standards

**See:** `STANDARDS-SUMMARY.md` - Comprehensive standards for aiterm project

**Based on:** zsh-configuration standards (`~/projects/dev-tools/zsh-configuration/standards/`)

**Key Standards:**
- **Project Organization:** .STATUS file, directory structure, universal files
- **Documentation:** QUICK-START, REFCARD, TUTORIAL templates (ADHD-friendly)
- **Commit Messages:** Conventional commits (type(scope): subject)
- **Testing:** 80%+ coverage goal, arrange-act-assert pattern
- **Development:** Branch strategy, pre-commit checklist, release process

**Quick Access:**
```bash
# View all standards
cat STANDARDS-SUMMARY.md

# Reference templates
cat standards/adhd/QUICK-START-TEMPLATE.md
cat standards/adhd/REFCARD-TEMPLATE.md
cat standards/adhd/TUTORIAL-TEMPLATE.md

# Code standards
cat standards/code/COMMIT-MESSAGES.md
```

---

## Detailed Documentation

Detailed docs have been split into focused rule files in `.claude/rules/`:

- **architecture.md** - System architecture, file structure, design principles
- **migration.md** - Code migration from v2.5.0 (zsh → Python)
- **development.md** - Development workflow, testing, adding commands

These files load automatically when working in relevant paths.

---

## Success Criteria

### MVP (v0.1.0) ✅ COMPLETE
- [x] Installs in <5 minutes (with UV: < 2 minutes!)
- [x] Context switching works (8 types)
- [x] Claude Code auto-approvals manageable (8 presets)
- [x] Tests pass (51/51, 83% coverage)
- [x] Comprehensive documentation deployed
- [ ] `aiterm init` wizard (deferred to v0.2.0)
- [ ] DT uses daily for 1 week (testing in progress)

### Long-term (v1.0.0)
- [ ] Multi-terminal support
- [ ] 10+ external users
- [ ] Community templates
- [ ] Web UI option
- [ ] Featured in Claude Code docs

---

**Remember:** This is a pivot from a working project. The zsh integration still works. We're rebuilding in Python for expandability!
