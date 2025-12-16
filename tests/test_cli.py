"""Tests for aiterm CLI."""

from typer.testing import CliRunner

from aiterm import __version__
from aiterm.cli.main import app

runner = CliRunner()


def test_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "aiterm" in result.output


def test_init():
    """Test init command."""
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Setup wizard" in result.output


def test_doctor():
    """Test doctor command."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Health check" in result.output


def test_profile_list():
    """Test profile list command."""
    result = runner.invoke(app, ["profile", "list"])
    assert result.exit_code == 0
    assert "Available Profiles" in result.output


def test_claude_settings():
    """Test claude settings command."""
    result = runner.invoke(app, ["claude", "settings"])
    assert result.exit_code == 0
