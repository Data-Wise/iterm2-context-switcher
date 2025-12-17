# TODOS - aiterm

Tasks and next steps for the aiterm project.

**Updated:** 2025-12-17
**Version:** 0.1.0-dev

---

## Completed (December 2025)

- [x] ✅ Created comprehensive Claude Code CLI tutorial (3,266 lines)
  - 16 sections covering all features
  - ADHD-friendly workflows and tips
  - Plugins & Marketplaces guide with vetting checklist
  - Plain English explanations for beginners
  - DT's workflow applications throughout
- [x] ✅ Documented Claude Code plugins system
- [x] ✅ Added terminal setup guides (iTerm2, VS Code, Terminal.app)

---

## Immediate (Current Sprint)

- [x] ✅ Add Claude Code tutorial to MkDocs site
- [ ] Preview and verify MkDocs build
- [ ] Push tutorial to dev branch
- [ ] Merge dev → main
- [ ] Tag v0.1.0-dev release

---

## v0.1.1 (Bug Fixes & Polish)

- [ ] Implement full `aiterm init` wizard (currently placeholder)
- [ ] Add more detailed `aiterm doctor` diagnostics
- [ ] Add `aiterm profile install` command
- [ ] Add `aiterm profile test` command
- [ ] Shell integration script for zsh/bash

---

## v0.2.0 (Hook Management)

- [ ] `aiterm claude hooks list` - Show available hooks
- [ ] `aiterm claude hooks install <name>` - Install from template
- [ ] `aiterm claude hooks create <name>` - Interactive hook creator
- [ ] `aiterm claude hooks validate` - Check hook syntax
- [ ] `aiterm claude hooks enable/disable <name>` - Toggle hooks

**Hook Templates:**
- [ ] block-sensitive-files (PreToolUse)
- [ ] quota-display (SessionStart)
- [ ] test-runner (PostToolUse)
- [ ] context-injector (UserPromptSubmit)

---

## v0.3.0 (MCP & Commands)

- [ ] `aiterm mcp list` - Show configured MCP servers
- [ ] `aiterm mcp install <server>` - Install + configure
- [ ] `aiterm mcp test <server>` - Test connection
- [ ] `aiterm claude commands list` - Show custom commands
- [ ] `aiterm claude commands create` - From template

---

## v0.4.0 (Multi-Terminal & Gemini)

- [ ] Warp terminal support
- [ ] Alacritty support
- [ ] Kitty support
- [ ] `aiterm gemini init` - Gemini CLI integration
- [ ] `aiterm switch claude|gemini` - Switch AI tools

---

## Technical Debt

- [ ] Increase test coverage to 90%+
- [ ] Add integration tests for iTerm2
- [ ] Add type hints throughout
- [ ] Add docstrings to all functions
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Pre-commit hooks (ruff, mypy, black)

---

## Documentation

- [x] ✅ Claude Code CLI comprehensive tutorial (docs/CLAUDE-CODE-TUTORIAL.md)
- [x] ✅ ADHD-friendly workflow guide (Section 16 of tutorial)
- [x] ✅ Plugin vetting guide and recommendations
- [ ] Quickstart video tutorial
- [ ] Update MkDocs site with v0.1.0 features
- [ ] API documentation
- [ ] Contributing guide
- [ ] Recipe book (common patterns)

---

## Distribution

- [ ] Publish to PyPI
- [ ] Homebrew formula
- [ ] Docker image (optional)

---

## Community

- [ ] GitHub discussions enabled
- [ ] Issue templates
- [ ] PR template
- [ ] Example gallery

---

## Long-term Ideas (v1.0+)

See IDEAS.md for full roadmap:
- Web UI (Streamlit)
- Template marketplace
- AI workflow optimizer
- Cross-tool intelligence
- VSCode extension
