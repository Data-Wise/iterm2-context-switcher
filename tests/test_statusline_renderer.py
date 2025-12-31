"""Tests for StatusLine renderer and segments."""

import json
import pytest
from pathlib import Path

from aiterm.statusline.renderer import StatusLineRenderer
from aiterm.statusline.segments import (
    ProjectSegment,
    GitSegment,
    ModelSegment,
    TimeSegment,
    ThinkingSegment,
    LinesSegment,
)
from aiterm.statusline.config import StatusLineConfig


class TestStatusLineRenderer:
    """Test StatusLineRenderer class."""

    @pytest.fixture
    def mock_json(self):
        """Create mock JSON input."""
        return json.dumps({
            "workspace": {
                "current_dir": "/Users/dt/projects/dev-tools/aiterm",
                "project_dir": "/Users/dt/projects/dev-tools/aiterm"
            },
            "model": {
                "display_name": "Claude Sonnet 4.5"
            },
            "output_style": {
                "name": "learning"
            },
            "session_id": "test-123",
            "cost": {
                "total_lines_added": 123,
                "total_lines_removed": 45,
                "total_duration_ms": 45000
            }
        })

    def test_render_basic(self, mock_json):
        """Test basic rendering."""
        renderer = StatusLineRenderer()
        output = renderer.render(mock_json)

        assert isinstance(output, str)
        assert "╭─" in output  # Line 1 start
        assert "╰─" in output  # Line 2 start
        assert "Sonnet" in output  # Model name
        assert "+123" in output  # Lines added

    def test_render_invalid_json(self):
        """Test rendering with invalid JSON."""
        renderer = StatusLineRenderer()
        output = renderer.render("{ invalid json }")

        assert "Invalid JSON" in output

    def test_render_two_lines(self, mock_json):
        """Test output has exactly 2 lines."""
        renderer = StatusLineRenderer()
        output = renderer.render(mock_json)

        # Remove ANSI window title escape sequence
        lines = output.split('\n')
        # Should have 2 lines (plus possible empty line at end)
        assert len([l for l in lines if l]) >= 2


class TestProjectSegment:
    """Test ProjectSegment class."""

    @pytest.fixture
    def config(self):
        """Create test config."""
        return StatusLineConfig()

    @pytest.fixture
    def segment(self, config):
        """Create ProjectSegment."""
        return ProjectSegment(config)

    def test_python_project_icon(self, segment, tmp_path):
        """Test Python project detection."""
        # Create pyproject.toml
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'")

        icon = segment._get_project_icon(str(tmp_path))
        assert icon == "🐍"

    def test_r_package_icon(self, segment, tmp_path):
        """Test R package detection."""
        # Create DESCRIPTION file
        (tmp_path / "DESCRIPTION").write_text("Package: testpkg\nVersion: 1.0.0")

        icon = segment._get_project_icon(str(tmp_path))
        assert icon == "📦"

    def test_default_icon(self, segment, tmp_path):
        """Test default icon for unknown project type."""
        icon = segment._get_project_icon(str(tmp_path))
        assert icon == "📁"

    def test_format_directory_basename(self, segment, tmp_path, monkeypatch):
        """Test basename directory mode."""
        # Mock config to return basename mode
        def mock_get(key, default=None):
            if key == 'display.directory_mode':
                return 'basename'
            return default

        monkeypatch.setattr(segment.config, 'get', mock_get)

        result = segment._format_directory(str(tmp_path), str(tmp_path))
        assert result == tmp_path.name

    def test_r_version_detection(self, segment, tmp_path):
        """Test R package version detection."""
        desc_file = tmp_path / "DESCRIPTION"
        desc_file.write_text("Package: testpkg\nVersion: 1.2.3\nTitle: Test")

        version = segment._get_r_version(str(tmp_path))
        assert version == "v1.2.3"

    def test_r_version_missing(self, segment, tmp_path):
        """Test R version when DESCRIPTION doesn't exist."""
        version = segment._get_r_version(str(tmp_path))
        assert version is None


class TestModelSegment:
    """Test ModelSegment class."""

    @pytest.fixture
    def config(self):
        return StatusLineConfig()

    @pytest.fixture
    def segment(self, config):
        return ModelSegment(config)

    def test_render_sonnet(self, segment):
        """Test rendering Sonnet model."""
        output = segment.render("Claude Sonnet 4.5")

        assert "Sonnet" in output
        assert "Claude" not in output  # Shortened
        assert "\033[" in output  # Has ANSI color codes

    def test_render_opus(self, segment):
        """Test rendering Opus model."""
        output = segment.render("Claude Opus 4")

        assert "Opus" in output
        assert "Claude" not in output

    def test_render_haiku(self, segment):
        """Test rendering Haiku model."""
        output = segment.render("Claude Haiku 3.5")

        assert "Haiku" in output


class TestTimeSegment:
    """Test TimeSegment class."""

    @pytest.fixture
    def config(self):
        return StatusLineConfig()

    @pytest.fixture
    def segment(self, config):
        return TimeSegment(config)

    def test_render_includes_time(self, segment):
        """Test rendering includes current time."""
        output = segment.render("test-session")

        assert "│" in output  # Separator
        # Should have time in HH:MM format (ANSI-wrapped)
        assert ":" in output

    def test_render_includes_duration(self, segment):
        """Test rendering includes session duration."""
        output = segment.render("test-session")

        assert "⏱" in output  # Duration icon

    def test_session_duration_format(self, segment):
        """Test session duration formatting."""
        # Clean up any existing session file
        from pathlib import Path
        session_file = Path("/tmp/claude-session-new-session-test")
        if session_file.exists():
            session_file.unlink()

        # New session
        duration = segment._get_session_duration("new-session-test")
        assert duration in ["0m", "<1m"]


class TestLinesSegment:
    """Test LinesSegment class."""

    @pytest.fixture
    def config(self):
        return StatusLineConfig()

    @pytest.fixture
    def segment(self, config):
        return LinesSegment(config)

    def test_render_with_changes(self, segment):
        """Test rendering with lines changed."""
        output = segment.render(123, 45)

        assert "+123" in output
        assert "45" in output

    def test_render_no_changes(self, segment):
        """Test rendering with no changes."""
        output = segment.render(0, 0)

        assert output == ""

    def test_render_only_additions(self, segment):
        """Test rendering with only additions."""
        output = segment.render(50, 0)

        assert "+50" in output

    def test_render_disabled_in_config(self, segment, monkeypatch):
        """Test rendering when disabled in config."""
        def mock_get(key, default=None):
            if key == 'display.show_lines_changed':
                return False
            return default

        monkeypatch.setattr(segment.config, 'get', mock_get)

        output = segment.render(100, 50)
        assert output == ""


class TestThinkingSegment:
    """Test ThinkingSegment class."""

    @pytest.fixture
    def config(self):
        return StatusLineConfig()

    @pytest.fixture
    def segment(self, config):
        return ThinkingSegment(config)

    def test_render_when_settings_missing(self, segment):
        """Test rendering when settings file doesn't exist."""
        output = segment.render()

        # Should return empty string gracefully
        assert output == ""
