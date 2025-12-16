"""Main CLI entry point for aiterm."""

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

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


# Sub-command groups (stubs for now)
profile_app = typer.Typer(help="Profile management commands.")
claude_app = typer.Typer(help="Claude Code integration commands.")

app.add_typer(profile_app, name="profile")
app.add_typer(claude_app, name="claude")


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
