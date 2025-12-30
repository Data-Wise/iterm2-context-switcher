# aiterm Demo GIFs

Terminal recordings for aiterm documentation using [VHS](https://github.com/charmbracelet/vhs).

## Requirements

```bash
brew install vhs
```

## Generate GIFs

```bash
# Generate all demos
cd docs/demos
for tape in *.tape; do
  vhs "$tape"
done

# Or generate specific demo
vhs feature-workflow.tape
```

## Available Demos

| Demo | Description | Duration |
|------|-------------|----------|
| `feature-workflow.tape` | Feature branch commands (status, start, cleanup) | ~30s |
| `context-detection.tape` | Context detection and profile switching | ~25s |
| `worktree-setup.tape` | Creating worktrees with craft + aiterm | ~20s |
| `craft-finish.tape` | AI-assisted feature completion workflow | ~30s |

## Customization

Edit tape files to adjust:

- `Set FontSize` - Text size (default: 18)
- `Set Width/Height` - GIF dimensions (800x500)
- `Set Theme` - Color scheme (Dracula)
- `Set TypingSpeed` - How fast text appears (40ms)
- `Sleep` - Pause duration between commands

## Embedding in Docs

```markdown
![Feature Workflow](./demos/feature-workflow.gif)
```

## Tape File Template

```tape
# Demo Title
# Brief description

Output demo-name.gif

Set Shell "zsh"
Set FontSize 18
Set Width 800
Set Height 500
Set Theme "Dracula"
Set Padding 15
Set TypingSpeed 40ms

# Command 1
Type "command here"
Enter
Sleep 2s

# Command 2
Type "another command"
Enter
Sleep 2s
```

## CI/CD Generation (Optional)

Add to GitHub Actions:

```yaml
- name: Generate demo GIFs
  run: |
    brew install vhs
    cd docs/demos
    for tape in *.tape; do
      vhs "$tape"
    done
```

## Tips

- Keep demos under 30 seconds
- Use `Sleep` to let viewers read output
- Add comments in tape files for context
- Test with `vhs --preview` before generating
