# IDEAS - Terminal Optimizer for AI Coding

**Project Vision:** CLI tool for optimizing terminals (iTerm2+) for AI-assisted development with Claude Code and Gemini CLI.

**Target Users:**
- Primary: DT (power user, R developer, statistician)
- Secondary: Public release (developers using Claude Code/Gemini)

**Tech Stack:**
- Language: Python
- CLI Framework: Typer
- Terminal API: iTerm2 Python API
- Distribution: pip installable

---

## Phase 1: MVP (Week 1) - v0.1.0 ✅ COMPLETE

**Goal:** Working CLI that improves on current aiterm
**Status:** ✅ COMPLETE (2025-12-16)

### Core Features

#### 1. Setup & Diagnostics ✅
- [x] ✅ `aiterm init` - Interactive setup wizard (placeholder)
- [x] ✅ `aiterm doctor` - Health check (terminal, shell, Python, version)
- [x] ✅ `aiterm --version` - Show version info

#### 2. Terminal Optimization ✅
- [x] ✅ Migrated iterm2-integration.zsh → Python
- [x] ✅ Profile management commands
  - `aiterm profile list` - List available profiles
- [x] ✅ Context detection (8 types)
  - `aiterm detect` / `aiterm context detect`
  - `aiterm switch` / `aiterm context apply`
  - Production 🚨, AI-Session 🤖, R-Pkg 📦, Python 🐍, Node 📦, Quarto 📊, Emacs ⚡, Dev-Tools 🔧

#### 3. Basic Claude Code Integration ✅
- [x] ✅ Settings file management
  - `aiterm claude settings` - Show settings
  - `aiterm claude backup` - Timestamped backup
- [x] ✅ Auto-approval presets (8 presets)
  - `aiterm claude approvals add <preset>` - Add preset
  - `aiterm claude approvals list` - Show permissions
  - `aiterm claude approvals presets` - List all presets
  - Presets: safe-reads, git-ops, github-cli, python-dev, node-dev, r-dev, web-tools, minimal

#### 4. Testing ✅
- [x] ✅ Port existing test suite → pytest
- [x] ✅ Add CLI command tests (test_cli.py)
- [x] ✅ Context detection tests (test_context.py)
- [x] ✅ iTerm2 tests (test_iterm2.py)
- [x] ✅ Claude settings tests (test_claude_settings.py)
- [x] ✅ **Result:** 51 tests, 83% coverage

---

## Phase 2: Enhanced Claude Integration (v0.2.0-v0.2.1) ✅ COMPLETE

**Goal:** Deep Claude Code customization + Distribution
**Status:** ✅ COMPLETE (2025-12-26)

### v0.2.0 Delivered (Dec 24, 2025):
- [x] Hook Management System (580 lines)
- [x] Command Library System (600 lines)
- [x] MCP Server Integration (513 lines)
- [x] Documentation Helpers (715 lines)

### v0.2.1 Delivered (Dec 26, 2025):
- [x] **PyPI Publishing:** https://pypi.org/project/aiterm-dev/
- [x] **Homebrew Fixed:** All transitive dependencies
- [x] **Trusted Publishing:** GitHub Actions OIDC
- [x] **9 New REFCARDs:** Claude, MCP, Hooks, Context, OpenCode
- [x] **CLI Improvements:** 19 commands with epilog examples

### Original Planning (Reference)

**NEW: R-Development MCP Consolidation** ⭐
- **Discovery:** 59% of Claude commands (35/59) are R-ecosystem related!
- **Strategy:** Rename `statistical-research` → `r-development` MCP
- **Add 6 new R tools:**
  - r_ecosystem_health (MediationVerse health check)
  - r_package_check_quick (quick R package check)
  - manuscript_section_writer (write statistical papers)
  - reviewer_response_generator (respond to reviewers)
  - pkgdown_build (R package documentation)
  - pkgdown_deploy (deploy to GitHub Pages)
- **Result:** 14 → 20 tools (+43%), comprehensive R toolkit
- **See:** COMMAND-MCP-REFACTORING-ANALYSIS-REVISED.md

### NEW KNOWLEDGE: 9 Hook Types Available!
- PreToolUse (block/approve tools before execution)
- PermissionRequest (auto-approve/deny dialogs)
- PostToolUse (actions after tool completion)
- UserPromptSubmit (add context to prompts)
- Notification (custom alerts)
- Stop/SubagentStop (control when Claude stops)
- PreCompact (before context compaction)
- SessionStart (initialize sessions)
- SessionEnd (cleanup and logging)

### Features

#### 1. Hook Management
- [ ] `aiterm claude hooks list` - Show available hooks and their configs
- [ ] `aiterm claude hooks install <name>` - Install from template library
- [ ] `aiterm claude hooks create <name>` - Interactive hook creator
- [ ] `aiterm claude hooks validate` - Check hook syntax and behavior
- [ ] `aiterm claude hooks test <name>` - Dry-run hook with sample data
- [ ] `aiterm claude hooks enable/disable <name>` - Toggle hooks

**Hook Template Library:**
- **PreToolUse Hooks:**
  - block-sensitive-files (prevent .env, credentials access)
  - validate-bash-commands (security checks)
  - cost-estimator (warn before expensive operations)
- **SessionStart Hooks:**
  - quota-display (show API quota on startup)
  - project-context (detect project type, show info)
  - git-status-check (warn if uncommitted changes)
- **PostToolUse Hooks:**
  - test-runner (auto-run tests after edits)
  - backup-creator (save versions before changes)
  - changelog-updater (track file modifications)
- **UserPromptSubmit Hooks:**
  - ✅ **@smart prompt optimizer v1.0** (AUTO-ENHANCE MODE - ACTIVE!)
    - Detects `@smart` or `[refine]` in prompts
    - **Automatically** adds project context (type, git, recent files)
    - **Non-interactive** - instant enhancement, zero friction
    - Works with existing `/workflow:*` commands
    - Location: `~/.claude/hooks/prompt-optimizer.sh`
    - Status: Production-ready ✅
  - 🔮 **@smart v2.0** (Future: INTERACTIVE MODE)
    - Build `/smart` slash command with menu
    - Options: Submit/Revise/Delegate/Cancel
    - Works alongside auto-enhance hook
    - See "Command Templates" section below
  - context-injector (add project-specific context)
  - style-enforcer (ensure consistency)
- **PermissionRequest Hooks:**
  - auto-approve-reads (safe operations)
  - block-destructive (prevent rm, dangerous ops)

#### 2. Command Templates (Enhanced with Frontmatter)
- [ ] `aiterm claude commands list` - Show all custom commands
- [ ] `aiterm claude commands create --template <type>` - From library
- [ ] `aiterm claude commands validate` - Check frontmatter syntax
- [ ] `aiterm claude commands migrate` - Convert old commands to new format
- [ ] `aiterm claude commands namespace <category>` - Create namespaced commands

**Template types with full frontmatter:**
- **Smart Prompting** (`/smart`) - 🔮 PLANNED (v2.0)
  - `/smart [prompt]` - Interactive menu for prompt optimization
    - Gathers project context (like @smart hook)
    - Shows interactive menu: Submit/Revise/Delegate/Cancel
    - Allows editing in $EDITOR before submission
    - Background agent delegation via Task tool
    - Complements auto-enhance @smart hook
  - Implementation: Interactive slash command (not hook)
  - Priority: Week 2-3 after core CLI is stable
- **Research** (`/research:*`):
  - `/research:literature` (with Zotero MCP integration)
  - `/research:cite` (format citations)
  - `/research:methods` (statistical methods templates)
  - `/research:tables` (LaTeX table generation)
- **Workflow** (`/workflow:*`):
  - `/workflow:recap` (your existing command)
  - `/workflow:next` (your existing command)
  - `/workflow:focus` (your existing command)
  - `/workflow:brainstorm` (your existing command)
- **Teaching** (`/teaching:*`):
  - `/teaching:grade` (with rubric)
  - `/teaching:feedback` (constructive comments)
  - `/teaching:rubric` (create grading rubrics)
- **Dev** (`/dev:*`):
  - `/dev:review` (code review standards)
  - `/dev:test` (run test suite)
  - `/dev:deploy` (deployment checklist)
- **R Package** (`/rpkg:*`):
  - `/rpkg:check` (devtools::check())
  - `/rpkg:document` (devtools::document())
  - `/rpkg:test` (devtools::test())
  - `/rpkg:build` (full build pipeline)

#### 3. MCP Server Management (Comprehensive)

**PRIORITY: MCP Creation Wizard** ✨
- [ ] `aiterm mcp create` - Interactive MCP server creation wizard
  - Template selection (simple-api, research-tools, r-package-dev, etc.)
  - Step-by-step configuration
  - Automatic file structure generation
  - Test server creation
- [ ] `aiterm mcp templates list` - Show available MCP templates
- [ ] `aiterm mcp validate <server>` - Validate MCP server structure
- [ ] Template library with 10+ starter templates

**MCP Management:**
- [ ] `aiterm mcp list` - Show configured servers with status
- [ ] `aiterm mcp search <keyword>` - Search mcp.run, glama.ai
- [ ] `aiterm mcp install <server>` - Install + configure interactively
- [ ] `aiterm mcp test <server>` - Test connection and tools
- [ ] `aiterm mcp config <server>` - Edit configuration
- [ ] `aiterm mcp credentials <server>` - Secure credential management
- [ ] `aiterm mcp recommend` - Suggest servers based on project type
- [ ] `aiterm mcp oauth <server>` - OAuth 2.0 authentication setup
- [ ] `aiterm mcp export/import` - Team configuration sharing

**MCP Server Categories:**
- **Research & Data:**
  - **r-development** (your comprehensive R toolkit - 20 tools!) ✨
  - postgres-mcp, sqlite-mcp (database access)
  - jupyter-mcp (notebook interaction)
  - teaching-toolkit (statistical courses, Canvas integration)
- **Development:**
  - filesystem (you already use this!)
  - github (issues, PRs)
  - gitlab
  - docker-mcp
- **Productivity:**
  - slack-mcp
  - google-drive-mcp
  - notion-mcp
  - calendar-mcp

**Special Feature - Context-Aware Installation:**
```bash
cd ~/projects/r-packages/medfit
aiterm mcp recommend

# Suggests:
# - r-execution (run R code)
# - github (for package releases)
# - filesystem (local file access)
```

#### 4. Skills Management (NEW - Oct 2025 Feature!)
- [ ] `aiterm skills list` - Show installed skills
- [ ] `aiterm skills create <name>` - Interactive skill creator
- [ ] `aiterm skills install <name>` - Install from template library
- [ ] `aiterm skills validate <name>` - Check SKILL.md format
- [ ] `aiterm skills test <name>` - Test skill invocation
- [ ] `aiterm skills share <name>` - Export for team
- [ ] `aiterm skills import <file>` - Install from export

**Skill Template Library:**
- **Research Skills:**
  - statistical-analysis-workflow (data → analysis → tables → plots)
  - literature-review (search → read → cite → summarize)
  - methods-writing (statistical methods documentation)
  - sensitivity-analysis (robustness checks)
- **R Package Skills:**
  - r-package-workflow (check → test → document → build)
  - cran-submission (pre-CRAN checklist)
  - pkgdown-site (build documentation site)
  - vignette-creation (create package vignettes)
- **Teaching Skills:**
  - assignment-grading (consistent grading workflow)
  - feedback-generation (constructive comments)
  - rubric-creation (grading rubrics)
  - course-materials (lecture/homework templates)
- **Code Quality Skills:**
  - code-review-standards (your project-specific standards)
  - test-coverage (ensure adequate testing)
  - documentation (docstrings, comments)
  - refactoring (safe refactoring patterns)

**Skill Features:**
- Automatic invocation (Claude detects when to use)
- Supporting files (scripts, templates)
- Path-based rules (`.claude/rules/` for conditional activation)
- Allowed-tools restrictions
- Progressive disclosure (lazy loading)

---

## Phase 2.5: Advanced Claude Code Features (v0.2.5)

**Goal:** Leverage newly discovered capabilities

### Features

#### 1. Subagent Management
- [ ] `aiterm agents list` - Show configured subagents
- [ ] `aiterm agents create <name>` - Interactive subagent creator
- [ ] `aiterm agents test <name>` - Test subagent behavior
- [ ] `aiterm agents validate` - Check agent config

**Subagent Templates:**
- **research-agent** (tools: Read, WebFetch, focused on research)
- **coding-agent** (tools: all, focused on implementation)
- **review-agent** (tools: Read, Grep, Glob, focused on code review)
- **statistical-agent** (tools: Bash, Read, focused on R/stats)

#### 2. Memory System Management
- [ ] `aiterm memory hierarchy` - Show precedence order
- [ ] `aiterm memory validate` - Check CLAUDE.md files
- [ ] `aiterm memory create` - Interactive CLAUDE.md creator
- [ ] `aiterm memory rules add` - Add path-specific rules
- [ ] `aiterm memory migrate` - Convert old format to new

**Memory Templates:**
- Research project CLAUDE.md
- R package CLAUDE.md
- Teaching course CLAUDE.md
- Dev tools CLAUDE.md

#### 3. Output Styles
- [ ] `aiterm styles list` - Show available output styles
- [ ] `aiterm styles create <name>` - Create custom style
- [ ] `aiterm styles preview <name>` - Preview style changes
- [ ] `aiterm styles set <name>` - Set default style

**Custom Styles:**
- academic-writing (formal, citation-focused)
- teaching-materials (student-friendly)
- code-documentation (developer-focused)
- statistical-reports (results presentation)

#### 4. Plugin Management
- [ ] `aiterm plugins list` - Show installed plugins
- [ ] `aiterm plugins search <keyword>` - Search marketplaces
- [ ] `aiterm plugins install <name>` - Install plugin
- [ ] `aiterm plugins create` - Initialize new plugin
- [ ] `aiterm plugins package` - Package for distribution
- [ ] `aiterm plugins validate` - Check plugin.json

**Plugin Components:**
- Commands bundled together
- Agents pre-configured
- Skills included
- Hooks packaged
- MCP servers integrated

#### 5. GitHub Actions Integration
- [ ] `aiterm ci generate` - Generate GitHub Actions workflow
- [ ] `aiterm ci test` - Test workflow locally
- [ ] `aiterm ci validate` - Check workflow syntax

**Workflow Templates:**
- R package CI (check, test, coverage)
- Research paper CI (compile LaTeX, run analysis)
- Documentation CI (build site, deploy)

---

## Phase 2.6: Workflow Commands & Documentation Automation (v0.2.6)

**Goal:** ADHD-friendly session management + automated documentation updates
**Timeline:** 2-3 weeks
**Status:** ✅ `/workflow:done` command created (2025-12-21)

### Background

**Problem Discovered:**
- `/workflow:done` was referenced 14+ times in ADHD guide but **file didn't exist**!
- Documentation rot happens at session boundaries (README updated, CLAUDE.md forgotten)
- Website docs (mkdocs.yml, docs/*.md) diverge from README
- CLAUDE.md staleness causes AI assistants to hallucinate

**Solution:**
- Created `/workflow:done` command (474 lines, comprehensive)
- Planned enhancements for automatic documentation detection/updates
- Three-phase rollout: Detection → Auto-updates → AI generation

### Features

#### 1. `/workflow:done` - Session Completion Command ✅ CREATED

**Core Functionality (Implemented):**
- [ ] Captures session progress from git changes
- [ ] Updates .STATUS file with accomplishments
- [ ] Generates commit message from changes
- [ ] Preserves context for next session
- [ ] Interactive summary with 4 options (A/B/C/D)
- [ ] Works even if user "forgot what they did"

**Location:** `~/.claude/commands/workflow/done.md`

**ADHD-Optimized:**
- 30-second fast path (press Enter to accept)
- Auto-detects accomplishments from git
- Prevents context loss at session boundaries
- Forgiveness mode for forgotten work

**Integration:**
- Complements `/workflow:recap` (start session)
- Works with `/workflow:next` (decide next task)
- Integrates with shell `finish` command

#### 2. Documentation Detection (Phase 1 - Planned)

**Auto-detect documentation needs:**

**Tier 1: Always Check**
- [ ] CHANGELOG.md - Generate entry from git diff
- [ ] NEWS.md - User-facing changes
- [ ] .STATUS file - Progress tracking (already in done.md)

**Tier 2: Conditional Checks**
- [ ] README.md - If new features/commands added
- [ ] CLAUDE.md - If architecture/patterns changed
- [ ] Planning docs - ROADMAP.md, IDEAS.md, TODO.md
- [ ] Website docs (docs/*.md) - If user-facing changes
- [ ] mkdocs.yml - If new pages created (orphan detection)

**Tier 3: Smart Detection**
- [ ] API docs - If public interfaces changed
- [ ] Test coverage - If added code but no tests
- [ ] Migration guides - If breaking changes detected

**Detection Methods:**
```bash
# CLAUDE.md staleness
CLAUDE_AGE=$(git log -1 --format=%at CLAUDE.md)
if [ $DAYS_OLD -gt 14 ]; then warn; fi

# Orphaned website pages
find docs -name "*.md" | while read doc; do
  grep -q "$doc" mkdocs.yml || echo "Orphaned: $doc"
done

# README vs docs/ divergence
diff <(extract_section README.md Installation) \
     <(extract_section docs/installation.md Installation)
```

#### 3. Documentation Auto-Updates (Phase 2 - Planned)

**Auto-fixable Documentation:**

**CHANGELOG.md:**
```markdown
## [Unreleased]

### Added
- [Inferred from new files/functions]

### Changed
- [Modified files with descriptions]

### Fixed
- [If commit messages contain "fix"]
```

**CLAUDE.md Section Updates:**
- New directories → Update "Project Structure"
- New CLI commands → Update "Commands" section
- New dependencies → Update "Tech Stack"
- Architecture changes → Update "Architecture"

**mkdocs.yml Navigation:**
```yaml
# Auto-add new pages to nav
nav:
  - Guide:
+   - Authentication: guide/authentication.md  # Auto-detected
```

**README ↔ docs/ Sync:**
- Detect divergence in key sections
- Offer to sync (bidirectional)
- Shared includes for single source of truth

#### 4. AI-Powered Documentation (Phase 3 - Future)

- [ ] GPT-4 generates doc updates from code
- [ ] Analyzes semantic changes (not just diffs)
- [ ] Writes tutorial content automatically
- [ ] Multi-file coordination

### Implementation Plan

**Phase 1: Detection & Warnings (Week 1)** ⭐
- Add Step 2.5 to `/workflow:done` (meta-documentation check)
- CLAUDE.md staleness warning
- Orphaned page detector
- README ↔ docs/ divergence check
- **Effort:** 3-4 hours

**Phase 2: Auto-Updates (Week 2-3)**
- CHANGELOG auto-generation
- CLAUDE.md section updates
- mkdocs.yml nav additions
- Shared content system (docs/snippets/)
- **Effort:** 8-12 hours

**Phase 3: AI Enhancement (v0.3.0)**
- LLM-powered doc generation
- Semantic change analysis
- Full automation
- **Effort:** 2-3 weeks

### Integration with Workflow

**Updated Session Pattern:**
```bash
START:  /workflow:recap      # "Where was I?"
WORK:   [code happens]
END:    /workflow:done        # New comprehensive end:
        ├─ Detect changes
        ├─ Check ALL docs (code + meta + website)
        ├─ Auto-update what we can
        ├─ Prompt for review
        ├─ Update .STATUS
        └─ Generate commit (includes doc updates)
```

**Shell Integration:**
```bash
finish() {
  claude "/workflow:done"     # Checks code + all docs now
  git commit -m "$MESSAGE"    # Includes doc updates
  git push
}
```

### Success Criteria

**Phase 1 (Detection):**
- ✅ 0 orphaned website pages
- ✅ CLAUDE.md never >14 days stale
- ✅ 100% divergence detection

**Phase 2 (Auto-Updates):**
- ✅ 80% of CHANGELOG entries auto-generated
- ✅ 90% of mkdocs.yml nav updates automatic
- ✅ CLAUDE.md sections auto-updated

**Phase 3 (AI):**
- ✅ 95% of documentation auto-generated
- ✅ Zero manual doc maintenance

### Files

**Created:**
- `~/.claude/commands/workflow/done.md` (474 lines)

**Planning Documents:**
- Session brainstorm: `/workflow:done` documentation features
- CLAUDE.md & website sync strategies
- Three-phase implementation plan

**To Update:**
- This file (IDEAS.md) - Document the plan
- CHANGELOG.md - Note command creation
- aiterm CLAUDE.md - Document Homebrew + workflow:done

---

## Phase 2.7: Distribution & Installation (v0.2.7)

**Goal:** Professional distribution via Homebrew
**Timeline:** 1-2 weeks (setup + testing)
**Status:** ✅ Homebrew formula created & deployed (2025-12-21)

### Features

#### 1. Homebrew Formula (Primary macOS Distribution) ⭐
- [ ] `Formula/aiterm.rb` - Python formula with virtualenv
- [ ] Private tap testing (data-wise/homebrew-tap)
- [ ] Installation: `brew install data-wise/tap/aiterm`
- [ ] Auto-dependency management (Python 3.10+)
- [ ] Update workflow: `brew upgrade aiterm`

**Benefits:**
- One-line installation for Mac users
- Automatic Python dependency handling
- Familiar workflow (`brew install/upgrade`)
- Professional appearance for public release

**Technical Approach:**
- Use `Language::Python::Virtualenv` pattern
- Install from GitHub releases (tarball)
- Automated SHA256 computation
- Test block for validation

#### 2. Automated Release Workflow
- [ ] `.github/workflows/release.yml` - Automated releases
- [ ] GitHub Release → PyPI upload (automatic)
- [ ] GitHub Release → Homebrew formula update (PR to tap)
- [ ] Auto-generate release notes from commits
- [ ] Version bump automation (`bump2version`)

**Workflow:**
```bash
# Single command triggers everything
git tag v0.2.7
git push --tags

# GitHub Action handles:
# 1. Build Python package
# 2. Upload to PyPI
# 3. Update Homebrew formula
# 4. Generate release notes
```

#### 3. Updated Installation Documentation
- [ ] README.md - Add Homebrew as primary method (macOS)
- [ ] Keep pip/UV as cross-platform option
- [ ] Installation comparison table
- [ ] Platform-specific instructions

**Installation Options:**
| Platform | Primary Method | Alternative |
|----------|---------------|-------------|
| macOS | `brew install data-wise/tap/aiterm` | `pip install aiterm` |
| Linux | `pip install aiterm` | `uv pip install aiterm` |
| All | `pip install aiterm` | - |

#### 4. Multi-Version Support (Future)
- [ ] Versioned installs: `brew install aiterm@0.2`
- [ ] Pin to specific version
- [ ] Rollback support via Homebrew

**Timeline:**
- **Week 1:** Create formula, test in private tap
- **Week 2:** Automated release workflow, update docs
- **v0.3.0:** Public tap release
- **v0.5.0+:** Submit to homebrew-core (official Homebrew)

---

## Phase 3: Gemini & Multi-Tool (v0.3.0)

**Goal:** Support multiple AI tools + Public Homebrew Release

### Features

#### 1. Public Homebrew Distribution ⭐
- [ ] Make tap repository public
- [ ] Homebrew formula tested with 10+ users
- [ ] Installation becomes: `brew tap data-wise/tap && brew install aiterm`
- [ ] Announce on Twitter/HN
- [ ] Add Homebrew badge to README

#### 2. Gemini CLI Integration
- [ ] Gemini-specific profiles
- [ ] Gemini triggers
- [ ] `aiterm gemini init`
- [ ] `aiterm switch claude|gemini`

#### 2. Context-Aware Features
- [ ] `aiterm context detect` - Show current context
- [ ] `aiterm context history` - Where you've been today
- [ ] `aiterm context export` - Export for other tools
- [ ] Context-based recommendations
  - Suggest Claude for coding
  - Suggest Gemini for research

#### 3. Status Bar Builder
- [ ] Interactive status bar designer
- [ ] Component library (icon, name, branch, quota, time)
- [ ] `aiterm statusbar build`
- [ ] `aiterm statusbar preview`
- [ ] Theme variants (cool-blues, forest-greens, purple-charcoal)

---

## Phase 4: Advanced & Polish (v1.0.0)

**Goal:** Production-ready public release

### Features

#### 1. Multi-Terminal Support
- [ ] iTerm2 (full support)
- [ ] Warp (basic support)
- [ ] Alacritty (config file)
- [ ] Kitty (config file)
- [ ] Terminal capability detection
- [ ] Graceful degradation

#### 2. Workflow Templates
- [ ] Template system architecture
- [ ] `aiterm workflow install <name>`
- [ ] Built-in workflows:
  - research (R, Quarto, literature)
  - teaching (courses, grading)
  - dev-tools (current DT setup)
  - web-dev
  - data-science
- [ ] Export/import workflows
- [ ] Community template sharing

#### 3. Session Management
- [ ] `aiterm record session` - Track context switches
- [ ] `aiterm sessions list`
- [ ] `aiterm sessions show <id>`
- [ ] Session analytics
  - Time per project
  - Quota usage patterns
  - Context switch frequency

#### 4. Web UI (Optional)
- [ ] Streamlit-based config builder
- [ ] Visual profile editor
- [ ] Template browser
- [ ] Usage dashboard

---

## Phase 4.5: Official Homebrew Core (v0.5.0+)

**Goal:** Get aiterm into official Homebrew
**Timeline:** After 100+ GitHub stars, 30+ days history

### Requirements for homebrew-core

#### Prerequisites
- [ ] 75+ GitHub stars (show community interest)
- [ ] 30+ days since first release (stability)
- [ ] Active maintenance (regular commits)
- [ ] Comprehensive documentation
- [ ] No reported installation issues

#### Submission Process
- [ ] Review homebrew-core contribution guidelines
- [ ] Ensure formula follows all best practices
- [ ] Create PR to `homebrew/homebrew-core`
- [ ] Respond to review feedback
- [ ] Maintain formula in core repo

**Benefits:**
- Installation becomes just: `brew install aiterm` (no tap needed)
- Maximum discoverability
- Homebrew team validates quality
- Automatic updates for all users
- Featured in `brew search` results

**Success Metrics:**
- Merged into homebrew-core
- No installation issues reported
- Regular updates via automated PR

---

## Future Ideas (Post-v1.0)

### Cross-Platform Packaging
- [ ] Linuxbrew support (use existing formula)
- [ ] apt PPA for Ubuntu/Debian
- [ ] chocolatey for Windows
- [ ] Standalone binary distribution (PyInstaller/Nuitka)

**Benefits:**
- Windows/Linux users get native installers
- No Python dependency conflicts
- Professional multi-platform support

### AI Workflow Optimizer
- Analyze usage patterns
- Suggest optimal settings
- Auto-tune based on behavior
- Compare Claude vs Gemini performance

### Context-Aware Quota System
- Different quotas per project type
- Warn before expensive operations
- Integrate with existing `qu` command
- Budget tracking per context

### Cross-Tool Intelligence
- Task-based AI selection
  - Code → Claude
  - Research → Gemini
  - Brainstorming → Both
- Side-by-side comparison mode
- Response quality tracking

### Teaching Mode
- Student-safe profiles
- Limited quotas
- Session recording for grading
- Assignment-specific contexts

### Integration Ecosystem
- VSCode extension
- Raycast extension
- Alfred workflow
- Slack status sync
- Calendar integration

### Advanced Terminal Features
- Custom keyboard shortcuts
- Hotkey window management
- Multi-pane layouts
- Terminal multiplexer integration

---

## Technical Debt & Improvements

### Code Quality
- [ ] Comprehensive test coverage (>80%)
- [ ] Type hints throughout
- [ ] Documentation (docstrings)
- [ ] CI/CD pipeline
- [ ] Pre-commit hooks

### Performance
- [ ] Fast startup (<100ms)
- [ ] Lazy loading modules
- [ ] Cache terminal detection
- [ ] Optimize context detection

### User Experience
- [ ] Rich CLI output (colors, tables)
- [ ] Progress bars for long operations
- [ ] Better error messages
- [ ] Interactive prompts (questionary)
- [ ] Shell completion (zsh, bash)

### Distribution
- [ ] PyPI package
- [ ] Homebrew formula
- [ ] Docker image
- [ ] Documentation site (MkDocs)

---

## Community Features

### Sharing & Collaboration
- [ ] Template marketplace
- [ ] User configs repository
- [ ] GitHub discussions
- [ ] Example gallery

### Documentation
- [ ] Quickstart guide
- [ ] Video tutorials
- [ ] Recipe book (common patterns)
- [ ] API documentation
- [ ] Contributing guide

---

## Non-Goals (Explicitly Out of Scope)

- Full IDE replacement
- Windows primary support (nice-to-have only)
- Non-AI terminal optimization
- Shell customization (use oh-my-zsh/powerlevel10k)
- Git workflow management (use existing tools)

---

## Success Metrics

### MVP (v0.1)
- DT uses daily for 1 week
- Faster setup than manual config
- No regressions from current aiterm

### v1.0
- 10+ external users
- <5 GitHub issues
- Documentation complete
- Install time <5 minutes

### Long-term
- 100+ stars on GitHub
- Community templates
- Integration with other tools
- Featured in Claude Code docs
