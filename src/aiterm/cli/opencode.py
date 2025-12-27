"""OpenCode CLI commands for aiterm.

Provides commands for managing OpenCode configuration, agents, and MCP servers.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aiterm.opencode import (
    OpenCodeConfig,
    Agent,
    MCPServer,
    load_config,
    save_config,
    validate_config,
    get_config_path,
    backup_config,
    RECOMMENDED_MODELS,
    DEFAULT_MCP_SERVERS,
)

app = typer.Typer(
    help="OpenCode CLI configuration and management.",
    rich_markup_mode="rich",
)

console = Console()

# ─── Config commands ──────────────────────────────────────────────────────────


@app.command(
    "config",
    epilog="""
[bold]Examples:[/]
  ait opencode config           # Show current config
  ait opencode config --raw     # Show raw JSON
""",
)
def config_show(
    raw: bool = typer.Option(False, "--raw", "-r", help="Show raw JSON output."),
) -> None:
    """Display current OpenCode configuration."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        console.print(f"Expected at: {get_config_path()}")
        return

    if raw:
        import json

        console.print(json.dumps(config.to_dict(), indent=2))
        return

    # Build config table
    table = Table(title="OpenCode Configuration", show_header=False, border_style="cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Config File", str(config.path))
    table.add_row("Model", config.model or "[dim]not set[/]")
    table.add_row("Small Model", config.small_model or "[dim]not set[/]")
    table.add_row("Default Agent", config.default_agent or "[dim]not set[/]")
    table.add_row("Scroll Accel", "[green]enabled[/]" if config.has_scroll_acceleration else "[dim]disabled[/]")
    table.add_row("MCP Servers", f"{len(config.enabled_servers)} enabled / {len(config.mcp_servers)} total")
    table.add_row("Custom Agents", str(len(config.agents)))
    table.add_row("Instructions", str(len(config.instructions)))

    console.print(table)

    # Show enabled servers
    if config.enabled_servers:
        console.print("\n[bold]Enabled MCP Servers:[/]")
        for name in config.enabled_servers:
            console.print(f"  [green]●[/] {name}")


@app.command(
    "validate",
    epilog="""
[bold]Examples:[/]
  ait opencode validate         # Validate config
""",
)
def config_validate() -> None:
    """Validate OpenCode configuration."""
    valid, messages = validate_config()

    if valid:
        console.print("[green]✓[/] Configuration is valid")
    else:
        console.print("[red]✗[/] Configuration has issues")

    if messages:
        console.print()
        for msg in messages:
            if msg.startswith("No ") or msg.startswith("Missing"):
                console.print(f"  [yellow]⚠[/] {msg}")
            else:
                console.print(f"  [red]✗[/] {msg}")


@app.command(
    "backup",
    epilog="""
[bold]Examples:[/]
  ait opencode backup           # Create timestamped backup
""",
)
def config_backup() -> None:
    """Create backup of OpenCode configuration."""
    config_path = get_config_path()
    if not config_path.exists():
        console.print("[red]No OpenCode configuration found to backup.[/]")
        return

    backup_path = backup_config()
    if backup_path:
        console.print(f"[green]✓[/] Backup created: {backup_path}")
    else:
        console.print("[red]Failed to create backup.[/]")


# ─── Agents sub-commands ──────────────────────────────────────────────────────

agents_app = typer.Typer(help="Manage OpenCode agents.")
app.add_typer(agents_app, name="agents")


@agents_app.command(
    "list",
    epilog="""
[bold]Examples:[/]
  ait opencode agents list      # List all agents
""",
)
def agents_list() -> None:
    """List configured agents."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    if not config.agents:
        console.print("[dim]No custom agents configured.[/]")
        console.print("\n[bold]Built-in modes:[/] build, plan, review, debug, docs")
        console.print("\nUse 'ait opencode agents add' to create a custom agent.")
        return

    table = Table(title="Custom Agents", border_style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Model")
    table.add_column("Tools")

    for name, agent in config.agents.items():
        # agent.tools is now a dict[str, bool], not a list
        enabled_tools = [t for t, v in agent.tools.items() if v] if agent.tools else []
        tools_str = ", ".join(enabled_tools[:3]) if enabled_tools else "[dim]default[/]"
        if len(enabled_tools) > 3:
            tools_str += f" (+{len(enabled_tools) - 3})"
        table.add_row(
            name,
            agent.description or "[dim]no description[/]",
            agent.model or "[dim]default[/]",
            tools_str,
        )

    console.print(table)


@agents_app.command(
    "add",
    epilog="""
[bold]Examples:[/]
  ait opencode agents add r-dev --desc "R development" --model anthropic/claude-sonnet-4-5
  ait opencode agents add quick --desc "Fast responses" --model anthropic/claude-haiku-4-5
""",
)
def agents_add(
    name: str = typer.Argument(..., help="Agent name (e.g., 'r-dev', 'quick')."),
    description: str = typer.Option("", "--desc", "-d", help="Agent description."),
    model: str = typer.Option("", "--model", "-m", help="Model to use (e.g., anthropic/claude-sonnet-4-5)."),
    tools: Optional[str] = typer.Option(None, "--tools", "-t", help="Comma-separated list of tools."),
) -> None:
    """Add a custom agent."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        console.print(f"Create {get_config_path()} first.")
        raise typer.Exit(1)

    # Validate model format
    if model and "/" not in model:
        console.print(f"[red]Invalid model format:[/] {model}")
        console.print("Model should be in format 'provider/model' (e.g., anthropic/claude-sonnet-4-5)")
        raise typer.Exit(1)

    # Parse tools (now a dict[str, bool])
    tools_dict = {t.strip(): True for t in tools.split(",")} if tools else {}

    # Create agent
    agent = Agent(
        name=name,
        description=description,
        model=model,
        tools=tools_dict,
    )

    # Backup first
    backup_config()

    # Add agent
    config.agents[name] = agent

    if save_config(config):
        console.print(f"[green]✓[/] Added agent '{name}'")
        if model:
            console.print(f"  Model: {model}")
        if tools_dict:
            console.print(f"  Tools: {', '.join(tools_dict.keys())}")
    else:
        console.print("[red]Failed to save configuration.[/]")
        raise typer.Exit(1)


@agents_app.command(
    "remove",
    epilog="""
[bold]Examples:[/]
  ait opencode agents remove r-dev   # Remove agent
""",
)
def agents_remove(
    name: str = typer.Argument(..., help="Agent name to remove."),
) -> None:
    """Remove a custom agent."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        raise typer.Exit(1)

    if name not in config.agents:
        console.print(f"[red]Agent '{name}' not found.[/]")
        if config.agents:
            console.print(f"Available agents: {', '.join(config.agents.keys())}")
        raise typer.Exit(1)

    # Backup first
    backup_config()

    # Remove agent
    del config.agents[name]

    if save_config(config):
        console.print(f"[green]✓[/] Removed agent '{name}'")
    else:
        console.print("[red]Failed to save configuration.[/]")
        raise typer.Exit(1)


# ─── Servers sub-commands ─────────────────────────────────────────────────────

servers_app = typer.Typer(help="Manage MCP servers.")
app.add_typer(servers_app, name="servers")


@servers_app.command(
    "list",
    epilog="""
[bold]Examples:[/]
  ait opencode servers list     # List all servers
""",
)
def servers_list() -> None:
    """List configured MCP servers."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    table = Table(title="MCP Servers", border_style="cyan")
    table.add_column("Server", style="bold")
    table.add_column("Status")
    table.add_column("Type")

    for name, server in config.mcp_servers.items():
        status = "[green]enabled[/]" if server.enabled else "[dim]disabled[/]"
        table.add_row(name, status, server.type)

    console.print(table)

    # Show available but not configured
    configured = set(config.mcp_servers.keys())
    available = set(DEFAULT_MCP_SERVERS.keys()) - configured
    if available:
        console.print(f"\n[dim]Available (not configured): {', '.join(sorted(available))}[/]")


@servers_app.command(
    "enable",
    epilog="""
[bold]Examples:[/]
  ait opencode servers enable github   # Enable GitHub server
""",
)
def servers_enable(
    name: str = typer.Argument(..., help="Server name to enable."),
) -> None:
    """Enable an MCP server."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        raise typer.Exit(1)

    if name not in config.mcp_servers:
        # Try to add from defaults
        if name in DEFAULT_MCP_SERVERS:
            default = DEFAULT_MCP_SERVERS[name]
            config.mcp_servers[name] = MCPServer(
                name=name,
                type=default.get("type", "local"),
                command=default.get("command", []),
                enabled=True,
            )
            backup_config()
            if save_config(config):
                console.print(f"[green]✓[/] Added and enabled '{name}'")
                return
        console.print(f"[red]Server '{name}' not found.[/]")
        raise typer.Exit(1)

    if config.mcp_servers[name].enabled:
        console.print(f"[yellow]Server '{name}' is already enabled.[/]")
        return

    backup_config()
    config.mcp_servers[name].enabled = True

    if save_config(config):
        console.print(f"[green]✓[/] Enabled '{name}'")
    else:
        console.print("[red]Failed to save configuration.[/]")
        raise typer.Exit(1)


@servers_app.command(
    "disable",
    epilog="""
[bold]Examples:[/]
  ait opencode servers disable playwright   # Disable Playwright
""",
)
def servers_disable(
    name: str = typer.Argument(..., help="Server name to disable."),
) -> None:
    """Disable an MCP server."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        raise typer.Exit(1)

    if name not in config.mcp_servers:
        console.print(f"[red]Server '{name}' not found.[/]")
        raise typer.Exit(1)

    if not config.mcp_servers[name].enabled:
        console.print(f"[yellow]Server '{name}' is already disabled.[/]")
        return

    backup_config()
    config.mcp_servers[name].enabled = False

    if save_config(config):
        console.print(f"[green]✓[/] Disabled '{name}'")
    else:
        console.print("[red]Failed to save configuration.[/]")
        raise typer.Exit(1)


# ─── Models sub-commands ──────────────────────────────────────────────────────


@app.command(
    "models",
    epilog="""
[bold]Examples:[/]
  ait opencode models           # List recommended models
""",
)
def models_list() -> None:
    """List recommended models for OpenCode."""
    console.print("[bold cyan]Recommended Models[/]\n")

    console.print("[bold]Primary (for main tasks):[/]")
    for model in RECOMMENDED_MODELS["primary"]:
        console.print(f"  • {model}")

    console.print("\n[bold]Small (for summaries/titles):[/]")
    for model in RECOMMENDED_MODELS["small"]:
        console.print(f"  • {model}")

    console.print("\n[dim]Use: ait opencode set-model <model>[/]")


@app.command(
    "set-model",
    epilog="""
[bold]Examples:[/]
  ait opencode set-model anthropic/claude-sonnet-4-5           # Set primary
  ait opencode set-model anthropic/claude-haiku-4-5 --small    # Set small model
""",
)
def set_model(
    model: str = typer.Argument(..., help="Model to set (e.g., anthropic/claude-sonnet-4-5)."),
    small: bool = typer.Option(False, "--small", "-s", help="Set as small model instead of primary."),
) -> None:
    """Set the model for OpenCode."""
    if "/" not in model:
        console.print(f"[red]Invalid model format:[/] {model}")
        console.print("Model should be in format 'provider/model'")
        raise typer.Exit(1)

    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        raise typer.Exit(1)

    backup_config()

    if small:
        config.small_model = model
        field = "small_model"
    else:
        config.model = model
        field = "model"

    if save_config(config):
        console.print(f"[green]✓[/] Set {field} to '{model}'")
    else:
        console.print("[red]Failed to save configuration.[/]")
        raise typer.Exit(1)


# ─── Instructions command ────────────────────────────────────────────────────


@app.command(
    "instructions",
    epilog="""
[bold]Examples:[/]
  ait opencode instructions           # List instruction files
""",
)
def instructions_list() -> None:
    """List configured instruction files (synced with Claude Code)."""
    from pathlib import Path

    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    console.print("[bold cyan]Instruction Files[/]\n")

    # Show configured instructions from config
    if config.instructions:
        console.print("[bold]From config (project-level):[/]")
        for instr in config.instructions:
            if isinstance(instr, dict):
                path = instr.get("path", str(instr))
            else:
                path = str(instr)
            console.print(f"  • {path}")
    else:
        console.print("[dim]No instructions configured in config.[/]")

    # Check for global AGENTS.md
    global_agents = Path.home() / ".config/opencode/AGENTS.md"
    console.print("\n[bold]Global instructions:[/]")
    if global_agents.exists():
        if global_agents.is_symlink():
            target = global_agents.resolve()
            console.print(f"  • AGENTS.md → {target}")
        else:
            console.print(f"  • AGENTS.md ({global_agents.stat().st_size} bytes)")
    else:
        console.print("  [dim]No global AGENTS.md[/]")

    # Show Claude Code equivalents
    console.print("\n[bold]Claude Code equivalents:[/]")
    claude_global = Path.home() / ".claude/CLAUDE.md"
    if claude_global.exists():
        console.print(f"  • ~/.claude/CLAUDE.md ({claude_global.stat().st_size} bytes)")
    console.print("  • CLAUDE.md (per-project)")
    console.print("  • .claude/rules/*.md (per-project)")

    console.print("\n[dim]Tip: OpenCode reads CLAUDE.md via 'instructions' config.[/]")


# ─── Keybinds command ────────────────────────────────────────────────────────
# NOTE: Keybinds are NOT supported by OpenCode schema (v1.0.203+).
# This command is kept for documentation purposes.


@app.command(
    "keybinds",
    epilog="""
[bold]Examples:[/]
  ait opencode keybinds           # Show keybinds status
""",
)
def keybinds_list() -> None:
    """List configured keyboard shortcuts (note: not currently supported by OpenCode)."""
    console.print("[bold cyan]Keyboard Shortcuts[/]\n")
    console.print("[yellow]Note:[/] Keybinds are not currently supported by OpenCode schema (v1.0.203+).")
    console.print("\nThis feature may be added in a future OpenCode version.")
    console.print("Check https://opencode.ai/docs for updates.")


# ─── Commands command ────────────────────────────────────────────────────────


@app.command(
    "commands",
    epilog="""
[bold]Examples:[/]
  ait opencode commands           # List custom commands
""",
)
def commands_list() -> None:
    """List configured custom commands."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    console.print("[bold cyan]Custom Commands[/]\n")

    if not config.commands:
        console.print("[dim]No custom commands configured.[/]")
        return

    table = Table(border_style="cyan")
    table.add_column("Command", style="bold")
    table.add_column("Description")
    table.add_column("Template")

    for name, cmd in config.commands.items():
        # Use cmd.template (new schema) instead of cmd.command
        table.add_row(name, cmd.description or "[dim]no description[/]", cmd.template or "[dim]none[/]")

    console.print(table)


# ─── Tools command ───────────────────────────────────────────────────────────


@app.command(
    "tools",
    epilog="""
[bold]Examples:[/]
  ait opencode tools              # List tool configuration
""",
)
def tools_list() -> None:
    """List configured tools."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    console.print("[bold cyan]Tool Configuration[/]\n")

    if not config.tools:
        console.print("[dim]No tool configuration found.[/]")
        console.print("\nAdd to config.json:")
        console.print('  "tools": { "bash": true, "read": true }')
        return

    table = Table(border_style="cyan")
    table.add_column("Tool", style="bold")
    table.add_column("Status")

    for name, enabled in config.tools.items():
        # Tools are now boolean (enabled/disabled)
        status = "[green]enabled[/]" if enabled else "[red]disabled[/]"
        table.add_row(name, status)

    console.print(table)
    console.print(f"\n[dim]Enabled: {len(config.enabled_tools)}, Disabled: {len(config.disabled_tools)}[/]")


# ─── Summary command ─────────────────────────────────────────────────────────


@app.command(
    "summary",
    epilog="""
[bold]Examples:[/]
  ait opencode summary            # Full configuration summary
""",
)
def config_summary() -> None:
    """Show complete configuration summary."""
    config = load_config()
    if not config:
        console.print("[red]No OpenCode configuration found.[/]")
        return

    console.print("[bold cyan]OpenCode Configuration Summary[/]\n")

    # Models
    console.print("[bold]Models:[/]")
    console.print(f"  Primary: {config.model or '[dim]not set[/]'}")
    console.print(f"  Small: {config.small_model or '[dim]not set[/]'}")

    # Agents
    console.print(f"\n[bold]Agents:[/] ({len(config.agents)} custom)")
    for name, agent in config.agents.items():
        model_short = agent.model.split("/")[-1] if agent.model else "default"
        # agent.tools is now a dict[str, bool]
        enabled_tools = [t for t, v in agent.tools.items() if v] if agent.tools else []
        console.print(f"  • {name}: {model_short} ({len(enabled_tools)} tools)")

    # Commands
    if config.commands:
        console.print(f"\n[bold]Commands:[/] ({len(config.commands)})")
        for name in config.commands:
            console.print(f"  • {name}")

    # Tool Configuration (now boolean enabled/disabled)
    if config.tools:
        console.print(f"\n[bold]Tools:[/]")
        console.print(f"  Enabled: {', '.join(config.enabled_tools) or '[dim]none[/]'}")
        if config.disabled_tools:
            console.print(f"  Disabled: {', '.join(config.disabled_tools)}")

    # MCP Servers
    console.print(f"\n[bold]MCP Servers:[/] ({len(config.enabled_servers)} enabled)")
    for name in config.enabled_servers:
        console.print(f"  [green]●[/] {name}")

    # Instructions
    if config.instructions:
        console.print(f"\n[bold]Instructions:[/] ({len(config.instructions)} files)")
        for instr in config.instructions:
            console.print(f"  • {instr}")
