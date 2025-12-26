"""Tests for Phase 3-4 CLI modules: gemini, statusbar, terminals, workflows, sessions.

Self-diagnosing test suite with validation.
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """Mock home directory."""
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path


# =============================================================================
# Gemini CLI Tests (Phase 3.1)
# =============================================================================


class TestGeminiCLI:
    """Tests for gemini CLI module."""

    def test_import_module(self):
        """Test module imports correctly."""
        from aiterm.cli import gemini
        assert hasattr(gemini, "app")
        assert hasattr(gemini, "GeminiConfig")
        assert hasattr(gemini, "GEMINI_MODELS")

    def test_gemini_config_dataclass(self):
        """Test GeminiConfig dataclass."""
        from aiterm.cli.gemini import GeminiConfig

        config = GeminiConfig(
            model="gemini-2.0-flash",
            sandbox=True,
            yolo=False,
        )
        assert config.model == "gemini-2.0-flash"
        assert config.sandbox is True
        assert config.yolo is False

    def test_gemini_models_defined(self):
        """Test GEMINI_MODELS has expected entries."""
        from aiterm.cli.gemini import GEMINI_MODELS

        assert "gemini-2.0-flash" in GEMINI_MODELS
        assert "gemini-1.5-pro" in GEMINI_MODELS

    def test_gemini_config_to_dict(self):
        """Test GeminiConfig.to_dict()."""
        from aiterm.cli.gemini import GeminiConfig

        config = GeminiConfig(
            model="gemini-1.5-pro",
            yolo=True,
        )
        d = config.to_dict()
        assert d["model"] == "gemini-1.5-pro"
        assert d["yolo"] is True

    def test_gemini_models_command(self, runner):
        """Test gemini models command."""
        from aiterm.cli.gemini import app

        result = runner.invoke(app, ["models"])
        assert result.exit_code == 0
        assert "gemini" in result.output.lower()


# =============================================================================
# StatusBar CLI Tests (Phase 3.2)
# =============================================================================


class TestStatusBarCLI:
    """Tests for statusbar CLI module."""

    def test_import_module(self):
        """Test module imports correctly."""
        from aiterm.cli import statusbar
        assert hasattr(statusbar, "app")
        assert hasattr(statusbar, "StatusBarConfig")
        assert hasattr(statusbar, "STATUSBAR_TEMPLATES")

    def test_statusbar_config_dataclass(self):
        """Test StatusBarConfig dataclass."""
        from aiterm.cli.statusbar import StatusBarConfig

        config = StatusBarConfig(
            name="test",
            type="command",
            command="/bin/bash script.sh",
        )
        assert config.name == "test"
        assert config.type == "command"

    def test_statusbar_templates_exist(self):
        """Test built-in templates are defined."""
        from aiterm.cli.statusbar import STATUSBAR_TEMPLATES

        expected = ["minimal", "powerlevel10k", "developer", "stats"]
        for name in expected:
            assert name in STATUSBAR_TEMPLATES, f"Missing template: {name}"

    def test_statusbar_config_to_dict(self):
        """Test StatusBarConfig.to_dict()."""
        from aiterm.cli.statusbar import StatusBarConfig

        config = StatusBarConfig(
            name="test",
            type="command",
            command="/bin/bash test.sh",
        )
        d = config.to_dict()
        assert d["type"] == "command"
        assert d["command"] == "/bin/bash test.sh"

    def test_statusbar_templates_command(self, runner):
        """Test statusbar templates command."""
        from aiterm.cli.statusbar import app

        result = runner.invoke(app, ["templates"])
        assert result.exit_code == 0
        assert "minimal" in result.output or "powerlevel10k" in result.output

    def test_statusbar_components_command(self, runner):
        """Test statusbar components command."""
        from aiterm.cli.statusbar import app

        result = runner.invoke(app, ["components"])
        assert result.exit_code == 0
        assert "model" in result.output.lower()


# =============================================================================
# Terminals CLI Tests (Phase 4.1)
# =============================================================================


class TestTerminalsCLI:
    """Tests for terminals CLI module."""

    def test_import_module(self):
        """Test module imports correctly."""
        from aiterm.cli import terminals
        assert hasattr(terminals, "app")
        assert hasattr(terminals, "TerminalType")
        assert hasattr(terminals, "BACKENDS")

    def test_terminal_type_enum(self):
        """Test TerminalType enum."""
        from aiterm.cli.terminals import TerminalType

        assert TerminalType.ITERM2.value == "iterm2"
        assert TerminalType.KITTY.value == "kitty"
        assert TerminalType.ALACRITTY.value == "alacritty"

    def test_terminal_backends_registered(self):
        """Test all backends are registered."""
        from aiterm.cli.terminals import BACKENDS, TerminalType

        # Should have at least iTerm2, Kitty, Alacritty, WezTerm, Ghostty
        assert TerminalType.ITERM2 in BACKENDS
        assert TerminalType.KITTY in BACKENDS
        assert TerminalType.ALACRITTY in BACKENDS

    def test_iterm2_backend_features(self):
        """Test iTerm2 backend has expected features."""
        from aiterm.cli.terminals import ITerm2Backend

        backend = ITerm2Backend()
        features = backend.get_features()
        assert "profiles" in features
        assert "tab_title" in features

    def test_detect_current_terminal(self, monkeypatch):
        """Test terminal detection."""
        from aiterm.cli.terminals import detect_current_terminal, TerminalType

        # Mock iTerm2
        monkeypatch.setenv("ITERM_SESSION_ID", "test")
        assert detect_current_terminal() == TerminalType.ITERM2

        # Clear and test unknown
        monkeypatch.delenv("ITERM_SESSION_ID")
        monkeypatch.setenv("TERM_PROGRAM", "unknown")
        result = detect_current_terminal()
        # Could be UNKNOWN or another detected terminal

    def test_terminals_list_command(self, runner):
        """Test terminals list command."""
        from aiterm.cli.terminals import app

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "iterm2" in result.output.lower() or "terminal" in result.output.lower()


# =============================================================================
# Workflows CLI Tests (Phase 4.2)
# =============================================================================


class TestWorkflowsCLI:
    """Tests for workflows CLI module."""

    def test_import_module(self):
        """Test module imports correctly."""
        from aiterm.cli import workflows
        assert hasattr(workflows, "app")
        assert hasattr(workflows, "WorkflowTemplate")
        assert hasattr(workflows, "WORKFLOW_TEMPLATES")

    def test_workflow_template_dataclass(self):
        """Test WorkflowTemplate dataclass."""
        from aiterm.cli.workflows import WorkflowTemplate

        wf = WorkflowTemplate(
            name="test-workflow",
            description="Test",
            context_type="python",
            auto_approvals=["Bash(python:*)"],
        )
        assert wf.name == "test-workflow"
        assert wf.context_type == "python"

    def test_workflow_templates_exist(self):
        """Test built-in templates are defined."""
        from aiterm.cli.workflows import WORKFLOW_TEMPLATES

        expected = ["r-development", "python-development", "node-development", "research"]
        for name in expected:
            assert name in WORKFLOW_TEMPLATES, f"Missing template: {name}"

    def test_workflow_to_dict(self):
        """Test WorkflowTemplate.to_dict()."""
        from aiterm.cli.workflows import WorkflowTemplate

        wf = WorkflowTemplate(
            name="test",
            description="Test",
            auto_approvals=["Bash(pytest:*)"],
        )
        d = wf.to_dict()
        assert d["name"] == "test"
        assert "auto_approvals" in d

    def test_workflows_list_command(self, runner):
        """Test workflows list command."""
        from aiterm.cli.workflows import app

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "r-development" in result.output or "python" in result.output.lower()


# =============================================================================
# Sessions CLI Tests (Phase 4.3)
# =============================================================================


class TestSessionsCLI:
    """Tests for sessions CLI module."""

    def test_import_module(self):
        """Test module imports correctly."""
        from aiterm.cli import sessions
        assert hasattr(sessions, "app")
        assert hasattr(sessions, "Session")
        assert hasattr(sessions, "load_sessions")

    def test_session_dataclass(self):
        """Test Session dataclass."""
        from aiterm.cli.sessions import Session

        session = Session(
            id="test-123",
            project="myproject",
            started=datetime.now(),
        )
        assert session.id == "test-123"
        assert session.project == "myproject"
        assert session.is_active is True  # No ended time

    def test_session_duration(self):
        """Test Session.duration property."""
        from aiterm.cli.sessions import Session

        start = datetime.now() - timedelta(hours=2, minutes=30)
        session = Session(
            id="test",
            project="proj",
            started=start,
        )
        duration = session.duration
        assert duration.seconds >= 2 * 3600  # At least 2 hours

    def test_session_duration_str(self):
        """Test Session.duration_str property."""
        from aiterm.cli.sessions import Session

        start = datetime.now() - timedelta(minutes=45)
        session = Session(id="test", project="proj", started=start)
        assert "45m" in session.duration_str or "44m" in session.duration_str

    def test_session_to_dict(self):
        """Test Session.to_dict()."""
        from aiterm.cli.sessions import Session

        session = Session(
            id="test-123",
            project="myproject",
            started=datetime.now(),
            workflow="python-development",
            commits=5,
        )
        d = session.to_dict()
        assert d["id"] == "test-123"
        assert d["project"] == "myproject"
        assert d["workflow"] == "python-development"
        assert d["commits"] == 5

    def test_session_from_dict(self):
        """Test Session.from_dict()."""
        from aiterm.cli.sessions import Session

        data = {
            "id": "test-456",
            "project": "testproj",
            "started": datetime.now().isoformat(),
            "ended": None,
            "commits": 3,
        }
        session = Session.from_dict(data)
        assert session.id == "test-456"
        assert session.commits == 3

    def test_generate_session_id(self):
        """Test session ID generation."""
        from aiterm.cli.sessions import generate_session_id

        id1 = generate_session_id()
        id2 = generate_session_id()
        assert id1 != id2
        assert len(id1) > 10

    def test_sessions_status_command(self, runner):
        """Test sessions status command."""
        from aiterm.cli.sessions import app

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0


# =============================================================================
# Self-Diagnostic Tests
# =============================================================================


class TestPhase34SelfDiagnostics:
    """Self-diagnosing tests for Phase 3-4 modules."""

    def test_all_phase34_modules_importable(self):
        """Verify all Phase 3-4 modules can be imported."""
        modules = ["gemini", "statusbar", "terminals", "workflows", "sessions"]
        for name in modules:
            try:
                module = __import__(f"aiterm.cli.{name}", fromlist=[name])
                assert hasattr(module, "app"), f"{name}.app missing"
            except ImportError as e:
                pytest.fail(f"Failed to import aiterm.cli.{name}: {e}")

    def test_all_cli_apps_are_typer(self):
        """Verify all CLI apps are Typer instances."""
        import typer
        from aiterm.cli import gemini, statusbar, terminals, workflows, sessions

        for module in [gemini, statusbar, terminals, workflows, sessions]:
            assert isinstance(module.app, typer.Typer), f"{module.__name__}.app is not Typer"

    def test_templates_have_descriptions(self):
        """Verify all templates have descriptions."""
        from aiterm.cli.statusbar import STATUSBAR_TEMPLATES
        from aiterm.cli.workflows import WORKFLOW_TEMPLATES

        for name, template in STATUSBAR_TEMPLATES.items():
            assert "description" in template, f"statusbar template {name} missing description"

        for name, wf in WORKFLOW_TEMPLATES.items():
            assert wf.description, f"workflow template {name} missing description"

    def test_dataclasses_serializable(self):
        """Verify dataclasses can be serialized to JSON."""
        from aiterm.cli.gemini import GeminiConfig
        from aiterm.cli.statusbar import StatusBarConfig
        from aiterm.cli.workflows import WorkflowTemplate
        from aiterm.cli.sessions import Session

        # Test GeminiConfig
        gc = GeminiConfig(model="test")
        json.dumps(gc.to_dict())

        # Test StatusBarConfig
        sc = StatusBarConfig(name="test", type="command", command="echo hi")
        json.dumps(sc.to_dict())

        # Test WorkflowTemplate
        wt = WorkflowTemplate(name="test")
        json.dumps(wt.to_dict())

        # Test Session
        s = Session(id="test", project="proj", started=datetime.now())
        json.dumps(s.to_dict())
