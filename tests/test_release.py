"""Tests for release CLI commands."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from aiterm.cli.release import (
    app,
    check_git_branch,
    check_git_status,
    check_tag_exists,
    get_changelog_version,
    get_project_root,
    get_version_from_init,
    get_version_from_pyproject,
    run_command,
)

runner = CliRunner()


class TestVersionDetection:
    """Tests for version detection functions."""

    def test_get_project_root_finds_pyproject(self, tmp_path: Path):
        """Should find project root by pyproject.toml."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")
        subdir = tmp_path / "src" / "pkg"
        subdir.mkdir(parents=True)

        with patch("aiterm.cli.release.Path.cwd", return_value=subdir):
            root = get_project_root()
            assert root == tmp_path

    def test_get_version_from_pyproject(self, tmp_path: Path):
        """Should extract version from pyproject.toml."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "test"\nversion = "1.2.3"\n')

        version = get_version_from_pyproject(tmp_path)
        assert version == "1.2.3"

    def test_get_version_from_pyproject_missing(self, tmp_path: Path):
        """Should return None if pyproject.toml missing."""
        version = get_version_from_pyproject(tmp_path)
        assert version is None

    def test_get_version_from_init(self, tmp_path: Path):
        """Should extract version from __init__.py."""
        src = tmp_path / "src" / "aiterm"
        src.mkdir(parents=True)
        (src / "__init__.py").write_text('__version__ = "2.0.0"\n')

        version = get_version_from_init(tmp_path)
        assert version == "2.0.0"

    def test_get_version_from_init_missing(self, tmp_path: Path):
        """Should return None if __init__.py missing."""
        version = get_version_from_init(tmp_path)
        assert version is None

    def test_get_changelog_version(self, tmp_path: Path):
        """Should extract version from CHANGELOG.md."""
        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("""# Changelog

## [0.5.0] - 2025-01-01

### Added
- New feature

## [0.4.0] - 2024-12-30
""")

        version = get_changelog_version(tmp_path)
        assert version == "0.5.0"

    def test_get_changelog_version_missing(self, tmp_path: Path):
        """Should return None if CHANGELOG.md missing."""
        version = get_changelog_version(tmp_path)
        assert version is None


class TestGitHelpers:
    """Tests for git helper functions."""

    def test_run_command_success(self):
        """Should return exit code and output."""
        code, output = run_command(["echo", "hello"])
        assert code == 0
        assert "hello" in output

    def test_run_command_failure(self):
        """Should handle command failures."""
        code, output = run_command(["false"])
        assert code != 0

    def test_run_command_not_found(self):
        """Should handle missing commands."""
        code, output = run_command(["nonexistent_command_xyz"])
        assert code == 1
        assert "not found" in output.lower()

    @patch("aiterm.cli.release.run_command")
    def test_check_git_status_clean(self, mock_run):
        """Should detect clean working tree."""
        mock_run.return_value = (0, "")
        ok, msg = check_git_status(Path("."))
        assert ok is True
        assert "uncommitted" in msg.lower()

    @patch("aiterm.cli.release.run_command")
    def test_check_git_status_dirty(self, mock_run):
        """Should detect uncommitted changes."""
        mock_run.return_value = (0, "M src/file.py\n?? new_file.py")
        ok, msg = check_git_status(Path("."))
        assert ok is False
        assert "uncommitted" in msg.lower()

    @patch("aiterm.cli.release.run_command")
    def test_check_git_branch(self, mock_run):
        """Should get current branch."""
        mock_run.return_value = (0, "main")
        ok, branch, _ = check_git_branch()
        assert ok is True
        assert branch == "main"

    @patch("aiterm.cli.release.run_command")
    def test_check_tag_exists_true(self, mock_run):
        """Should detect existing tag."""
        mock_run.return_value = (0, "v1.0.0\nv1.1.0")
        assert check_tag_exists("1.0.0") is True

    @patch("aiterm.cli.release.run_command")
    def test_check_tag_exists_false(self, mock_run):
        """Should detect missing tag."""
        mock_run.return_value = (0, "v1.0.0\nv1.1.0")
        assert check_tag_exists("2.0.0") is False


class TestReleaseCheckCommand:
    """Tests for release check command."""

    def test_check_help(self):
        """Should show help text."""
        result = runner.invoke(app, ["check", "--help"])
        assert result.exit_code == 0
        assert "Validate release readiness" in result.output

    @patch("aiterm.cli.release.get_project_root")
    @patch("aiterm.cli.release.get_version_from_pyproject")
    @patch("aiterm.cli.release.get_version_from_init")
    @patch("aiterm.cli.release.get_changelog_version")
    @patch("aiterm.cli.release.check_git_status")
    @patch("aiterm.cli.release.check_git_branch")
    @patch("aiterm.cli.release.check_tag_exists")
    def test_check_all_pass(
        self,
        mock_tag,
        mock_branch,
        mock_status,
        mock_changelog,
        mock_init,
        mock_pyproject,
        mock_root,
        tmp_path,
    ):
        """Should pass when all checks pass."""
        mock_root.return_value = tmp_path
        mock_pyproject.return_value = "1.0.0"
        mock_init.return_value = "1.0.0"
        mock_changelog.return_value = "1.0.0"
        mock_status.return_value = (True, "Clean")
        mock_branch.return_value = (True, "main", "main")
        mock_tag.return_value = False

        result = runner.invoke(app, ["check", "--skip-tests"])
        assert result.exit_code == 0
        assert "Ready to release" in result.output

    @patch("aiterm.cli.release.get_project_root")
    @patch("aiterm.cli.release.get_version_from_pyproject")
    @patch("aiterm.cli.release.get_version_from_init")
    @patch("aiterm.cli.release.get_changelog_version")
    @patch("aiterm.cli.release.check_git_status")
    @patch("aiterm.cli.release.check_git_branch")
    @patch("aiterm.cli.release.check_tag_exists")
    def test_check_version_mismatch(
        self,
        mock_tag,
        mock_branch,
        mock_status,
        mock_changelog,
        mock_init,
        mock_pyproject,
        mock_root,
        tmp_path,
    ):
        """Should fail on version mismatch."""
        mock_root.return_value = tmp_path
        mock_pyproject.return_value = "1.0.0"
        mock_init.return_value = "1.0.1"  # Mismatch!
        mock_changelog.return_value = "1.0.0"
        mock_status.return_value = (True, "Clean")
        mock_branch.return_value = (True, "main", "main")
        mock_tag.return_value = False

        result = runner.invoke(app, ["check", "--skip-tests"])
        assert result.exit_code == 1
        assert "Not ready" in result.output


class TestReleaseStatusCommand:
    """Tests for release status command."""

    def test_status_help(self):
        """Should show help text."""
        result = runner.invoke(app, ["status", "--help"])
        assert result.exit_code == 0
        assert "current release state" in result.output.lower()

    @patch("aiterm.cli.release.get_project_root")
    @patch("aiterm.cli.release.get_version_from_pyproject")
    @patch("aiterm.cli.release.run_command")
    def test_status_shows_version(self, mock_run, mock_ver, mock_root, tmp_path):
        """Should show current version."""
        mock_root.return_value = tmp_path
        mock_ver.return_value = "0.5.0"
        mock_run.return_value = (0, "v0.4.0\nv0.3.0")

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "0.5.0" in result.output


class TestReleaseTagCommand:
    """Tests for release tag command."""

    def test_tag_help(self):
        """Should show help text."""
        result = runner.invoke(app, ["tag", "--help"])
        assert result.exit_code == 0
        assert "annotated git tag" in result.output.lower()

    @patch("aiterm.cli.release.get_project_root")
    @patch("aiterm.cli.release.get_version_from_pyproject")
    @patch("aiterm.cli.release.check_tag_exists")
    @patch("aiterm.cli.release.run_command")
    def test_tag_creates_tag(self, mock_run, mock_exists, mock_ver, mock_root, tmp_path):
        """Should create a new tag."""
        mock_root.return_value = tmp_path
        mock_ver.return_value = "0.5.0"
        mock_exists.return_value = False
        mock_run.return_value = (0, "")

        result = runner.invoke(app, ["tag", "0.5.0"])
        assert result.exit_code == 0
        assert "Created tag" in result.output

    @patch("aiterm.cli.release.get_project_root")
    @patch("aiterm.cli.release.check_tag_exists")
    def test_tag_exists_error(self, mock_exists, mock_root, tmp_path):
        """Should error if tag exists."""
        mock_root.return_value = tmp_path
        mock_exists.return_value = True

        result = runner.invoke(app, ["tag", "0.4.0"])
        assert result.exit_code == 1
        assert "already exists" in result.output
