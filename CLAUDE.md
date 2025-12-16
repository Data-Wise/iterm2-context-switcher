# CLAUDE.md

This file provides guidance to Claude Code when working with the aiterm project.

## Project Overview

**aiterm** (formerly iterm2-context-switcher) - Terminal optimizer CLI for AI-assisted development with Claude Code and Gemini CLI.

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

## Project Status: Week 1 MVP (v0.1.0-dev)

**Current Phase:** First feature shipped (@smart prompt optimizer)!

**Progress:**
- [x] Planning complete (IDEAS.md, ROADMAP.md, ARCHITECTURE.md)
- [x] @smart Prompt Optimizer (Tier 1 MVP) ✅ IMPLEMENTED!
- [ ] Python project structure
- [ ] Core CLI commands (init, doctor)
- [ ] Terminal integration (migrate from zsh)
- [ ] Claude Code settings management
- [ ] Testing & documentation

**This Week's Goals:**
1. Set up Python project structure (Poetry/pip)
2. Migrate zsh integration to Python
3. Build core CLI commands (init, doctor, profile, claude)
4. Port existing test suite
5. Get DT using it daily

See `ROADMAP.md` for detailed day-by-day plan.

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

---

## Integration with DT's Existing Setup

**Existing Tools:**
- `~/.claude/statusline-p10k.sh` - Status bar (will integrate)
- `~/.claude/settings.json` - Claude Code config (will manage)
- `~/.config/zsh/functions.zsh` - Shell functions (will complement)

**Workflow Commands:**
- `/recap`, `/next`, `/focus` - ADHD-friendly workflow (will enhance)
- `work`, `finish`, `dash`, `pp` - Project management (will integrate with context)

**MCP Servers:**
- Statistical Research MCP (14 tools, 17 skills)
- Shell MCP server
- Filesystem MCP
- (aiterm will help configure these)

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
- MCP server integration
- Advanced status bar builder

---

## Key Constraints

1. **ADHD-Friendly:** Fast commands, clear output, no analysis paralysis
2. **Week 1 MVP:** Ship v0.1.0 in 7 days, DT using daily
3. **No Regressions:** Must work as well as v2.5.0 zsh version
4. **Python 3.10+:** Modern Python, type hints, async-ready
5. **Medium Integration:** Active control, not just config files

---

## Detailed Documentation

Detailed docs have been split into focused rule files in `.claude/rules/`:

- **architecture.md** - System architecture, file structure, design principles
- **migration.md** - Code migration from v2.5.0 (zsh → Python)
- **development.md** - Development workflow, testing, adding commands

These files load automatically when working in relevant paths.

---

## Success Criteria

### MVP (v0.1.0)
- [ ] Installs in <5 minutes
- [ ] `aiterm init` sets up terminal
- [ ] Context switching works (8 types)
- [ ] Claude Code auto-approvals manageable
- [ ] Tests pass (>80% coverage)
- [ ] DT uses daily for 1 week

### Long-term (v1.0.0)
- [ ] Multi-terminal support
- [ ] 10+ external users
- [ ] Community templates
- [ ] Web UI option
- [ ] Featured in Claude Code docs

---

**Remember:** This is a pivot from a working project. The zsh integration still works. We're rebuilding in Python for expandability!
