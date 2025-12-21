# aiterm Architecture Documentation

**Version:** 0.2.0-dev
**Last Updated:** 2025-12-21

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flows](#data-flows)
4. [Sequence Diagrams](#sequence-diagrams)
5. [State Machines](#state-machines)
6. [Design Patterns](#design-patterns)
7. [File Structure](#file-structure)

---

## System Overview

### High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        CLI[CLI Layer<br/>Typer]
    end

    subgraph "Core Library"
        Terminal[Terminal Backend<br/>Abstraction]
        Context[Context Detection<br/>Engine]
        Settings[Settings Manager]
    end

    subgraph "Integrations"
        ITerm2[iTerm2<br/>Integration]
        Claude[Claude Code<br/>Integration]
        MCP[MCP Server<br/>Management]
    end

    CLI --> Terminal
    CLI --> Context
    CLI --> Settings

    Terminal --> ITerm2
    Settings --> Claude
    Settings --> MCP

    Context --> Terminal
    Context -.-> Claude
```

**Key Components:**
- **CLI Layer** - User-facing commands (Typer framework)
- **Terminal Backend** - Abstracted terminal operations
- **Context Detection** - Project type detection
- **Settings Manager** - Configuration management
- **Integrations** - iTerm2, Claude Code, MCP servers

---

### Technology Stack

```mermaid
graph LR
    subgraph "Runtime"
        Python[Python 3.10+]
    end

    subgraph "CLI Framework"
        Typer[Typer<br/>CLI framework]
        Rich[Rich<br/>Terminal output]
        Quest[Questionary<br/>Interactive prompts]
    end

    subgraph "Build & Distribution"
        UV[UV<br/>Package manager]
        Hatchling[Hatchling<br/>Build backend]
    end

    subgraph "Testing"
        Pytest[pytest<br/>Test framework]
        Coverage[pytest-cov<br/>Coverage]
    end

    Python --> Typer
    Python --> Rich
    Python --> Quest
    Python --> UV
    UV --> Hatchling
    Python --> Pytest
```

---

## Component Architecture

### 1. Terminal Backend Architecture

```mermaid
graph TB
    subgraph "Terminal Backend"
        Base[TerminalBackend<br/>Abstract Base Class]
        ITerm2[iTerm2Terminal<br/>Implementation]
        Wezterm[WeztermTerminal<br/>Future]
        Alacritty[AlacrittyTerminal<br/>Future]

        Base -.-> ITerm2
        Base -.-> Wezterm
        Base -.-> Alacritty
    end

    subgraph "Operations"
        Profile[switch_profile]
        Title[set_title]
        Status[set_status_var]
        Query[get_current_profile]
    end

    ITerm2 --> Profile
    ITerm2 --> Title
    ITerm2 --> Status
    ITerm2 --> Query

    subgraph "iTerm2 Integration"
        Escape[Escape Sequences]
        API[Python API<br/>Future]
    end

    ITerm2 --> Escape
    ITerm2 -.-> API
```

**Design Pattern:** Abstract Factory + Strategy

**Key Abstractions:**
- `TerminalBackend` - Base interface for all terminals
- `iTerm2Terminal` - iTerm2-specific implementation
- Future: Wezterm, Alacritty, Kitty support

---

### 2. Context Detection Architecture

```mermaid
graph TB
    subgraph "Context Detection Engine"
        Detector[ContextDetector<br/>Base Class]
        Registry[DetectorRegistry<br/>Singleton]
    end

    subgraph "Built-in Detectors"
        Prod[ProductionDetector<br/>Priority: 1]
        AI[AISessionDetector<br/>Priority: 2]
        R[RPackageDetector<br/>Priority: 3]
        Py[PythonDetector<br/>Priority: 4]
        Node[NodeDetector<br/>Priority: 5]
        Quarto[QuartoDetector<br/>Priority: 6]
        MCP[MCPDetector<br/>Priority: 7]
        Dev[DevToolsDetector<br/>Priority: 8]
        Default[DefaultDetector<br/>Priority: 9]
    end

    subgraph "Custom Detectors"
        Custom[User-Defined<br/>Detectors]
    end

    Registry --> Prod
    Registry --> AI
    Registry --> R
    Registry --> Py
    Registry --> Node
    Registry --> Quarto
    Registry --> MCP
    Registry --> Dev
    Registry --> Default
    Registry -.-> Custom

    Detector <.. Prod
    Detector <.. AI
    Detector <.. R
    Detector <.. Custom
```

**Design Pattern:** Chain of Responsibility + Priority Queue

**Detection Flow:**
1. User calls `detect_context(path)`
2. Registry iterates detectors by priority
3. First detector that returns non-null wins
4. Return `Context` object with profile, title, metadata

---

### 3. Settings Management Architecture

```mermaid
graph TB
    subgraph "Settings Manager"
        Manager[SettingsManager<br/>Singleton]
        Validator[ConfigValidator]
        Backup[BackupManager]
    end

    subgraph "Configuration Files"
        Aiterm[~/.aiterm/config.json]
        Claude[~/.claude/settings.json]
    end

    subgraph "Operations"
        Read[read_settings]
        Write[write_settings]
        Validate[validate_config]
        Apply[apply_preset]
    end

    Manager --> Read
    Manager --> Write
    Manager --> Validate
    Manager --> Apply

    Read --> Aiterm
    Read --> Claude
    Write --> Aiterm
    Write --> Claude
    Validate --> Validator
    Write --> Backup

    Backup -.-> Claude
```

**Design Pattern:** Singleton + Template Method

**Key Features:**
- Automatic backups before writes
- JSON validation
- Preset management (8 presets)
- Merge strategies (replace vs merge)

---

### 4. CLI Command Architecture

```mermaid
graph TB
    subgraph "CLI Entry Point"
        Main[aiterm<br/>Main Command]
    end

    subgraph "Command Groups"
        Core[Core Commands<br/>doctor, detect]
        Profile[Profile Commands<br/>list, switch]
        Claude[Claude Commands<br/>approvals, settings]
        MCP[MCP Commands<br/>list, test, validate]
    end

    subgraph "Command Implementation"
        Handler[Command Handler]
        Validator[Input Validator]
        Output[Output Formatter<br/>Rich]
    end

    Main --> Core
    Main --> Profile
    Main --> Claude
    Main -.-> MCP

    Core --> Handler
    Profile --> Handler
    Claude --> Handler

    Handler --> Validator
    Handler --> Output
```

**Design Pattern:** Command Pattern + Decorator

**Command Structure:**
```python
@app.command()
def doctor():
    """Check aiterm installation"""
    # 1. Validate environment
    # 2. Check dependencies
    # 3. Format output (Rich)
    # 4. Return exit code
```

---

## Data Flows

### 1. Context Detection Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Detector
    participant Terminal
    participant iTerm2

    User->>CLI: cd ~/projects/RMediation
    activate CLI

    CLI->>Detector: detect_context(pwd)
    activate Detector

    Detector->>Detector: Check DESCRIPTION file
    Detector->>Detector: Check R/ directory
    Detector->>Detector: Parse package name/version

    Detector-->>CLI: Context(type=r-package, profile=R-Dev)
    deactivate Detector

    CLI->>Terminal: switch_profile("R-Dev")
    activate Terminal
    Terminal->>iTerm2: ESC]1337;SetProfile=R-Dev
    iTerm2-->>Terminal: Profile switched
    deactivate Terminal

    CLI->>Terminal: set_title("RMediation v1.0.0")
    activate Terminal
    Terminal->>iTerm2: ESC]0;RMediation v1.0.0
    iTerm2-->>Terminal: Title set
    deactivate Terminal

    CLI->>Terminal: set_status_var("project_type", "R PKG")
    activate Terminal
    Terminal->>iTerm2: ESC]1337;SetUserVar=...
    iTerm2-->>Terminal: Variable set
    deactivate Terminal

    CLI-->>User: Context switched ✅
    deactivate CLI
```

**Performance:**
- Detection: < 50ms
- Profile switch: < 150ms
- Total: < 200ms

---

### 2. Auto-Approval Application Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Settings
    participant Backup
    participant Claude

    User->>CLI: aiterm claude approvals set r-package
    activate CLI

    CLI->>Settings: read_claude_settings()
    activate Settings
    Settings->>Claude: Read ~/.claude/settings.json
    Claude-->>Settings: Current settings
    Settings-->>CLI: settings dict
    deactivate Settings

    CLI->>Backup: create_backup(settings)
    activate Backup
    Backup->>Claude: Write ~/.claude/settings.json.backup.TIMESTAMP
    Backup-->>CLI: Backup created
    deactivate Backup

    CLI->>Settings: apply_approval_preset("r-package")
    activate Settings
    Settings->>Settings: Load r-package preset (35 tools)
    Settings->>Settings: Merge with current approvals
    Settings->>Settings: Validate JSON structure
    Settings-->>CLI: Updated settings
    deactivate Settings

    CLI->>Settings: write_claude_settings(updated)
    activate Settings
    Settings->>Claude: Write ~/.claude/settings.json
    Claude-->>Settings: Write complete
    Settings-->>CLI: Success
    deactivate Settings

    CLI-->>User: ✅ Applied r-package preset (35 tools)
    deactivate CLI
```

**Safety Features:**
- Automatic backup before write
- JSON validation
- Rollback on error
- Backup retention (last 5)

---

### 3. Profile Switching Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Terminal
    participant iTerm2
    participant Shell

    User->>CLI: aiterm profile switch R-Dev
    activate CLI

    CLI->>Terminal: get_terminal()
    activate Terminal
    Terminal->>Terminal: Detect terminal type
    Terminal-->>CLI: iTerm2Terminal instance
    deactivate Terminal

    CLI->>Terminal: switch_profile("R-Dev")
    activate Terminal

    Terminal->>Terminal: Validate profile exists
    Terminal->>iTerm2: Send escape sequence<br/>ESC]1337;SetProfile=R-Dev BEL
    iTerm2->>iTerm2: Switch profile
    iTerm2->>Shell: Update environment
    iTerm2-->>Terminal: Profile switched

    Terminal-->>CLI: Success
    deactivate Terminal

    CLI->>Terminal: set_title("R Development")
    activate Terminal
    Terminal->>iTerm2: ESC]0;R Development BEL
    iTerm2-->>Terminal: Title set
    deactivate Terminal

    CLI-->>User: ✅ Switched to R-Dev
    deactivate CLI
```

---

## Sequence Diagrams

### 4. Doctor Command Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Checks
    participant System

    User->>CLI: aiterm doctor
    activate CLI

    CLI->>Checks: check_python_version()
    activate Checks
    Checks->>System: python --version
    System-->>Checks: 3.11.5
    Checks-->>CLI: ✅ Python 3.11.5
    deactivate Checks

    CLI->>Checks: check_terminal()
    activate Checks
    Checks->>System: $TERM_PROGRAM
    System-->>Checks: iTerm.app
    Checks->>System: iTerm2 version
    System-->>Checks: Build 3.5.0
    Checks-->>CLI: ✅ iTerm2 (Build 3.5.0)
    deactivate Checks

    CLI->>Checks: check_claude_code()
    activate Checks
    Checks->>System: ~/.claude/ exists?
    System-->>Checks: Yes
    Checks->>System: claude --version
    System-->>Checks: 0.2.0
    Checks-->>CLI: ✅ Claude Code 0.2.0
    deactivate Checks

    CLI->>Checks: check_config()
    activate Checks
    Checks->>System: ~/.aiterm/config.json exists?
    System-->>Checks: Yes
    Checks->>System: Validate JSON
    System-->>Checks: Valid
    Checks-->>CLI: ✅ Settings OK
    deactivate Checks

    CLI-->>User: All checks passed! ✅
    deactivate CLI
```

---

### 5. Profile List Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Terminal
    participant Config

    User->>CLI: aiterm profile list
    activate CLI

    CLI->>Config: read_config()
    activate Config
    Config->>Config: Load ~/.aiterm/config.json
    Config-->>CLI: Config dict
    deactivate Config

    CLI->>Terminal: get_available_profiles()
    activate Terminal
    Terminal->>Config: profiles section
    Terminal->>Terminal: Parse profile definitions
    Terminal-->>CLI: List of profiles
    deactivate Terminal

    loop For each profile
        CLI->>CLI: Format profile info
        CLI->>CLI: Add theme, triggers, description
    end

    CLI-->>User: Display formatted profile list
    deactivate CLI
```

---

## State Machines

### 1. Context Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Unknown: Start
    Unknown --> Detected: Context found
    Unknown --> Unknown: No context
    Detected --> Switched: Apply profile
    Switched --> Active: Profile applied
    Active --> Detected: Directory change
    Active --> [*]: Exit terminal
```

**States:**
- **Unknown** - No context detected
- **Detected** - Context identified
- **Switched** - Profile switching in progress
- **Active** - Profile active and in use

---

### 2. Settings Management Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Unloaded
    Unloaded --> Loading: Read request
    Loading --> Loaded: Success
    Loading --> Error: Parse fail
    Loaded --> Modifying: Update request
    Modifying --> Validating: Changes made
    Validating --> BackingUp: Validation passed
    Validating --> Error: Validation failed
    BackingUp --> Writing: Backup created
    Writing --> Loaded: Write success
    Writing --> Error: Write fail
    Error --> Loaded: Rollback
    Loaded --> [*]: Session end
```

**States:**
- **Unloaded** - Settings not read
- **Loading** - Reading from disk
- **Loaded** - Settings in memory
- **Modifying** - Changes being made
- **Validating** - Checking validity
- **BackingUp** - Creating backup
- **Writing** - Writing to disk
- **Error** - Error state (with rollback)

---

### 3. Profile Switching State

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Detecting: cd command
    Detecting --> Matched: Context found
    Detecting --> Idle: No match
    Matched --> Switching: Profile selected
    Switching --> Applied: Escape sequence sent
    Switching --> Failed: Terminal error
    Applied --> Updating: Set title/vars
    Updating --> Idle: Complete
    Failed --> Idle: Fallback to default
```

---

## Design Patterns

### 1. Singleton Pattern

**Used For:** Settings Manager, Detector Registry

```python
class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._load_settings()
        self._initialized = True
```

**Why:** Single source of truth for settings

---

### 2. Factory Pattern

**Used For:** Terminal backend creation

```python
def get_terminal() -> TerminalBackend:
    """Factory function for terminal backends"""
    term_program = os.getenv("TERM_PROGRAM", "")

    if "iTerm" in term_program:
        return iTerm2Terminal()
    elif "WezTerm" in term_program:
        return WeztermTerminal()  # Future
    else:
        return DefaultTerminal()  # Fallback
```

**Why:** Abstract terminal selection

---

### 3. Strategy Pattern

**Used For:** Context detection

```python
class ContextDetector(ABC):
    @abstractmethod
    def detect(self, path: str) -> Context | None:
        """Detect context from path"""
        pass

class RPackageDetector(ContextDetector):
    def detect(self, path: str) -> Context | None:
        if self._has_file(path, "DESCRIPTION"):
            # R package logic
            return Context(...)
        return None
```

**Why:** Pluggable detection strategies

---

### 4. Chain of Responsibility

**Used For:** Detector priority chain

```python
class DetectorRegistry:
    def detect(self, path: str) -> Context | None:
        # Try detectors in priority order
        for detector in sorted(self.detectors, key=lambda d: d.priority):
            context = detector.detect(path)
            if context:
                return context  # First match wins
        return None  # No matches
```

**Why:** First-match-wins with priority

---

### 5. Template Method

**Used For:** Settings operations

```python
class SettingsManager:
    def apply_preset(self, preset_name: str):
        # Template method
        settings = self.read_settings()       # 1. Read
        self.backup_settings(settings)        # 2. Backup
        updated = self._merge_preset(settings, preset_name)  # 3. Merge
        self.validate_settings(updated)       # 4. Validate
        self.write_settings(updated)          # 5. Write

    def _merge_preset(self, settings, preset):
        # Subclass hook (override for custom merge)
        pass
```

**Why:** Consistent operation flow

---

## File Structure

### Project Layout

```
aiterm/
├── src/aiterm/              # Main package
│   ├── __init__.py
│   ├── cli/                 # CLI commands
│   │   ├── __init__.py
│   │   ├── main.py          # Entry point
│   │   ├── core.py          # doctor, detect
│   │   ├── profile.py       # profile commands
│   │   ├── claude.py        # Claude Code commands
│   │   └── mcp.py           # MCP commands (future)
│   ├── terminal/            # Terminal backends
│   │   ├── __init__.py
│   │   ├── base.py          # Abstract base
│   │   ├── iterm2.py        # iTerm2 implementation
│   │   ├── wezterm.py       # Wezterm (future)
│   │   └── detector.py      # Terminal detection
│   ├── context/             # Context detection
│   │   ├── __init__.py
│   │   ├── base.py          # Abstract detector
│   │   ├── registry.py      # Detector registry
│   │   ├── detectors/       # Built-in detectors
│   │   │   ├── production.py
│   │   │   ├── ai_session.py
│   │   │   ├── r_package.py
│   │   │   ├── python.py
│   │   │   ├── nodejs.py
│   │   │   ├── quarto.py
│   │   │   ├── mcp.py
│   │   │   └── dev_tools.py
│   │   └── types.py         # Context type definitions
│   ├── claude/              # Claude Code integration
│   │   ├── __init__.py
│   │   ├── settings.py      # Settings management
│   │   ├── presets.py       # Auto-approval presets
│   │   ├── hooks.py         # Hook management (future)
│   │   └── commands.py      # Command templates (future)
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   ├── config.py        # Config file handling
│   │   ├── shell.py         # Shell integration
│   │   └── exceptions.py    # Custom exceptions
│   └── version.py           # Version info
├── templates/               # User-facing templates
│   ├── profiles/            # iTerm2 profile JSON
│   │   ├── R-Dev.json
│   │   ├── Python-Dev.json
│   │   └── ...
│   ├── hooks/               # Hook templates (future)
│   └── commands/            # Command templates (future)
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                    # Documentation
│   ├── api/
│   ├── architecture/
│   ├── guides/
│   └── troubleshooting/
├── pyproject.toml           # Project config
└── README.md
```

---

### Module Dependencies

```mermaid
graph TB
    subgraph "Public API"
        CLI[cli/]
    end

    subgraph "Core Library"
        Terminal[terminal/]
        Context[context/]
        Settings[claude/]
        Utils[utils/]
    end

    CLI --> Terminal
    CLI --> Context
    CLI --> Settings

    Terminal --> Utils
    Context --> Utils
    Settings --> Utils

    Context -.-> Terminal
```

**Dependency Rules:**
- CLI depends on Core Library
- Core Library is self-contained
- Utils are leaf modules (no dependencies)
- Context may trigger Terminal operations
- No circular dependencies

---

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**
   - Load detectors on-demand
   - Cache detector results
   - Lazy import heavy modules

2. **Caching**
   - Cache context detection results
   - Cache settings reads (TTL: 5s)
   - Cache terminal type detection

3. **Async Operations** (Future)
   - Parallel detector execution
   - Async file I/O
   - Non-blocking profile switching

---

### Performance Targets

| Operation | Target | Current | Status |
|-----------|--------|---------|--------|
| Context detection | < 50ms | ~30ms | ✅ |
| Profile switching | < 150ms | ~100ms | ✅ |
| Settings read | < 10ms | ~5ms | ✅ |
| Settings write | < 50ms | ~40ms | ✅ |
| Doctor check | < 200ms | ~150ms | ✅ |

---

## Security Considerations

### File Permissions

- `~/.aiterm/config.json` - 600 (user read/write only)
- `~/.claude/settings.json` - 600 (user read/write only)
- Backups - 600 (user read/write only)

### Input Validation

- Profile names - Alphanumeric + dashes
- Paths - Absolute paths only, no symlink following
- Settings - JSON schema validation
- Presets - Whitelist of known presets

### Escape Sequence Safety

- No user input in escape sequences (XSS risk)
- Whitelist of allowed sequences
- Sanitize all title/variable values

---

## Extension Points

### Adding New Terminal Backend

```python
from aiterm.terminal.base import TerminalBackend

class MyTerminal(TerminalBackend):
    def switch_profile(self, name: str) -> bool:
        # Custom implementation
        pass

    def set_title(self, text: str) -> bool:
        # Custom implementation
        pass
```

### Adding Custom Detector

```python
from aiterm.context.base import ContextDetector
from aiterm.context import register_detector

class MyDetector(ContextDetector):
    priority = 10

    def detect(self, path: str) -> Context | None:
        # Custom logic
        pass

register_detector(MyDetector())
```

---

## Future Architecture

### Phase 2 Additions

```mermaid
graph TB
    subgraph "Phase 2"
        Hook[Hook Manager]
        MCP[MCP Creator]
        Plugin[Plugin System]
    end

    subgraph "Existing"
        CLI[CLI]
        Terminal[Terminal]
        Context[Context]
    end

    CLI -.-> Hook
    CLI -.-> MCP
    CLI -.-> Plugin

    Hook -.-> Terminal
    MCP -.-> Context
```

**Planned Features:**
- Hook management system
- MCP server creation wizard
- Plugin architecture
- Remote terminal support
- Web UI

---

## Next Steps

- See [API Documentation](../api/AITERM-API.md) for detailed API reference
- See [User Guide](../guides/AITERM-USER-GUIDE.md) for usage examples
- See [Integration Guide](../guides/AITERM-INTEGRATION.md) for custom integrations
- See [Troubleshooting Guide](../troubleshooting/AITERM-TROUBLESHOOTING.md) for common issues

---

**Last Updated:** 2025-12-21
**Maintained By:** aiterm Development Team
