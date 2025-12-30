# Ghostty Quick Reference

Quick reference for aiterm's Ghostty terminal integration.

**Added in:** v0.3.9

---

## Current Commands (v0.3.9+)

```
┌─────────────────────────────────────────────────────────────┐
│ GHOSTTY COMMANDS                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ STATUS & CONFIG                                             │
│ ──────────────                                              │
│ ait ghostty status        Show config and detection status  │
│ ait ghostty config        Display config file location      │
│ ait ghostty config --edit Open config in $EDITOR            │
│                                                             │
│ THEME MANAGEMENT                                            │
│ ────────────────                                            │
│ ait ghostty theme list    List 14 built-in themes           │
│ ait ghostty theme show    Show current theme                │
│ ait ghostty theme apply   Apply a theme (auto-reload)       │
│                                                             │
│ FONT CONFIGURATION                                          │
│ ──────────────────                                          │
│ ait ghostty font show     Show current font settings        │
│ ait ghostty font set      Set font family and/or size       │
│                                                             │
│ GENERIC SETTINGS                                            │
│ ────────────────                                            │
│ ait ghostty set           Set any config key=value          │
│                                                             │
│ SHORTCUTS (via ghost alias)                                 │
│ ──────────────────────────                                  │
│ ait ghost                 → ait ghostty status              │
│ ait ghost theme           → ait ghostty theme list          │
│ ait ghost config          → ait ghostty config              │
│ ait ghost font            → ait ghostty font show           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Built-in Themes (14)

| Theme | Style |
|-------|-------|
| `catppuccin-mocha` | Dark, pastel |
| `catppuccin-latte` | Light, pastel |
| `catppuccin-frappe` | Medium dark |
| `catppuccin-macchiato` | Dark, muted |
| `dracula` | Dark, purple accent |
| `gruvbox-dark` | Dark, orange/green |
| `gruvbox-light` | Light, warm |
| `nord` | Dark, blue-gray |
| `solarized-dark` | Dark, teal accent |
| `solarized-light` | Light, teal accent |
| `tokyo-night` | Dark, purple/blue |
| `tokyo-night-storm` | Dark, stormy |
| `one-dark` | Atom One Dark |
| `one-light` | Atom One Light |

```bash
# Apply a theme
ait ghostty theme apply nord

# Ghostty auto-reloads on config change
```

---

## Common Configuration Keys

| Key | Values | Description |
|-----|--------|-------------|
| `theme` | Theme name | Color scheme |
| `font-family` | Font name | Monospace font |
| `font-size` | Integer | Font size in points |
| `window-padding-x` | Integer | Horizontal padding (px) |
| `window-padding-y` | Integer | Vertical padding (px) |
| `background-opacity` | 0.0-1.0 | Window transparency |
| `cursor-style` | block/bar/underline | Cursor shape |
| `cursor-style-blink` | true/false | Blink cursor |

```bash
# Examples
ait ghostty set background-opacity 0.95
ait ghostty set cursor-style bar
ait ghostty set window-padding-x 12
```

---

## Config File Location

```
~/.config/ghostty/config
```

```bash
# Open in editor
ait ghostty config --edit

# Example config
cat ~/.config/ghostty/config
```

**Sample config:**
```ini
font-family = JetBrains Mono
font-size = 14
theme = catppuccin-mocha
window-padding-x = 10
window-padding-y = 8
background-opacity = 1.0
cursor-style = block
```

---

## Detection

aiterm detects Ghostty via:

1. `GHOSTTY_RESOURCES_DIR` environment variable
2. `ghostty --version` command output

```bash
# Check detection
ait terminals detect

# Output when in Ghostty:
# ✓ Detected: ghostty
#   Version: Ghostty 1.2.3
```

---

## Planned Enhancements (v0.4.0)

The following commands are planned for Phase 0.8:

```
PROFILE MANAGEMENT (Planned)
────────────────────────────
ait ghostty profile list          List profiles
ait ghostty profile show <name>   Show profile details
ait ghostty profile apply <name>  Apply a profile
ait ghostty profile create <name> Create from current
ait ghostty profile delete <name> Delete a profile

KEYBIND MANAGEMENT (Planned)
────────────────────────────
ait ghostty keybind list              List keybindings
ait ghostty keybind add <key> <action> Add keybinding
ait ghostty keybind remove <key>      Remove keybinding
ait ghostty keybind preset <name>     Apply preset (vim/emacs)

SESSION CONTROL (Planned)
─────────────────────────
ait ghostty session save <name>       Save session layout
ait ghostty session restore <name>    Restore session
ait ghostty session list              List saved sessions
ait ghostty session split <dir>       Split pane (h/v)

CONFIG BACKUP (Planned)
───────────────────────
ait ghostty backup                    Timestamped backup
ait ghostty restore [backup]          Restore from backup
```

See: [Ghostty Enhancements Spec](../specs/SPEC-ghostty-enhancements-2025-12-30.md)

---

## flow-cli Integration

For instant Ghostty control via shell (no Python overhead):

```bash
# tm dispatcher commands
tm ghost status          # Same as: ait ghostty status
tm ghost theme dracula   # Same as: ait ghostty theme apply dracula
tm ghost font "Fira Code" 16  # Same as: ait ghostty font set
```

---

## Comparison with iTerm2

| Feature | Ghostty | iTerm2 |
|---------|---------|--------|
| Themes | ✓ Built-in (14) | ✓ Color presets |
| Profiles | ✗ Planned v0.4.0 | ✓ Full support |
| Tab Title | ✓ Via escape seqs | ✓ Via escape seqs |
| Badge | ✗ Not supported | ✓ Full support |
| Status Bar | ✗ Not supported | ✓ Full support |
| Native UI | ✓ macOS native | ✓ macOS native |
| Config Reload | ✓ Auto-reload | ✗ Manual |

---

## Related

- [Terminal Support Guide](../guide/terminals.md) - Full terminal documentation
- [Context Detection](../guide/context-detection.md) - Profile switching
- [REFCARD](../REFCARD.md) - Main quick reference
