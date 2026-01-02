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
        # Enable features for testing
        config = StatusLineConfig()
        config.set('display.show_lines_changed', True)

        renderer = StatusLineRenderer(config)
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
        config = StatusLineConfig()
        # Enable time features for testing
        config.set('display.show_current_time', True)
        config.set('display.show_session_duration', True)
        return config

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
        config = StatusLineConfig()
        # Enable lines changed feature for testing
        config.set('display.show_lines_changed', True)
        return config

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


class TestSpacingFeatures:
    """Test spacing features for gap between left and right segments."""

    @pytest.fixture
    def config(self, tmp_path, monkeypatch):
        """Create isolated config for testing."""
        # Use a temporary config file to avoid interference with user's config
        config_file = tmp_path / "test_statusline.json"
        monkeypatch.setenv('AITERM_CONFIG_DIR', str(tmp_path))
        config = StatusLineConfig()
        # Reset spacing to standard preset defaults
        config.set('spacing.mode', 'standard')
        config.set('spacing.min_gap', 10)
        config.set('spacing.max_gap', 40)
        config.set('spacing.show_separator', True)
        return config

    @pytest.fixture
    def renderer(self, config):
        return StatusLineRenderer(config)

    # =============================================================================
    # Gap Calculation Tests
    # =============================================================================

    def test_calculate_gap_standard_preset(self, renderer):
        """Test gap calculation with standard preset (20%)."""
        # Terminal width 120 * 0.20 = 24
        gap = renderer._calculate_gap(120)
        assert gap == 24

    def test_calculate_gap_minimal_preset(self, renderer, monkeypatch):
        """Test gap calculation with minimal preset (15%)."""
        renderer.config.set('spacing.mode', 'minimal')
        # Terminal width 120 * 0.15 = 18
        gap = renderer._calculate_gap(120)
        assert gap == 18

    def test_calculate_gap_spacious_preset(self, renderer, monkeypatch):
        """Test gap calculation with spacious preset (30%)."""
        renderer.config.set('spacing.mode', 'spacious')
        # Terminal width 120 * 0.30 = 36
        gap = renderer._calculate_gap(120)
        assert gap == 36

    def test_calculate_gap_min_constraint(self, renderer):
        """Test gap respects minimum constraint."""
        # Very narrow terminal: 50 * 0.20 = 10
        # Standard preset min_gap is 10, should not go below
        gap = renderer._calculate_gap(50)
        assert gap >= 10

        # Even narrower: 40 * 0.20 = 8, should clamp to min_gap=10
        gap = renderer._calculate_gap(40)
        assert gap == 10

    def test_calculate_gap_max_constraint(self, renderer):
        """Test gap respects maximum constraint."""
        # Very wide terminal: 300 * 0.20 = 60
        # Standard preset max_gap is 40, should not exceed
        gap = renderer._calculate_gap(300)
        assert gap == 40

    def test_calculate_gap_config_overrides(self, renderer):
        """Test config overrides for min/max gap."""
        # Set custom min/max
        renderer.config.set('spacing.min_gap', 15)
        renderer.config.set('spacing.max_gap', 30)

        # Test min override: 60 * 0.20 = 12, should clamp to 15
        gap = renderer._calculate_gap(60)
        assert gap == 15

        # Test max override: 200 * 0.20 = 40, should clamp to 30
        gap = renderer._calculate_gap(200)
        assert gap == 30

    # =============================================================================
    # Gap Rendering Tests
    # =============================================================================

    def test_render_gap_with_separator(self, renderer):
        """Test gap rendering with centered separator."""
        gap = renderer._render_gap(20)

        # Should contain separator (…) in ANSI wrapper
        assert '…' in gap
        # Should have ANSI color code (38;5;240m for dim gray)
        assert '\033[38;5;240m' in gap
        # Total visible length should be 20 (spaces + separator)
        visible_length = renderer._strip_ansi_length(gap)
        assert visible_length == 20

    def test_render_gap_without_separator(self, renderer):
        """Test gap rendering with separator disabled."""
        renderer.config.set('spacing.show_separator', False)
        gap = renderer._render_gap(20)

        # Should not contain separator
        assert '…' not in gap
        # Should be just spaces
        assert gap == ' ' * 20

    def test_render_gap_too_small_for_separator(self, renderer):
        """Test gap rendering when too small for separator."""
        # Gap of 2 is too small for separator (needs >= 3)
        gap = renderer._render_gap(2)

        # Should fall back to just spaces
        assert gap == '  '
        assert '…' not in gap

    # =============================================================================
    # Alignment Integration Tests
    # =============================================================================

    def test_align_line_with_spacing(self, renderer, monkeypatch):
        """Test line alignment uses spacing system."""
        # Mock terminal width
        from collections import namedtuple
        TerminalSize = namedtuple('TerminalSize', ['columns', 'lines'])

        def mock_get_terminal_size(fallback=None):
            return TerminalSize(columns=120, lines=24)

        import shutil
        monkeypatch.setattr(shutil, 'get_terminal_size', mock_get_terminal_size)

        left = "Left side"
        right = "Right side"

        aligned = renderer._align_line(left, right)

        # Should contain both sides
        assert "Left side" in aligned
        assert "Right side" in aligned

        # Should have gap with separator (if enabled)
        if renderer.config.get('spacing.show_separator', True):
            assert '…' in aligned

    def test_align_line_narrow_terminal(self, renderer, monkeypatch):
        """Test line alignment on narrow terminal."""
        # Mock narrow terminal (80 cols)
        from collections import namedtuple
        TerminalSize = namedtuple('TerminalSize', ['columns', 'lines'])

        def mock_get_terminal_size(fallback=None):
            return TerminalSize(columns=80, lines=24)

        import shutil
        monkeypatch.setattr(shutil, 'get_terminal_size', mock_get_terminal_size)

        left = "Left side with longer text"
        right = "Right side"

        aligned = renderer._align_line(left, right)

        # Should still contain both sides if there's any room
        assert "Left side" in aligned

    def test_align_line_fallback_to_left_only(self, renderer, monkeypatch):
        """Test line alignment falls back to left-only on very narrow terminal."""
        # Mock very narrow terminal (40 cols)
        from collections import namedtuple
        TerminalSize = namedtuple('TerminalSize', ['columns', 'lines'])

        def mock_get_terminal_size(fallback=None):
            return TerminalSize(columns=40, lines=24)

        import shutil
        monkeypatch.setattr(shutil, 'get_terminal_size', mock_get_terminal_size)

        left = "This is a very long left side segment that takes up lots of space"
        right = "Right"

        aligned = renderer._align_line(left, right)

        # Should fall back to left-only when no room for right side
        assert "This is a very long left side" in aligned

    # =============================================================================
    # Additional Edge Case Tests
    # =============================================================================

    def test_calculate_gap_invalid_preset(self, renderer):
        """Test gap calculation with invalid preset name."""
        # Config validation prevents invalid presets - this should raise ValueError
        import pytest
        with pytest.raises(ValueError) as exc_info:
            renderer.config.set('spacing.mode', 'invalid-preset')

        # Error message should list valid choices
        assert "Valid choices: minimal, standard, spacious" in str(exc_info.value)

    def test_calculate_gap_very_narrow_terminal(self, renderer):
        """Test gap calculation on very narrow terminal."""
        # 40 columns * 0.20 = 8, but min_gap is 10
        gap = renderer._calculate_gap(40)
        assert gap == 10  # Should clamp to min_gap

    def test_calculate_gap_very_wide_terminal(self, renderer):
        """Test gap calculation on ultra-wide terminal."""
        # 400 columns * 0.20 = 80, but max_gap is 40
        gap = renderer._calculate_gap(400)
        assert gap == 40  # Should clamp to max_gap

    def test_render_gap_exact_3_chars(self, renderer):
        """Test separator rendering with exactly 3 chars (minimum)."""
        gap = renderer._render_gap(3)

        # Should contain separator
        assert '…' in gap
        # Should have correct visible length
        visible_length = renderer._strip_ansi_length(gap)
        assert visible_length == 3

    def test_render_gap_odd_width(self, renderer):
        """Test separator centering with odd gap width."""
        gap = renderer._render_gap(7)

        # Should have correct visible length
        visible_length = renderer._strip_ansi_length(gap)
        assert visible_length == 7
        # Should contain separator
        assert '…' in gap

    def test_render_gap_even_width(self, renderer):
        """Test separator centering with even gap width."""
        gap = renderer._render_gap(8)

        # Should have correct visible length
        visible_length = renderer._strip_ansi_length(gap)
        assert visible_length == 8
        # Should contain separator
        assert '…' in gap

    def test_strip_ansi_complex_codes(self, renderer):
        """Test ANSI stripping with multiple escape sequences."""
        # Multiple codes: bold + color
        text = "\033[38;5;240m\033[1mBold and colored\033[0m"
        length = renderer._strip_ansi_length(text)
        assert length == len("Bold and colored")

    def test_strip_ansi_nested_codes(self, renderer):
        """Test nested ANSI codes."""
        # Nested codes with text between
        text = "\033[1m\033[31mRed bold\033[0m normal"
        length = renderer._strip_ansi_length(text)
        assert length == len("Red bold normal")

    def test_strip_ansi_no_codes(self, renderer):
        """Test ANSI stripping with plain text (no codes)."""
        text = "Plain text without codes"
        length = renderer._strip_ansi_length(text)
        assert length == len(text)
