# Status Bar Integration

Display context information in iTerm2's status bar.

## Available Variables (v2.4.0)

The context switcher sets these user variables on every directory change:

| Variable | Content | Example |
|----------|---------|---------|
| `\(user.ctxIcon)` | Context icon | `📦`, `🐍`, `🔧` |
| `\(user.ctxName)` | Project name | `medfit`, `myapp` |
| `\(user.ctxBranch)` | Git branch | `main`, `dev` |
| `\(user.ctxProfile)` | Active profile | `R-Dev`, `Python-Dev` |

---

## Quick Setup

### 1. Enable Status Bar

1. Open iTerm2 → Settings → Profiles
2. Select your profile (e.g., **Default**)
3. Go to **Session** tab
4. Check **Status bar enabled**
5. Click **Configure Status Bar**

### 2. Add Context Component

1. In the configuration panel, find **Interpolated String**
2. Drag it to your status bar
3. Click **Configure Component**
4. Set **String Value** to:

```
\(user.ctxIcon) \(user.ctxName) (\(user.ctxBranch))
```

This displays: `📦 medfit (main)`

---

## Example Configurations

### Minimal: Icon + Name

```
\(user.ctxIcon) \(user.ctxName)
```

Shows: `🔧 iterm2-context-switcher`

### Full: Icon + Name + Branch

```
\(user.ctxIcon) \(user.ctxName) (\(user.ctxBranch))
```

Shows: `📦 medfit (main)`

### Profile-Aware

```
[\(user.ctxProfile)] \(user.ctxIcon) \(user.ctxName)
```

Shows: `[R-Dev] 📦 medfit`

### Branch Only

```
\(user.ctxBranch)
```

Shows: `main` or `feature/new-api`

---

## Recommended Status Bar Layout

A balanced status bar setup:

```
┌────────────────────────────────────────────────────────┐
│ 📦 medfit (main)  │  ~/projects/...  │  CPU  │  12:30 │
└────────────────────────────────────────────────────────┘
     ↑                    ↑               ↑        ↑
  Context            Current Dir       System   Clock
```

**Components (left to right):**

1. **Interpolated String** - `\(user.ctxIcon) \(user.ctxName) (\(user.ctxBranch))`
2. **Spring** (spacer)
3. **Current Directory** (built-in)
4. **CPU Utilization** (built-in, optional)
5. **Clock** (built-in)

---

## Status Bar Styling

### Component Settings

For each component, you can set:

- **Background Color** - Override default
- **Text Color** - Override default
- **Priority** - Higher priority keeps component visible when space is tight (default: 5)
- **Minimum Width** - Prevent component from shrinking too small

### Recommended Settings for Context Component

- **Priority**: 10 (high - keep visible)
- **Minimum Width**: 100
- **Background Color**: Match your theme or leave default

---

## Per-Profile Status Bars

Each iTerm2 profile can have its own status bar configuration.

**Tip:** Configure the status bar on your **Default** profile, then child profiles (R-Dev, Python-Dev, etc.) will inherit it automatically.

---

## Built-in Git Component

iTerm2 also has a built-in **git state** component that shows:

- Branch name
- Dirty/clean status
- Ahead/behind remote

You can use this alongside or instead of `\(user.ctxBranch)`.

To add it:

1. Configure Status Bar
2. Drag **git state** to your bar
3. It auto-updates based on the current directory

---

## Troubleshooting

**Variables show empty or literal text:**

- Reload your shell: `source ~/.zshrc`
- Verify integration is loaded: `type _iterm_detect_context`
- Run `cd .` to trigger an update

**Status bar not visible:**

- Enable in Settings → Profiles → Session → Status bar enabled
- Check the profile you're using has status bar enabled

**Variables not updating:**

- Variables update on directory change (`cd`)
- Run `_iterm_detect_context` manually to force update

**Wrong variable values:**

- Check you're in the expected directory
- Verify git repo exists for branch info

---

## Technical Details

User variables are set via iTerm2's OSC 1337 escape sequence:

```bash
printf '\033]1337;SetUserVar=%s=%s\007' "name" "$(echo -n 'value' | base64)"
```

The context switcher calls this automatically on every `chpwd` hook (directory change).

Variables persist in the session until changed or the session ends.
