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


def test_context_detect():
    """Test context detect command."""
    result = runner.invoke(app, ["context", "detect"])
    assert result.exit_code == 0
    assert "Context Detection" in result.output


def test_context_show():
    """Test context show command."""
    result = runner.invoke(app, ["context", "show"])
    assert result.exit_code == 0
    assert "Context Detection" in result.output


def test_context_apply():
    """Test context apply command."""
    result = runner.invoke(app, ["context", "apply"])
    assert result.exit_code == 0
    # Should show warning about not being in iTerm2
    assert "Context Detection" in result.output


# ─── Shortcut command tests ──────────────────────────────────────────────────


def test_detect_shortcut():
    """Test detect shortcut command."""
    result = runner.invoke(app, ["detect"])
    assert result.exit_code == 0
    assert "Context Detection" in result.output


def test_switch_shortcut():
    """Test switch shortcut command."""
    result = runner.invoke(app, ["switch"])
    assert result.exit_code == 0
    assert "Context Detection" in result.output


# ─── Claude command tests ────────────────────────────────────────────────────


def test_claude_backup():
    """Test claude backup command."""
    result = runner.invoke(app, ["claude", "backup"])
    # Will either create backup or report no settings found
    assert result.exit_code == 0


def test_claude_approvals_list():
    """Test claude approvals list command."""
    result = runner.invoke(app, ["claude", "approvals", "list"])
    assert result.exit_code == 0


def test_claude_approvals_presets():
    """Test claude approvals presets command."""
    result = runner.invoke(app, ["claude", "approvals", "presets"])
    assert result.exit_code == 0
    assert "Available Presets" in result.output
    assert "safe-reads" in result.output
    assert "git-ops" in result.output
