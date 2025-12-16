"""Main CLI entry point for aiterm."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aiterm import __app_name__, __version__

# Initialize Typer app
app = typer.Typer(
    name=__app_name__,
    help="Terminal optimizer CLI for AI-assisted development.",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(
            Panel(
                f"[bold cyan]{__app_name__}[/] version [green]{__version__}[/]\n"
                f"Terminal optimizer for Claude Code & Gemini CLI",
                title="aiterm",
                border_style="cyan",
            )
        )
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    aiterm - Terminal optimizer CLI for AI-assisted development.

    Optimizes iTerm2 (and other terminals) for Claude Code and Gemini CLI.
    Manages profiles, hooks, commands, context detection, and auto-approvals.
    """
    pass


@app.command()
def init() -> None:
    """Interactive setup wizard for aiterm."""
    console.print("[bold cyan]aiterm init[/] - Setup wizard")
    console.print("[yellow]Coming soon![/] This will:")
    console.print("  - Detect your terminal type")
    console.print("  - Install base profiles")
    console.print("  - Configure context detection")
    console.print("  - Test installation")


@app.command()
def doctor() -> None:
    """Check aiterm installation and configuration."""
    console.print("[bold cyan]aiterm doctor[/] - Health check")
    console.print()

    # Terminal detection
    import os

    term_program = os.environ.get("TERM_PROGRAM", "unknown")
    shell = os.environ.get("SHELL", "unknown")

    console.print(f"[bold]Terminal:[/] {term_program}")
    console.print(f"[bold]Shell:[/] {shell}")
    console.print(f"[bold]Python:[/] {__import__('sys').version.split()[0]}")
    console.print(f"[bold]aiterm:[/] {__version__}")
    console.print()
    console.print("[green]Basic checks passed![/]")
    console.print("[yellow]Full diagnostics coming in v0.2.0[/]")


# ─── Context detection implementation ────────────────────────────────────────


def _context_detect_impl(path: Optional[Path], apply: bool) -> None:
    """Shared implementation for context detection commands."""
    from aiterm.context.detector import detect_context
    from aiterm.terminal import iterm2

    target = path or Path.cwd()
    context = detect_context(target)

    # Build info table
    table = Table(title="Context Detection", show_header=False, border_style="cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Directory", str(target))
    table.add_row("Type", f"{context.icon} {context.type.value}" if context.icon else context.type.value)
    table.add_row("Name", context.name)
    table.add_row("Profile", context.profile)

    if context.branch:
        dirty = " [red]*[/]" if context.is_dirty else ""
        table.add_row("Git Branch", f"{context.branch}{dirty}")

    console.print(table)

    # Apply to terminal if requested
    if apply:
        if iterm2.is_iterm2():
            iterm2.apply_context(context)
            console.print("\n[green]✓[/] Context applied to iTerm2")
        else:
            console.print("\n[yellow]⚠[/] Not running in iTerm2 - context not applied")


# ─── Top-level shortcuts ─────────────────────────────────────────────────────


@app.command()
def detect(
    path: Optional[Path] = typer.Argument(None, help="Directory to analyze."),
) -> None:
    """Detect project context (shortcut for 'context detect')."""
    _context_detect_impl(path, apply=False)


@app.command()
def switch(
    path: Optional[Path] = typer.Argument(None, help="Directory to analyze."),
) -> None:
    """Detect and apply context to terminal (shortcut for 'context apply')."""
    _context_detect_impl(path, apply=True)


# ─── Sub-command groups ──────────────────────────────────────────────────────


context_app = typer.Typer(help="Context detection commands.")
profile_app = typer.Typer(help="Profile management commands.")
claude_app = typer.Typer(help="Claude Code integration commands.")

app.add_typer(context_app, name="context")
app.add_typer(profile_app, name="profile")
app.add_typer(claude_app, name="claude")


@context_app.command("detect")
def context_detect(
    path: Optional[Path] = typer.Argument(
        None,
        help="Directory to analyze. Defaults to current directory.",
    ),
    apply: bool = typer.Option(
        False,
        "--apply",
        "-a",
        help="Apply detected context to terminal (switch profile, set title).",
    ),
) -> None:
    """Detect the project context for a directory."""
    _context_detect_impl(path, apply)


@context_app.command("show")
def context_show() -> None:
    """Show current context (alias for detect)."""
    context_detect(path=None, apply=False)


@context_app.command("apply")
def context_apply(
    path: Optional[Path] = typer.Argument(
        None,
        help="Directory to analyze. Defaults to current directory.",
    ),
) -> None:
    """Detect and apply context to terminal."""
    context_detect(path=path, apply=True)


@profile_app.command("list")
def profile_list() -> None:
    """List available profiles."""
    console.print("[bold cyan]Available Profiles:[/]")
    console.print("  - default (iTerm2 base)")
    console.print("  - ai-session (Claude Code / Gemini)")
    console.print("  - production (warning colors)")
    console.print()
    console.print("[yellow]Profile management coming in v0.2.0[/]")


@claude_app.command("settings")
def claude_settings() -> None:
    """Display current Claude Code settings."""
    from pathlib import Path

    settings_path = Path.home() / ".claude" / "settings.json"
    if settings_path.exists():
        console.print(f"[bold]Settings file:[/] {settings_path}")
        console.print("[yellow]Settings viewer coming in v0.2.0[/]")
    else:
        console.print("[red]No Claude Code settings found.[/]")
        console.print(f"Expected at: {settings_path}")


if __name__ == "__main__":
    app()
