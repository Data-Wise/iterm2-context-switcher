# ROADMAP - Week 1 MVP

**Goal:** Transform iterm2-context-switcher → aiterm CLI tool

**Timeline:** 7 days
**Target Version:** v0.1.0
**User:** DT (primary user testing)

---

## Day 1-2: Project Setup & Architecture

### Tasks

- [x] ✅ Create IDEAS.md
- [x] ✅ Create ROADMAP.md
- [ ] Update all documentation
- [ ] Set up Python project structure
  ```
  aiterm/
  ├── pyproject.toml          # Poetry/pip config
  ├── src/aiterm/
  │   ├── __init__.py
  │   ├── cli/                # CLI commands
  │   │   └── main.py
  │   ├── terminal/           # Terminal detection
  │   │   ├── __init__.py
  │   │   └── iterm2.py
  │   ├── context/            # Context detection
  │   │   └── detector.py
  │   └── utils/
  ├── tests/
  └── templates/
      └── profiles/           # iTerm2 profiles
  ```
- [ ] Initialize git (rename/pivot existing repo)
- [ ] Set up Poetry/pip for dependencies
- [ ] Install Typer, Rich, Questionary

### Deliverable
- Clean project structure
- `poetry install` works
- Basic CLI runs: `aiterm --version`

---

## Day 3-4: Core Terminal Integration

### Tasks

#### Migrate Existing Code
- [ ] Port `zsh/iterm2-integration.zsh` → Python module
- [ ] Extract context detection logic
  - R packages (DESCRIPTION)
  - Python (pyproject.toml)
  - Node.js (package.json)
  - Quarto (_quarto.yml)
  - MCP (mcp-server/)
  - Production paths
  - AI sessions
  - Dev-tools
- [ ] Port profile definitions
- [ ] Migrate test suite (`scripts/test-context-switcher.sh`)

#### New CLI Commands
- [ ] `aiterm init` - Interactive setup
  ```python
  @app.command()
  def init():
      """Interactive setup wizard for aiterm"""
      # Detect terminal
      # Check shell (zsh)
      # Install integration script
      # Set up profiles
      # Test context switching
  ```

- [ ] `aiterm doctor` - Diagnostics
  ```python
  @app.command()
  def doctor():
      """Check aiterm installation and configuration"""
      # Terminal type
      # Shell integration
      # Profiles installed
      # Context detection working
      # Show fix suggestions
  ```

- [ ] `aiterm profile list|install|test`
  ```python
  profile_app = typer.Typer()

  @profile_app.command("list")
  def list_profiles():
      """List available profiles"""

  @profile_app.command("install")
  def install_profile(name: str):
      """Install a specific profile"""

  @profile_app.command("test")
  def test_profiles():
      """Test profile switching"""
  ```

### Deliverable
- `aiterm init` successfully sets up terminal
- `aiterm doctor` shows status
- Profile switching works
- Context detection works (all 8 types)

---

## Day 5: Claude Code Integration

### Tasks

#### Settings Management
- [ ] Read Claude Code settings file
  - Location: `~/.claude/settings.json`
  - Parse JSON
  - Validate structure

- [ ] `aiterm claude settings show`
  ```python
  @claude_app.command("settings")
  def show_settings():
      """Display current Claude Code settings"""
      # Read settings.json
      # Pretty print with Rich
  ```

- [ ] `aiterm claude settings backup`
  ```python
  @claude_app.command("backup")
  def backup_settings():
      """Backup Claude Code settings"""
      # Copy to ~/.claude/settings.backup.json
      # Timestamp
  ```

#### Auto-Approval Presets
- [ ] Define preset templates
  ```python
  PRESETS = {
      "safe-reads": [
          "Bash(cat:*)",
          "Bash(ls:*)",
          "Bash(find:*)",
          "Read(*)",
      ],
      "git-ops": [
          "Bash(git status:*)",
          "Bash(git log:*)",
          "Bash(git diff:*)",
      ],
      "dev-tools": [
          # Your current 40+ patterns
      ]
  }
  ```

- [ ] `aiterm claude approvals add-preset <name>`
  ```python
  @approvals_app.command("add-preset")
  def add_preset(name: str):
      """Add an auto-approval preset"""
      # Load preset
      # Merge with existing settings
      # Write back to settings.json
  ```

- [ ] `aiterm claude approvals list`
  ```python
  @approvals_app.command("list")
  def list_approvals():
      """Show current auto-approvals"""
      # Read from settings.json
      # Display in table (Rich)
  ```

### Deliverable
- Can read/write Claude Code settings
- Auto-approval presets working
- Settings backup feature

---

## Day 6: Testing & Documentation

### Tasks

#### Testing
- [ ] Port existing 15 tests
- [ ] Add new CLI command tests
  ```python
  def test_init_command():
      result = runner.invoke(app, ["init"])
      assert result.exit_code == 0

  def test_doctor_command():
      result = runner.invoke(app, ["doctor"])
      assert "Terminal:" in result.output
  ```
- [ ] Integration tests for iTerm2
- [ ] Test on DT's actual setup

#### Documentation
- [ ] Update README.md (v0.1 features)
- [ ] Write quickstart guide
- [ ] Command reference
- [ ] Troubleshooting guide

### Deliverable
- All tests passing
- Documentation complete
- Ready for personal use

---

## Day 7: Polish & Dogfooding

### Tasks

#### Polish
- [ ] Add Rich output (colors, tables, progress bars)
- [ ] Better error messages
- [ ] Input validation
- [ ] Shell completion (zsh)

#### Real-World Testing
- [ ] Install on DT's machine
- [ ] Use for 1 full day
- [ ] Track issues
- [ ] Fix critical bugs
- [ ] Iterate based on usage

#### Prepare for v0.2
- [ ] Create GitHub issues for Phase 2 features
- [ ] Document learnings
- [ ] Plan hook management system

### Deliverable
- v0.1.0 release
- DT using daily
- No regressions from old system
- Plan for v0.2 ready

---

## Success Criteria for MVP

### Must Have
- ✅ CLI installs cleanly (`pip install -e .`)
- ✅ `aiterm init` sets up terminal (< 5 minutes)
- ✅ `aiterm doctor` shows accurate status
- ✅ Context switching works (all 8 types)
- ✅ Profile switching works
- ✅ Can manage Claude Code auto-approvals
- ✅ Tests pass (>80% coverage)
- ✅ Documentation exists

### Should Have
- ✅ Fast startup (< 500ms)
- ✅ Good error messages
- ✅ Shell completion
- ✅ Rich CLI output

### Nice to Have
- Interactive prompts (questionary)
- Config file support
- Undo/rollback features
- Verbose/debug modes

---

## Risks & Mitigations

### Risk: iTerm2 API complexity
**Mitigation:** Start with escape sequences (already working), add Python API later

### Risk: Claude Code settings format changes
**Mitigation:** Version detection, backwards compatibility

### Risk: Scope creep
**Mitigation:** Stick to this roadmap, defer to Phase 2

### Risk: Testing on single machine
**Mitigation:** VM testing, ask colleague to test

---

## Post-MVP: Week 2 Preview

### Planned for v0.2 (Phase 2)
1. Hook management system
2. Command template library
3. MCP server integration
4. Advanced status bar builder

### Quick wins to add:
- `aiterm context show` - Current context info
- `aiterm quota set` - Integration with existing `qu` command
- `aiterm export` - Export config for backup

---

## Daily Standup Format

### Each Day:
**What I did:**
**What I'm doing today:**
**Blockers:**

Use `/recap` and `/next` to track progress!

---

## Resources

### Dependencies
- `typer` - CLI framework
- `rich` - Terminal formatting
- `questionary` - Interactive prompts
- `pyyaml` - Config files
- `pytest` - Testing

### Documentation
- Typer docs: https://typer.tiangolo.com/
- iTerm2 Python API: https://iterm2.com/python-api/
- Claude Code docs: https://claude.com/code

### Existing Code to Reference
- `zsh/iterm2-integration.zsh` (context detection)
- `scripts/test-context-switcher.sh` (test patterns)
- `statusline-alternatives/` (theme ideas)
- `.claude/settings.local.json` (auto-approvals)
