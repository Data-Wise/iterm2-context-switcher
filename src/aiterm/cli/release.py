"""Release management commands for aiterm."""

import subprocess
import sys
from pathlib import Path

import typer
from rich import print
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="release",
    help="Release management commands for PyPI and Homebrew.",
    no_args_is_help=True,
)


def get_project_root() -> Path:
    """Find the project root by looking for pyproject.toml."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return cwd


def get_version_from_pyproject(root: Path) -> str | None:
    """Extract version from pyproject.toml."""
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None

    content = pyproject.read_text()
    for line in content.splitlines():
        if line.strip().startswith("version"):
            # Parse: version = "0.4.0"
            parts = line.split("=", 1)
            if len(parts) == 2:
                return parts[1].strip().strip('"').strip("'")
    return None


def get_version_from_init(root: Path) -> str | None:
    """Extract version from __init__.py."""
    # Try common locations
    locations = [
        root / "src" / "aiterm" / "__init__.py",
        root / "aiterm" / "__init__.py",
    ]

    for init_file in locations:
        if init_file.exists():
            content = init_file.read_text()
            for line in content.splitlines():
                if line.strip().startswith("__version__"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        return parts[1].strip().strip('"').strip("'")
    return None


def get_changelog_version(root: Path) -> str | None:
    """Extract latest version from CHANGELOG.md."""
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        return None

    content = changelog.read_text()
    # Look for pattern like ## [0.4.0] or ## [0.4.0] - 2025-12-30
    import re
    match = re.search(r"##\s*\[(\d+\.\d+\.\d+)\]", content)
    if match:
        return match.group(1)
    return None


def run_command(cmd: list[str], capture: bool = True) -> tuple[int, str]:
    """Run a command and return exit code and output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300,
        )
        output = result.stdout + result.stderr if capture else ""
        return result.returncode, output.strip()
    except subprocess.TimeoutExpired:
        return 1, "Command timed out"
    except FileNotFoundError:
        return 1, f"Command not found: {cmd[0]}"


def check_git_status(root: Path) -> tuple[bool, str]:
    """Check for uncommitted changes."""
    code, output = run_command(["git", "status", "--porcelain"], capture=True)
    if code != 0:
        return False, "Failed to check git status"
    if output:
        return False, f"Uncommitted changes:\n{output}"
    return True, "No uncommitted changes"


def check_git_branch() -> tuple[bool, str, str]:
    """Check current git branch."""
    code, branch = run_command(["git", "branch", "--show-current"])
    if code != 0:
        return False, "Failed to get branch", ""
    return True, branch, branch


def check_tag_exists(version: str) -> bool:
    """Check if a git tag exists."""
    code, _ = run_command(["git", "tag", "-l", f"v{version}"])
    # Check if the tag is in the list
    code, output = run_command(["git", "tag", "-l", f"v{version}"])
    return f"v{version}" in output.splitlines()


def run_tests(root: Path) -> tuple[bool, str]:
    """Run pytest and return success status."""
    code, output = run_command(["pytest", "--tb=no", "-q"], capture=True)
    if code == 0:
        # Extract pass count from output
        lines = output.strip().splitlines()
        for line in reversed(lines):
            if "passed" in line:
                return True, line
        return True, "Tests passed"
    return False, output


@app.command("check")
def release_check(
    skip_tests: bool = typer.Option(False, "--skip-tests", "-s", help="Skip running tests"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """
    Validate release readiness.

    Checks version consistency, tests, git status, and more.

    Examples:
        ait release check
        ait release check --skip-tests
        ait release check --verbose
    """
    root = get_project_root()

    print(Panel.fit("[bold]Release Check[/bold]", style="blue"))
    print()

    checks: list[tuple[str, bool, str]] = []
    all_passed = True

    # 1. Version consistency
    pyproject_ver = get_version_from_pyproject(root)
    init_ver = get_version_from_init(root)
    changelog_ver = get_changelog_version(root)

    versions_match = (
        pyproject_ver is not None
        and pyproject_ver == init_ver
        and pyproject_ver == changelog_ver
    )

    if versions_match:
        checks.append(("Version consistency", True, f"{pyproject_ver}"))
        if verbose:
            print(f"  pyproject.toml: {pyproject_ver}")
            print(f"  __init__.py: {init_ver}")
            print(f"  CHANGELOG.md: {changelog_ver}")
    else:
        all_passed = False
        details = []
        if pyproject_ver:
            details.append(f"pyproject.toml: {pyproject_ver}")
        if init_ver:
            details.append(f"__init__.py: {init_ver}")
        if changelog_ver:
            details.append(f"CHANGELOG.md: {changelog_ver}")
        checks.append(("Version consistency", False, ", ".join(details) if details else "Missing version"))

    version = pyproject_ver or init_ver or changelog_ver or "unknown"

    # 2. Tests
    if not skip_tests:
        print("[dim]Running tests...[/dim]", end="\r")
        test_passed, test_msg = run_tests(root)
        checks.append(("Tests", test_passed, test_msg))
        if not test_passed:
            all_passed = False
    else:
        checks.append(("Tests", True, "Skipped"))

    # 3. Git status (uncommitted changes)
    git_clean, git_msg = check_git_status(root)
    checks.append(("Clean working tree", git_clean, git_msg if not git_clean else "No uncommitted changes"))
    if not git_clean:
        all_passed = False

    # 4. Git branch
    branch_ok, branch_name, _ = check_git_branch()
    is_main = branch_name in ("main", "master")
    checks.append(("On main branch", is_main, f"Current: {branch_name}"))
    if not is_main:
        all_passed = False

    # 5. Tag exists check
    tag_exists = check_tag_exists(version)
    if tag_exists:
        checks.append(("Tag available", False, f"v{version} already exists"))
        all_passed = False
    else:
        checks.append(("Tag available", True, f"v{version} not yet tagged"))

    # Display results
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Status", width=3)
    table.add_column("Check", width=25)
    table.add_column("Details")

    for check_name, passed, details in checks:
        status = "[green]✓[/green]" if passed else "[red]✗[/red]"
        detail_style = "" if passed else "[dim]"
        table.add_row(status, check_name, f"{detail_style}{details}")

    print(table)
    print()

    if all_passed:
        print(f"[bold green]Ready to release v{version}[/bold green]")
        print()
        print("[dim]Next steps:[/dim]")
        print(f"  ait release tag {version}")
        print(f"  ait release pypi")
    else:
        print("[bold yellow]Not ready for release[/bold yellow]")
        print("[dim]Fix the issues above and run again.[/dim]")
        raise typer.Exit(1)


@app.command("status")
def release_status() -> None:
    """
    Show current release state and pending changes.

    Examples:
        ait release status
    """
    root = get_project_root()

    print(Panel.fit("[bold]Release Status[/bold]", style="blue"))
    print()

    # Current version
    version = get_version_from_pyproject(root) or "unknown"
    print(f"[bold]Current version:[/bold] {version}")

    # Latest tag
    code, tags = run_command(["git", "tag", "--sort=-v:refname"])
    if code == 0 and tags:
        latest_tag = tags.splitlines()[0]
        print(f"[bold]Latest tag:[/bold] {latest_tag}")

        # Commits since tag
        code, commits = run_command(["git", "rev-list", f"{latest_tag}..HEAD", "--count"])
        if code == 0:
            count = int(commits) if commits.isdigit() else 0
            print(f"[bold]Commits since tag:[/bold] {count}")

            if count > 0:
                print()
                print("[bold]Pending changes:[/bold]")
                code, log = run_command([
                    "git", "log", f"{latest_tag}..HEAD",
                    "--oneline", "--no-decorate"
                ])
                if code == 0:
                    for line in log.splitlines()[:10]:
                        print(f"  [dim]•[/dim] {line}")
                    if count > 10:
                        print(f"  [dim]... and {count - 10} more[/dim]")
    else:
        print("[dim]No tags found[/dim]")

    # Suggest next version
    print()
    if version != "unknown":
        parts = version.split(".")
        if len(parts) == 3:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            print("[bold]Suggested next versions:[/bold]")
            print(f"  Patch: {major}.{minor}.{patch + 1}")
            print(f"  Minor: {major}.{minor + 1}.0")
            print(f"  Major: {major + 1}.0.0")


@app.command("tag")
def release_tag(
    version: str = typer.Argument(None, help="Version to tag (e.g., 0.5.0)"),
    message: str = typer.Option(None, "--message", "-m", help="Tag message"),
    push: bool = typer.Option(False, "--push", "-p", help="Push tag to origin"),
) -> None:
    """
    Create an annotated git tag.

    Examples:
        ait release tag 0.5.0
        ait release tag 0.5.0 -m "Release v0.5.0"
        ait release tag 0.5.0 --push
    """
    root = get_project_root()

    # Use current version if not specified
    if version is None:
        version = get_version_from_pyproject(root)
        if not version:
            print("[red]Could not detect version. Please specify explicitly.[/red]")
            raise typer.Exit(1)

    tag_name = f"v{version}" if not version.startswith("v") else version

    # Check if tag exists
    if check_tag_exists(version.lstrip("v")):
        print(f"[red]Tag {tag_name} already exists[/red]")
        raise typer.Exit(1)

    # Create tag
    tag_message = message or f"Release {tag_name}"
    code, output = run_command(["git", "tag", "-a", tag_name, "-m", tag_message])

    if code != 0:
        print(f"[red]Failed to create tag: {output}[/red]")
        raise typer.Exit(1)

    print(f"[green]✓[/green] Created tag {tag_name}")

    if push:
        code, output = run_command(["git", "push", "origin", tag_name])
        if code != 0:
            print(f"[red]Failed to push tag: {output}[/red]")
            raise typer.Exit(1)
        print(f"[green]✓[/green] Pushed {tag_name} to origin")
    else:
        print(f"[dim]Push with: git push origin {tag_name}[/dim]")


if __name__ == "__main__":
    app()
