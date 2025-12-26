"""Session management CLI.

Phase 4.3: Manage Claude Code and development sessions.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    help="Manage development sessions.",
    no_args_is_help=True,
)
console = Console()


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class Session:
    """Represents a development session."""

    id: str
    project: str
    started: datetime
    ended: datetime | None = None
    workflow: str = ""
    notes: str = ""
    commits: int = 0
    files_changed: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    cost_usd: float = 0.0
    tags: list[str] = field(default_factory=list)

    @property
    def duration(self) -> timedelta:
        """Get session duration."""
        end = self.ended or datetime.now()
        return end - self.started

    @property
    def duration_str(self) -> str:
        """Get human-readable duration."""
        duration = self.duration
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @property
    def is_active(self) -> bool:
        """Check if session is still active."""
        return self.ended is None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "project": self.project,
            "started": self.started.isoformat(),
            "ended": self.ended.isoformat() if self.ended else None,
            "workflow": self.workflow,
            "notes": self.notes,
            "commits": self.commits,
            "files_changed": self.files_changed,
            "lines_added": self.lines_added,
            "lines_removed": self.lines_removed,
            "cost_usd": self.cost_usd,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Session:
        """Create from dictionary."""
        return cls(
            id=data["id"],
            project=data["project"],
            started=datetime.fromisoformat(data["started"]),
            ended=datetime.fromisoformat(data["ended"]) if data.get("ended") else None,
            workflow=data.get("workflow", ""),
            notes=data.get("notes", ""),
            commits=data.get("commits", 0),
            files_changed=data.get("files_changed", 0),
            lines_added=data.get("lines_added", 0),
            lines_removed=data.get("lines_removed", 0),
            cost_usd=data.get("cost_usd", 0.0),
            tags=data.get("tags", []),
        )


def get_sessions_dir() -> Path:
    """Get sessions directory."""
    return Path.home() / ".claude" / "sessions"


def get_sessions_file() -> Path:
    """Get sessions history file."""
    return get_sessions_dir() / "history.json"


def generate_session_id() -> str:
    """Generate a unique session ID."""
    import random
    import string
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{timestamp}-{suffix}"


def load_sessions() -> list[Session]:
    """Load all sessions from history."""
    sessions_file = get_sessions_file()
    if not sessions_file.exists():
        return []

    try:
        data = json.loads(sessions_file.read_text())
        return [Session.from_dict(s) for s in data.get("sessions", [])]
    except (json.JSONDecodeError, OSError):
        return []


def save_sessions(sessions: list[Session]) -> bool:
    """Save sessions to history."""
    sessions_dir = get_sessions_dir()
    sessions_dir.mkdir(parents=True, exist_ok=True)

    sessions_file = get_sessions_file()
    try:
        data = {"sessions": [s.to_dict() for s in sessions]}
        sessions_file.write_text(json.dumps(data, indent=2))
        return True
    except OSError:
        return False


def get_active_session() -> Session | None:
    """Get the currently active session."""
    sessions = load_sessions()
    for session in sessions:
        if session.is_active:
            return session
    return None


def get_session_by_id(session_id: str) -> Session | None:
    """Get a specific session by ID."""
    sessions = load_sessions()
    for session in sessions:
        if session.id == session_id:
            return session
    return None


# =============================================================================
# CLI Commands
# =============================================================================


@app.command("start")
def session_start(
    project: str = typer.Argument(None, help="Project name (default: current directory)."),
    workflow: str = typer.Option(None, "--workflow", "-w", help="Workflow to apply."),
    notes: str = typer.Option("", "--notes", "-n", help="Session notes."),
    tags: str = typer.Option("", "--tags", "-t", help="Comma-separated tags."),
) -> None:
    """Start a new development session."""
    # Check for existing active session
    active = get_active_session()
    if active:
        console.print(f"[yellow]Session already active: {active.id}[/]")
        console.print(f"  Project: {active.project}")
        console.print(f"  Duration: {active.duration_str}")
        console.print("\nEnd it with 'ait sessions end' first.")
        return

    # Create new session
    project_name = project or Path.cwd().name
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    session = Session(
        id=generate_session_id(),
        project=project_name,
        started=datetime.now(),
        workflow=workflow or "",
        notes=notes,
        tags=tag_list,
    )

    # Save
    sessions = load_sessions()
    sessions.append(session)
    if save_sessions(sessions):
        console.print(f"[green]Started session:[/] {session.id}")
        console.print(f"  Project: {project_name}")
        if workflow:
            console.print(f"  Workflow: {workflow}")
        console.print(f"\n[dim]End with 'ait sessions end' when done.[/]")
    else:
        console.print("[red]Failed to start session.[/]")
        raise typer.Exit(1)


@app.command("end")
def session_end(
    notes: str = typer.Option(None, "--notes", "-n", help="Add/update notes."),
    commits: int = typer.Option(None, "--commits", "-c", help="Number of commits made."),
) -> None:
    """End the current session."""
    active = get_active_session()
    if not active:
        console.print("[yellow]No active session.[/]")
        return

    # Update session
    active.ended = datetime.now()
    if notes:
        active.notes = (active.notes + "\n" + notes).strip() if active.notes else notes

    # Try to get git stats
    if commits is None:
        import subprocess
        try:
            # Count commits during session
            since = active.started.strftime("%Y-%m-%d %H:%M:%S")
            result = subprocess.run(
                ["git", "log", "--oneline", f"--since={since}"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                active.commits = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
        except Exception:
            pass
    else:
        active.commits = commits

    # Save
    sessions = load_sessions()
    for i, s in enumerate(sessions):
        if s.id == active.id:
            sessions[i] = active
            break

    if save_sessions(sessions):
        console.print(f"[green]Ended session:[/] {active.id}")
        console.print(f"  Duration: {active.duration_str}")
        console.print(f"  Commits: {active.commits}")
    else:
        console.print("[red]Failed to end session.[/]")
        raise typer.Exit(1)


@app.command("status")
def session_status() -> None:
    """Show current session status."""
    active = get_active_session()

    console.print("[bold cyan]Session Status[/]\n")

    if active:
        console.print(f"[green]● Active session[/]")
        console.print(f"  ID: {active.id}")
        console.print(f"  Project: {active.project}")
        console.print(f"  Duration: {active.duration_str}")
        if active.workflow:
            console.print(f"  Workflow: {active.workflow}")
        if active.notes:
            console.print(f"  Notes: {active.notes[:50]}...")
        if active.tags:
            console.print(f"  Tags: {', '.join(active.tags)}")
    else:
        console.print("[dim]No active session.[/]")
        console.print("\nStart one with: ait sessions start")


@app.command("list")
def session_list(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of sessions to show."),
    project: str = typer.Option(None, "--project", "-p", help="Filter by project."),
    active_only: bool = typer.Option(False, "--active", "-a", help="Show only active sessions."),
) -> None:
    """List recent sessions."""
    sessions = load_sessions()

    # Filter
    if project:
        sessions = [s for s in sessions if s.project == project]
    if active_only:
        sessions = [s for s in sessions if s.is_active]

    # Sort by start time (most recent first)
    sessions = sorted(sessions, key=lambda s: s.started, reverse=True)[:limit]

    if not sessions:
        console.print("[yellow]No sessions found.[/]")
        return

    table = Table(title="Development Sessions", border_style="cyan")
    table.add_column("ID", style="bold")
    table.add_column("Project")
    table.add_column("Duration", justify="right")
    table.add_column("Commits", justify="right")
    table.add_column("Status")
    table.add_column("Date")

    for session in sessions:
        status = "[green]active[/]" if session.is_active else "[dim]ended[/]"
        date_str = session.started.strftime("%Y-%m-%d")

        table.add_row(
            session.id[:15],
            session.project[:15],
            session.duration_str,
            str(session.commits),
            status,
            date_str,
        )

    console.print(table)


@app.command("show")
def session_show(
    session_id: str = typer.Argument(..., help="Session ID to show."),
) -> None:
    """Show detailed session information."""
    session = get_session_by_id(session_id)
    if not session:
        # Try partial match
        sessions = load_sessions()
        matches = [s for s in sessions if s.id.startswith(session_id)]
        if len(matches) == 1:
            session = matches[0]
        elif len(matches) > 1:
            console.print(f"[yellow]Multiple sessions match '{session_id}':[/]")
            for s in matches:
                console.print(f"  {s.id}")
            return
        else:
            console.print(f"[red]Session '{session_id}' not found.[/]")
            return

    content = []
    content.append(f"[bold]Project:[/] {session.project}")
    content.append(f"[bold]Started:[/] {session.started.strftime('%Y-%m-%d %H:%M')}")
    if session.ended:
        content.append(f"[bold]Ended:[/] {session.ended.strftime('%Y-%m-%d %H:%M')}")
    content.append(f"[bold]Duration:[/] {session.duration_str}")
    content.append(f"[bold]Status:[/] {'Active' if session.is_active else 'Ended'}")

    if session.workflow:
        content.append(f"[bold]Workflow:[/] {session.workflow}")

    if session.commits or session.files_changed:
        content.append("")
        content.append("[bold]Stats:[/]")
        content.append(f"  Commits: {session.commits}")
        if session.files_changed:
            content.append(f"  Files changed: {session.files_changed}")
        if session.lines_added or session.lines_removed:
            content.append(f"  Lines: +{session.lines_added}/-{session.lines_removed}")
        if session.cost_usd > 0:
            content.append(f"  Cost: ${session.cost_usd:.2f}")

    if session.tags:
        content.append(f"\n[bold]Tags:[/] {', '.join(session.tags)}")

    if session.notes:
        content.append(f"\n[bold]Notes:[/]\n{session.notes}")

    console.print(Panel(
        "\n".join(content),
        title=f"Session: {session.id}",
        border_style="cyan",
    ))


@app.command("stats")
def session_stats(
    days: int = typer.Option(7, "--days", "-d", help="Days to include in stats."),
) -> None:
    """Show session statistics."""
    sessions = load_sessions()
    cutoff = datetime.now() - timedelta(days=days)

    # Filter to recent sessions
    recent = [s for s in sessions if s.started >= cutoff]
    completed = [s for s in recent if not s.is_active]

    console.print(f"[bold cyan]Session Statistics (Last {days} Days)[/]\n")

    # Summary
    total_duration = sum((s.duration for s in completed), timedelta())
    total_commits = sum(s.commits for s in completed)
    total_cost = sum(s.cost_usd for s in completed)

    hours = total_duration.total_seconds() / 3600

    table = Table(border_style="dim", show_header=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total sessions", str(len(recent)))
    table.add_row("Completed", str(len(completed)))
    table.add_row("Total time", f"{hours:.1f} hours")
    table.add_row("Total commits", str(total_commits))
    if total_cost > 0:
        table.add_row("Total cost", f"${total_cost:.2f}")

    if completed:
        avg_duration = total_duration / len(completed)
        avg_minutes = avg_duration.total_seconds() / 60
        table.add_row("Avg session", f"{avg_minutes:.0f} minutes")

    console.print(table)

    # Projects breakdown
    if recent:
        console.print("\n[bold]By Project:[/]")
        projects: dict[str, int] = {}
        for s in recent:
            projects[s.project] = projects.get(s.project, 0) + 1

        for project, count in sorted(projects.items(), key=lambda x: x[1], reverse=True)[:5]:
            console.print(f"  {project}: {count} sessions")


@app.command("delete")
def session_delete(
    session_id: str = typer.Argument(..., help="Session ID to delete."),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation."),
) -> None:
    """Delete a session from history."""
    sessions = load_sessions()
    session = None
    index = -1

    for i, s in enumerate(sessions):
        if s.id == session_id or s.id.startswith(session_id):
            session = s
            index = i
            break

    if not session:
        console.print(f"[red]Session '{session_id}' not found.[/]")
        return

    if session.is_active:
        console.print("[yellow]Cannot delete active session. End it first.[/]")
        return

    if not force:
        console.print(f"[yellow]Delete session {session.id}?[/]")
        console.print(f"  Project: {session.project}")
        console.print(f"  Duration: {session.duration_str}")
        console.print("\nUse --force to confirm deletion.")
        return

    sessions.pop(index)
    if save_sessions(sessions):
        console.print(f"[green]Deleted session {session.id}[/]")
    else:
        console.print("[red]Failed to delete session.[/]")


@app.command("export")
def session_export(
    output: Path = typer.Option(None, "--output", "-o", help="Output file."),
    format: str = typer.Option("json", "--format", "-f", help="Format: json or csv."),
) -> None:
    """Export session history."""
    sessions = load_sessions()

    if not sessions:
        console.print("[yellow]No sessions to export.[/]")
        return

    output_path = output or Path.cwd() / f"sessions-export.{format}"

    try:
        if format == "json":
            data = {"sessions": [s.to_dict() for s in sessions]}
            output_path.write_text(json.dumps(data, indent=2))
        elif format == "csv":
            import csv
            with open(output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "id", "project", "started", "ended", "duration_min",
                    "commits", "workflow", "tags"
                ])
                for s in sessions:
                    writer.writerow([
                        s.id,
                        s.project,
                        s.started.isoformat(),
                        s.ended.isoformat() if s.ended else "",
                        int(s.duration.total_seconds() / 60),
                        s.commits,
                        s.workflow,
                        ",".join(s.tags),
                    ])
        else:
            console.print(f"[red]Unknown format: {format}[/]")
            raise typer.Exit(1)

        console.print(f"[green]Exported {len(sessions)} sessions to:[/] {output_path}")
    except OSError as e:
        console.print(f"[red]Export failed: {e}[/]")
        raise typer.Exit(1)


@app.command("cleanup")
def session_cleanup(
    days: int = typer.Option(30, "--days", "-d", help="Delete sessions older than N days."),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show what would be deleted."),
) -> None:
    """Clean up old session history."""
    sessions = load_sessions()
    cutoff = datetime.now() - timedelta(days=days)

    old_sessions = [s for s in sessions if s.started < cutoff and not s.is_active]
    keep_sessions = [s for s in sessions if s.started >= cutoff or s.is_active]

    if not old_sessions:
        console.print(f"[green]No sessions older than {days} days.[/]")
        return

    console.print(f"Found {len(old_sessions)} sessions older than {days} days.")

    if dry_run:
        console.print("\n[yellow]Would delete:[/]")
        for s in old_sessions[:5]:
            console.print(f"  {s.id} - {s.project} ({s.started.strftime('%Y-%m-%d')})")
        if len(old_sessions) > 5:
            console.print(f"  ... and {len(old_sessions) - 5} more")
        return

    if save_sessions(keep_sessions):
        console.print(f"[green]Deleted {len(old_sessions)} old sessions.[/]")
        console.print(f"Remaining: {len(keep_sessions)} sessions")
    else:
        console.print("[red]Failed to save changes.[/]")
