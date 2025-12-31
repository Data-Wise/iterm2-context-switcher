"""Tests for the tutorial module."""

import pytest
from aiterm.utils.tutorial import (
    TutorialLevel,
    TutorialStep,
    Tutorial,
    get_tutorial,
    list_tutorials,
    parse_level,
    create_getting_started_tutorial,
    create_intermediate_tutorial,
    create_advanced_tutorial,
)


class TestTutorialLevel:
    """Tests for TutorialLevel enum."""

    def test_level_values(self):
        """Test enum values."""
        assert TutorialLevel.GETTING_STARTED.value == "getting-started"
        assert TutorialLevel.INTERMEDIATE.value == "intermediate"
        assert TutorialLevel.ADVANCED.value == "advanced"

    def test_display_name(self):
        """Test display name property."""
        assert TutorialLevel.GETTING_STARTED.display_name == "Getting Started"
        assert TutorialLevel.INTERMEDIATE.display_name == "Intermediate"
        assert TutorialLevel.ADVANCED.display_name == "Advanced"

    def test_step_count(self):
        """Test step count property."""
        assert TutorialLevel.GETTING_STARTED.step_count == 7
        assert TutorialLevel.INTERMEDIATE.step_count == 11
        assert TutorialLevel.ADVANCED.step_count == 13

    def test_duration(self):
        """Test duration property."""
        assert TutorialLevel.GETTING_STARTED.duration == "~10 min"
        assert TutorialLevel.INTERMEDIATE.duration == "~20 min"
        assert TutorialLevel.ADVANCED.duration == "~35 min"

    def test_description(self):
        """Test description property."""
        assert "Essential" in TutorialLevel.GETTING_STARTED.description
        assert "Claude Code" in TutorialLevel.INTERMEDIATE.description
        assert "Release" in TutorialLevel.ADVANCED.description


class TestTutorialStep:
    """Tests for TutorialStep dataclass."""

    def test_basic_step(self):
        """Test creating a basic step."""
        step = TutorialStep(
            number=1,
            title="Test Step",
            description="A test step.",
        )
        assert step.number == 1
        assert step.title == "Test Step"
        assert step.description == "A test step."
        assert step.command is None
        assert step.hint is None

    def test_step_with_command(self):
        """Test creating a step with command."""
        step = TutorialStep(
            number=2,
            title="Command Step",
            description="Run a command.",
            command="ait doctor",
            hint="Check installation",
            interactive=True,
        )
        assert step.command == "ait doctor"
        assert step.hint == "Check installation"
        assert step.interactive is True

    def test_step_with_visuals(self):
        """Test creating a step with GIF and diagram."""
        step = TutorialStep(
            number=3,
            title="Visual Step",
            description="Step with visuals.",
            gif_path="docs/demos/tutorials/example.gif",
            diagram="flowchart TD\n    A-->B",
        )
        assert step.gif_path == "docs/demos/tutorials/example.gif"
        assert step.diagram is not None


class TestTutorial:
    """Tests for Tutorial class."""

    def test_tutorial_creation(self):
        """Test creating a tutorial."""
        tutorial = Tutorial(
            level=TutorialLevel.GETTING_STARTED,
            title="Test Tutorial",
            description="A test tutorial.",
            steps=[
                TutorialStep(number=1, title="Step 1", description="First step"),
                TutorialStep(number=2, title="Step 2", description="Second step"),
            ],
        )
        assert tutorial.level == TutorialLevel.GETTING_STARTED
        assert tutorial.title == "Test Tutorial"
        assert len(tutorial.steps) == 2

    def test_show_step_valid(self):
        """Test showing a valid step."""
        tutorial = Tutorial(
            level=TutorialLevel.GETTING_STARTED,
            title="Test",
            description="Test",
            steps=[
                TutorialStep(number=1, title="Step 1", description="First"),
            ],
        )
        step = tutorial.show_step(1)
        assert step.number == 1

    def test_show_step_invalid(self):
        """Test showing invalid step raises error."""
        tutorial = Tutorial(
            level=TutorialLevel.GETTING_STARTED,
            title="Test",
            description="Test",
            steps=[
                TutorialStep(number=1, title="Step 1", description="First"),
            ],
        )
        with pytest.raises(ValueError, match="Step 0 not found"):
            tutorial.show_step(0)
        with pytest.raises(ValueError, match="Step 2 not found"):
            tutorial.show_step(2)


class TestTutorialFactories:
    """Tests for tutorial factory functions."""

    def test_getting_started_tutorial(self):
        """Test Getting Started tutorial factory."""
        tutorial = create_getting_started_tutorial()
        assert tutorial.level == TutorialLevel.GETTING_STARTED
        assert len(tutorial.steps) == 7
        assert "aiterm" in tutorial.title.lower()

    def test_intermediate_tutorial(self):
        """Test Intermediate tutorial factory."""
        tutorial = create_intermediate_tutorial()
        assert tutorial.level == TutorialLevel.INTERMEDIATE
        assert len(tutorial.steps) == 11
        assert len(tutorial.prerequisites) >= 1

    def test_advanced_tutorial(self):
        """Test Advanced tutorial factory."""
        tutorial = create_advanced_tutorial()
        assert tutorial.level == TutorialLevel.ADVANCED
        assert len(tutorial.steps) == 13
        assert len(tutorial.prerequisites) >= 1

    def test_all_tutorials_have_numbered_steps(self):
        """Test that all tutorials have properly numbered steps."""
        for factory in [
            create_getting_started_tutorial,
            create_intermediate_tutorial,
            create_advanced_tutorial,
        ]:
            tutorial = factory()
            for i, step in enumerate(tutorial.steps, 1):
                assert step.number == i, f"Step {i} has wrong number in {tutorial.title}"

    def test_tutorials_have_required_fields(self):
        """Test all steps have required fields."""
        for factory in [
            create_getting_started_tutorial,
            create_intermediate_tutorial,
            create_advanced_tutorial,
        ]:
            tutorial = factory()
            for step in tutorial.steps:
                assert step.title, f"Step {step.number} missing title"
                assert step.description, f"Step {step.number} missing description"


class TestTutorialHelpers:
    """Tests for helper functions."""

    def test_get_tutorial(self):
        """Test getting tutorial by level."""
        tutorial = get_tutorial(TutorialLevel.GETTING_STARTED)
        assert tutorial.level == TutorialLevel.GETTING_STARTED

        tutorial = get_tutorial(TutorialLevel.INTERMEDIATE)
        assert tutorial.level == TutorialLevel.INTERMEDIATE

        tutorial = get_tutorial(TutorialLevel.ADVANCED)
        assert tutorial.level == TutorialLevel.ADVANCED

    def test_parse_level_exact(self):
        """Test parsing exact level strings."""
        assert parse_level("getting-started") == TutorialLevel.GETTING_STARTED
        assert parse_level("intermediate") == TutorialLevel.INTERMEDIATE
        assert parse_level("advanced") == TutorialLevel.ADVANCED

    def test_parse_level_partial(self):
        """Test parsing partial level strings (min 3 chars)."""
        assert parse_level("getting") == TutorialLevel.GETTING_STARTED
        assert parse_level("inter") == TutorialLevel.INTERMEDIATE
        assert parse_level("adv") == TutorialLevel.ADVANCED
        # Short partials (< 3 chars) don't match
        assert parse_level("ge") is None
        assert parse_level("in") is None

    def test_parse_level_case_insensitive(self):
        """Test parsing is case insensitive."""
        assert parse_level("GETTING-STARTED") == TutorialLevel.GETTING_STARTED
        assert parse_level("Intermediate") == TutorialLevel.INTERMEDIATE
        assert parse_level("ADVANCED") == TutorialLevel.ADVANCED

    def test_parse_level_invalid(self):
        """Test parsing invalid level returns None."""
        assert parse_level("invalid") is None
        assert parse_level("") is None
        assert parse_level("xyz") is None

    def test_list_tutorials(self, capsys):
        """Test listing tutorials produces output."""
        list_tutorials()
        # Just verify it doesn't crash - output is rich formatted


class TestTutorialStepCounts:
    """Tests to verify step counts match spec."""

    def test_total_step_count(self):
        """Test total steps: 7 + 11 + 13 = 31."""
        total = (
            len(create_getting_started_tutorial().steps) +
            len(create_intermediate_tutorial().steps) +
            len(create_advanced_tutorial().steps)
        )
        assert total == 31

    def test_enum_matches_actual(self):
        """Test enum step counts match actual step counts."""
        for level in TutorialLevel:
            tutorial = get_tutorial(level)
            assert len(tutorial.steps) == level.step_count, (
                f"{level.value} enum says {level.step_count} "
                f"but tutorial has {len(tutorial.steps)} steps"
            )


class TestTutorialContent:
    """Tests for tutorial content quality."""

    def test_getting_started_has_doctor_command(self):
        """Test Getting Started includes ait doctor."""
        tutorial = create_getting_started_tutorial()
        commands = [s.command for s in tutorial.steps if s.command]
        assert "ait doctor" in commands

    def test_getting_started_has_detect_command(self):
        """Test Getting Started includes ait detect."""
        tutorial = create_getting_started_tutorial()
        commands = [s.command for s in tutorial.steps if s.command]
        assert "ait detect" in commands

    def test_intermediate_has_claude_settings(self):
        """Test Intermediate includes Claude settings command."""
        tutorial = create_intermediate_tutorial()
        commands = [s.command for s in tutorial.steps if s.command]
        assert "ait claude settings" in commands

    def test_advanced_has_release_commands(self):
        """Test Advanced includes release commands."""
        tutorial = create_advanced_tutorial()
        commands = [s.command for s in tutorial.steps if s.command]
        release_cmds = [c for c in commands if c and "release" in c]
        assert len(release_cmds) >= 1

    def test_tutorials_have_gif_paths(self):
        """Test tutorials reference GIF paths."""
        getting_started = create_getting_started_tutorial()
        gif_steps = [s for s in getting_started.steps if s.gif_path]
        assert len(gif_steps) >= 3, "Getting Started should have 3+ GIF references"

        intermediate = create_intermediate_tutorial()
        gif_steps = [s for s in intermediate.steps if s.gif_path]
        assert len(gif_steps) >= 3, "Intermediate should have 3+ GIF references"

        advanced = create_advanced_tutorial()
        gif_steps = [s for s in advanced.steps if s.gif_path]
        assert len(gif_steps) >= 3, "Advanced should have 3+ GIF references"
