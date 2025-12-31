"""StatusLine segments for modular rendering.

Each segment class handles rendering a specific part of the statusLine:
- ProjectSegment: Project type icon and directory display
- GitSegment: Git branch, status, ahead/behind
- ModelSegment: Claude model name with color coding
- TimeSegment: Current time and session duration
- ThinkingSegment: Thinking mode indicator
- LinesSegment: Lines added/removed
- UsageSegment: Session and weekly usage tracking
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import time
import json

from aiterm.statusline.config import StatusLineConfig
from aiterm.statusline.themes import Theme, get_theme
from aiterm.statusline.usage import UsageTracker, get_usage_color


class ProjectSegment:
    """Renders project type icon and directory."""

    # Project type detection patterns
    PROJECT_TYPES = {
        'production': {'patterns': ['*/production/*', '*/prod/*'], 'icon': '🚨'},
        'ai-session': {'patterns': ['*/claude-sessions/*', '*/gemini-sessions/*'], 'icon': '🤖'},
        'r-package': {'check': lambda p: (p / 'DESCRIPTION').exists() and 'Package:' in (p / 'DESCRIPTION').read_text(), 'icon': '📦'},
        'python': {'check': lambda p: (p / 'pyproject.toml').exists() or (p / 'setup.py').exists(), 'icon': '🐍'},
        'node': {'check': lambda p: (p / 'package.json').exists(), 'icon': '📦'},
        'quarto': {'check': lambda p: (p / '_quarto.yml').exists() or (p / '_quarto.yaml').exists(), 'icon': '📊'},
        'mcp': {'patterns': ['*/mcp-server/*', '*mcp*'], 'icon': '🔌'},
        'emacs': {'check': lambda p: any((p / f).exists() for f in ['init.el', 'Cask', '.dir-locals.el', 'early-init.el']), 'icon': '⚡'},
        'dev-tools': {'check': lambda p: (p / '.git').exists() and ((p / 'commands').exists() or (p / 'scripts').exists()), 'icon': '🔧'},
    }

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self, cwd: str, project_dir: str) -> str:
        """Render project segment.

        Args:
            cwd: Current working directory
            project_dir: Project root directory

        Returns:
            Formatted project segment with colors
        """
        # Get project info
        project_icon = self._get_project_icon(project_dir)
        project_type = self._get_project_type(project_dir)
        dir_display = self._format_directory(cwd, project_dir)
        r_version = self._get_r_version(project_dir)

        # Get project-specific context (Phase 4)
        python_env = self._get_python_env(project_dir)
        node_version = self._get_node_version(project_dir)
        r_health = self._get_r_package_health(project_dir)
        dep_warnings = self._get_dependency_warnings(project_dir, project_type)

        # Build content
        content = f"{project_icon} {dir_display}"

        if r_version and self.config.get('display.show_r_version', True):
            content += f" \033[38;5;245m{r_version}\033[38;5;250m"

        # Add project-specific context
        if python_env:
            content += f" \033[38;5;245m({python_env})\033[38;5;250m"

        if node_version:
            content += f" \033[38;5;245m({node_version})\033[38;5;250m"

        if r_health:
            content += f" {r_health}"

        if dep_warnings:
            content += f" \033[38;5;208m{dep_warnings}\033[38;5;250m"

        # Get colors from theme
        dir_bg = self.theme.dir_bg
        dir_fg = self.theme.dir_fg

        # Build segment with powerline edges
        segment = f"\033[{dir_bg};{dir_fg}m ░▒▓ {content} "

        return segment

    def _get_project_icon(self, project_dir: str) -> str:
        """Get icon for project type.

        Args:
            project_dir: Project directory path

        Returns:
            Unicode icon character
        """
        path = Path(project_dir)

        # Check path patterns first (faster)
        for project_type, config in self.PROJECT_TYPES.items():
            if 'patterns' in config:
                for pattern in config['patterns']:
                    # Simple pattern matching
                    pattern_parts = pattern.split('/')
                    path_str = str(path)

                    if pattern.startswith('*') and pattern.endswith('*'):
                        # Contains pattern
                        middle = pattern.strip('*')
                        if middle in path_str:
                            return config['icon']
                    elif pattern.endswith('/*'):
                        # Path ends with pattern
                        prefix = pattern[:-2]
                        if path_str.endswith(prefix):
                            return config['icon']

        # Check file-based detection
        for project_type, config in self.PROJECT_TYPES.items():
            if 'check' in config:
                try:
                    if config['check'](path):
                        return config['icon']
                except Exception:
                    # Ignore errors in check functions
                    pass

        return '📁'  # Default icon

    def _get_project_type(self, project_dir: str) -> str:
        """Get project type string.

        Args:
            project_dir: Project directory path

        Returns:
            Project type string (python/node/r-package/default)
        """
        path = Path(project_dir)

        # Check for R package
        if (path / 'DESCRIPTION').exists():
            try:
                content = (path / 'DESCRIPTION').read_text()
                if 'Package:' in content:
                    return 'r-package'
            except Exception:
                pass

        # Check for Python project
        if (path / 'pyproject.toml').exists() or (path / 'setup.py').exists():
            return 'python'

        # Check for Node.js project
        if (path / 'package.json').exists():
            return 'node'

        return 'default'

    def _format_directory(self, cwd: str, project_dir: str) -> str:
        """Format directory for display.

        Args:
            cwd: Current working directory
            project_dir: Project root directory

        Returns:
            Formatted directory string
        """
        # Replace home with ~
        home = str(Path.home())
        cwd_display = cwd.replace(home, '~')
        project_dir_display = project_dir.replace(home, '~')

        # Get directory mode from config
        dir_mode = self.config.get('display.directory_mode', 'smart')

        if dir_mode == 'basename':
            return Path(cwd).name

        if dir_mode == 'full':
            return cwd_display

        # Smart mode (default): context-aware
        if cwd == project_dir or cwd_display == project_dir_display:
            return Path(project_dir).name

        if cwd.startswith(project_dir + '/'):
            # Show relative to project
            rel = cwd[len(project_dir)+1:]
            return f"{Path(project_dir).name}/{rel}"

        # Shorten long paths
        parts = cwd_display.split('/')
        if len(parts) > 3:
            return f"{parts[0]}/…/{parts[-2]}/{parts[-1]}"

        return cwd_display

    def _get_r_version(self, project_dir: str) -> Optional[str]:
        """Get R package version if applicable.

        Args:
            project_dir: Project directory

        Returns:
            Version string like "v1.2.3" or None
        """
        desc_file = Path(project_dir) / 'DESCRIPTION'

        if not desc_file.exists():
            return None

        try:
            content = desc_file.read_text()
            for line in content.split('\n'):
                if line.startswith('Version:'):
                    version = line.replace('Version:', '').strip()
                    return f"v{version}"
        except Exception:
            pass

        return None

    def _get_python_env(self, project_dir: str) -> Optional[str]:
        """Detect Python environment (venv/conda/pyenv).

        Args:
            project_dir: Project directory

        Returns:
            Environment string like "venv: py3.11" or "conda: stats-env" or None
        """
        if not self.config.get('project.detect_python_env', False):
            return None

        project_path = Path(project_dir)

        # Check for virtual environment
        venv_paths = [
            project_path / 'venv',
            project_path / '.venv',
            project_path / 'env',
        ]

        for venv_path in venv_paths:
            if venv_path.exists():
                # Try to get Python version
                try:
                    python_bin = venv_path / 'bin' / 'python'
                    if python_bin.exists():
                        result = subprocess.run(
                            [str(python_bin), '--version'],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        if result.returncode == 0:
                            # Parse "Python 3.11.5" -> "py3.11"
                            version = result.stdout.strip().split()[1]
                            major_minor = '.'.join(version.split('.')[:2])
                            return f"venv: py{major_minor}"
                except Exception:
                    pass
                return "venv"

        # Check for conda environment
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env and conda_env != 'base':
            return f"conda: {conda_env}"

        # Check for pyenv
        pyenv_version_file = project_path / '.python-version'
        if pyenv_version_file.exists():
            try:
                version = pyenv_version_file.read_text().strip()
                return f"pyenv: {version}"
            except Exception:
                pass

        return None

    def _get_node_version(self, project_dir: str) -> Optional[str]:
        """Get Node.js version from .nvmrc or active version.

        Args:
            project_dir: Project directory

        Returns:
            Version string like "v20.11.0" or None
        """
        if not self.config.get('project.detect_node_version', False):
            return None

        project_path = Path(project_dir)

        # Check .nvmrc file
        nvmrc = project_path / '.nvmrc'
        if nvmrc.exists():
            try:
                version = nvmrc.read_text().strip()
                if not version.startswith('v'):
                    version = f"v{version}"
                return version
            except Exception:
                pass

        # Get current node version
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        return None

    def _get_r_package_health(self, project_dir: str) -> Optional[str]:
        """Check R package health (tests, check results).

        Args:
            project_dir: Project directory

        Returns:
            Health indicator like "✓" (all good), "⚠" (warnings), or None
        """
        if not self.config.get('project.detect_r_package_health', False):
            return None

        project_path = Path(project_dir)

        # Only check if this is an R package
        desc_file = project_path / 'DESCRIPTION'
        if not desc_file.exists():
            return None

        # Lightweight checks (not full R CMD check)
        warnings = []

        # Check if tests exist
        tests_dir = project_path / 'tests'
        if not tests_dir.exists():
            warnings.append("no tests")

        # Check for R CMD check results
        check_results = list(project_path.glob('*.Rcheck'))
        if check_results:
            # Check most recent
            latest_check = max(check_results, key=lambda p: p.stat().st_mtime)
            check_log = latest_check / '00check.log'
            if check_log.exists():
                try:
                    content = check_log.read_text()
                    if 'ERROR' in content:
                        return "❌"
                    elif 'WARNING' in content:
                        return "⚠"
                    elif 'NOTE' in content:
                        return "⚠"
                except Exception:
                    pass

        # If we have warnings but no check results, show warning
        if warnings:
            return "⚠"

        # All good
        return "✓"

    def _get_dependency_warnings(self, project_dir: str, project_type: str) -> Optional[str]:
        """Check for outdated dependencies.

        Args:
            project_dir: Project directory
            project_type: Type of project (python/node/r-package)

        Returns:
            Warning string like "⚠ 5 outdated" or None
        """
        if not self.config.get('project.show_dependency_warnings', False):
            return None

        project_path = Path(project_dir)

        # Python projects
        if project_type == 'python':
            try:
                result = subprocess.run(
                    ['pip', 'list', '--outdated', '--format=json'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=project_dir
                )
                if result.returncode == 0:
                    import json
                    outdated = json.loads(result.stdout)
                    if len(outdated) > 0:
                        return f"⚠ {len(outdated)} outdated"
            except Exception:
                pass

        # Node.js projects
        elif project_type == 'node':
            try:
                result = subprocess.run(
                    ['npm', 'outdated', '--json'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=project_dir
                )
                # npm outdated returns exit code 1 when there are outdated packages
                if result.stdout:
                    import json
                    try:
                        outdated = json.loads(result.stdout)
                        count = len(outdated)
                        if count > 0:
                            return f"⚠ {count} outdated"
                    except json.JSONDecodeError:
                        pass
            except Exception:
                pass

        # R packages
        elif project_type == 'r-package':
            # R dependency checking is expensive, skip for now
            # Could cache results or run in background
            pass

        return None


class GitSegment:
    """Renders git branch and status."""

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self, cwd: str) -> str:
        """Render git segment.

        Args:
            cwd: Current working directory

        Returns:
            Formatted git segment or empty string if not in git repo
        """
        if not self.config.get('display.show_git', True):
            return ""

        git_info = self._get_git_info(cwd)

        if not git_info:
            return ""

        branch, has_changes, ahead, behind, untracked = git_info

        # Determine background color from theme
        vcs_bg = self.theme.vcs_clean_bg if not has_changes and untracked == 0 else self.theme.vcs_modified_bg
        vcs_fg = self.theme.vcs_fg

        # Build git string
        git_str = f" {branch}"

        if has_changes:
            git_str += "*"

        if self.config.get('git.show_ahead_behind', True):
            if behind > 0:
                git_str += f" ⇣{behind}"
            if ahead > 0:
                git_str += f" ⇡{ahead}"

        if self.config.get('git.show_untracked_count', True) and untracked > 0:
            git_str += f" ?{untracked}"

        # Get enhanced git info
        if self.config.get('git.show_stash_count', False):
            stash_count = self._get_stash_count(cwd)
            if stash_count > 0:
                git_str += f" 📦{stash_count}"

        if self.config.get('git.show_remote_status', False):
            remote = self._get_remote_tracking(cwd)
            if remote:
                git_str += f" 🔗{remote}"

        # Build segment with powerline separator
        sep_left = ""
        segment = f"\033[38;5;54;{vcs_bg}m{sep_left}\033[{vcs_bg};{vcs_fg}m{git_str} \033[0m\033[38;5;60m▓▒░\033[0m"

        return segment

    def _get_git_info(self, cwd: str) -> Optional[Tuple[str, bool, int, int, int]]:
        """Get git repository information.

        Args:
            cwd: Current working directory

        Returns:
            Tuple of (branch, has_changes, ahead, behind, untracked_count) or None
        """
        try:
            # Check if in git repo
            subprocess.run(
                ['git', '-C', cwd, 'rev-parse', '--git-dir'],
                capture_output=True,
                check=True
            )

            # Get branch name
            result = subprocess.run(
                ['git', '-C', cwd, 'branch', '--show-current'],
                capture_output=True,
                text=True
            )
            branch = result.stdout.strip()

            if not branch:
                # Try tag or detached
                result = subprocess.run(
                    ['git', '-C', cwd, 'describe', '--tags', '--exact-match'],
                    capture_output=True,
                    text=True
                )
                branch = result.stdout.strip() or "detached"

            # Truncate long branch names
            max_len = self.config.get('git.truncate_branch_length', 32)
            if len(branch) > max_len:
                branch = f"{branch[:12]}…{branch[-12:]}"

            # Check for changes
            has_changes = False
            result = subprocess.run(
                ['git', '-C', cwd, 'diff', '--quiet'],
                capture_output=True
            )
            if result.returncode != 0:
                has_changes = True

            result = subprocess.run(
                ['git', '-C', cwd, 'diff', '--cached', '--quiet'],
                capture_output=True
            )
            if result.returncode != 0:
                has_changes = True

            # Get untracked count
            result = subprocess.run(
                ['git', '-C', cwd, 'ls-files', '--others', '--exclude-standard'],
                capture_output=True,
                text=True
            )
            untracked = len([l for l in result.stdout.strip().split('\n') if l])

            # Get ahead/behind
            ahead = 0
            behind = 0

            result = subprocess.run(
                ['git', '-C', cwd, 'rev-list', '--count', '@{u}..HEAD'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                ahead = int(result.stdout.strip() or 0)

            result = subprocess.run(
                ['git', '-C', cwd, 'rev-list', '--count', 'HEAD..@{u}'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                behind = int(result.stdout.strip() or 0)

            return (branch, has_changes, ahead, behind, untracked)

        except Exception:
            return None

    def _get_stash_count(self, cwd: str) -> int:
        """Get number of stashed changes.

        Args:
            cwd: Current working directory

        Returns:
            Number of stash entries
        """
        try:
            result = subprocess.run(
                ['git', '-C', cwd, 'stash', 'list'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = [l for l in result.stdout.strip().split('\n') if l]
                return len(lines)
        except Exception:
            pass
        return 0

    def _get_remote_tracking(self, cwd: str) -> Optional[str]:
        """Get remote tracking branch.

        Args:
            cwd: Current working directory

        Returns:
            Remote tracking branch name (e.g., "origin/main") or None
        """
        try:
            # Get upstream branch
            result = subprocess.run(
                ['git', '-C', cwd, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                remote = result.stdout.strip()
                # Shorten if too long
                if len(remote) > 20:
                    parts = remote.split('/')
                    if len(parts) >= 2:
                        return f"{parts[0]}/…"
                return remote
        except Exception:
            pass
        return None

    def _get_recent_activity(self, cwd: str) -> bool:
        """Check if there are commits in the last 24 hours.

        Args:
            cwd: Current working directory

        Returns:
            True if there are recent commits, False otherwise
        """
        try:
            # Get commits from last 24 hours
            result = subprocess.run(
                ['git', '-C', cwd, 'log', '--since', '24 hours ago', '--oneline'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = [l for l in result.stdout.strip().split('\n') if l]
                return len(lines) > 0
        except Exception:
            pass
        return False


class ModelSegment:
    """Renders Claude model name."""

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self, model_name: str) -> str:
        """Render model segment.

        Args:
            model_name: Model display name

        Returns:
            Formatted model name with color
        """
        # Shorten model name
        model_short = model_name.replace('Claude ', '')

        # Get color from theme based on model type
        if 'Sonnet' in model_name:
            color = self.theme.model_sonnet
        elif 'Opus' in model_name:
            color = self.theme.model_opus
        elif 'Haiku' in model_name:
            color = self.theme.model_haiku
        else:
            color = self.theme.model_opus  # Default

        return f"\033[{color}m{model_short}\033[0m"


class TimeSegment:
    """Renders current time and session duration."""

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self, session_id: str, transcript_path: Optional[str] = None) -> str:
        """Render time segment.

        Args:
            session_id: Session ID for duration tracking
            transcript_path: Optional path to session transcript for activity tracking

        Returns:
            Formatted time string
        """
        output = ""

        # Current time
        if self.config.get('display.show_current_time', True):
            current_time = time.strftime("%H:%M")
            output += f" \033[{self.theme.separator_fg}m│\033[0m \033[{self.theme.time_fg}m{current_time}\033[0m"

            # Add time-of-day indicator
            time_of_day = self._get_time_of_day_indicator()
            if time_of_day:
                output += f" {time_of_day}"

        # Session duration
        if self.config.get('display.show_session_duration', True):
            duration = self._get_session_duration(session_id)
            output += f" \033[{self.theme.separator_fg}m│\033[0m \033[{self.theme.duration_fg}m⏱ {duration}\033[0m"

            # Add productivity indicator
            productivity = self._get_productivity_indicator(transcript_path)
            if productivity:
                output += f" {productivity}"

        return output

    def _get_session_duration(self, session_id: str) -> str:
        """Get formatted session duration.

        Args:
            session_id: Session ID

        Returns:
            Formatted duration like "5m", "2h15m"
        """
        session_file = Path(f"/tmp/claude-session-{session_id or 'default'}")
        now = int(time.time())

        if not session_file.exists():
            session_file.write_text(str(now))
            return "0m"

        try:
            start = int(session_file.read_text().strip())
            elapsed = now - start

            if elapsed < 60:
                return "<1m"
            elif elapsed < 3600:
                return f"{elapsed // 60}m"
            else:
                hours = elapsed // 3600
                mins = (elapsed % 3600) // 60
                return f"{hours}h{mins}m"

        except Exception:
            return "0m"

    def _get_productivity_indicator(self, transcript_path: Optional[str]) -> Optional[str]:
        """Get productivity indicator based on recent activity.

        Args:
            transcript_path: Path to session transcript

        Returns:
            Activity indicator emoji (🟢/🟡/🔴) or None
        """
        if not self.config.get('time.show_productivity_indicator', False):
            return None

        if not transcript_path or not Path(transcript_path).exists():
            return None

        try:
            # Read transcript to get last message timestamp
            with open(transcript_path, 'r') as f:
                content = f.read()

            # Parse JSON transcript
            import json
            data = json.loads(content)

            # Get last message timestamp
            messages = data.get('messages', [])
            if not messages:
                return None

            last_msg = messages[-1]
            last_time = last_msg.get('timestamp', 0)

            # Return None if timestamp is missing or invalid
            if not last_time:
                return None

            # Calculate idle time
            now = int(time.time())
            idle_seconds = now - last_time

            # Return indicator based on idle time
            if idle_seconds < 300:  # < 5 min
                return "🟢"  # Active
            elif idle_seconds < 900:  # 5-15 min
                return "🟡"  # Idle
            else:  # > 15 min
                return "🔴"  # Long idle

        except Exception:
            return None

    def _get_time_of_day_indicator(self) -> Optional[str]:
        """Get time-of-day context icon.

        Returns:
            Time-of-day emoji (🌅/☀️/🌙/🌃) or None
        """
        if not self.config.get('time.show_time_of_day', False):
            return None

        hour = int(time.strftime("%H"))

        if 6 <= hour < 12:
            return "🌅"  # Morning
        elif 12 <= hour < 18:
            return "☀️"  # Afternoon
        elif 18 <= hour < 24:
            return "🌙"  # Evening
        else:
            return "🌃"  # Night


class ThinkingSegment:
    """Renders thinking mode indicator."""

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self) -> str:
        """Render thinking indicator.

        Returns:
            Formatted indicator or empty string
        """
        if not self.config.get('display.show_thinking_indicator', True):
            return ""

        # Read Claude Code settings
        settings_file = Path.home() / '.claude' / 'settings.json'

        if not settings_file.exists():
            return ""

        try:
            with open(settings_file) as f:
                settings = json.load(f)

            thinking_enabled = settings.get('alwaysThinkingEnabled', False)

            if thinking_enabled:
                return f" \033[{self.theme.separator_fg}m│\033[0m \033[{self.theme.thinking_fg}m🧠\033[0m"

        except Exception:
            pass

        return ""


class LinesSegment:
    """Renders lines added/removed."""

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))

    def render(self, lines_added: int, lines_removed: int) -> str:
        """Render lines changed segment.

        Args:
            lines_added: Total lines added
            lines_removed: Total lines removed

        Returns:
            Formatted lines string or empty
        """
        if not self.config.get('display.show_lines_changed', True):
            return ""

        if lines_added == 0 and lines_removed == 0:
            return ""

        # Format display
        output = f"\033[{self.theme.lines_added_fg}m+{lines_added}\033[0m"

        if lines_removed > 0:
            output += f"\033[{self.theme.lines_removed_fg}m/-{lines_removed}\033[0m"

        return output


class UsageSegment:
    """Renders usage tracking (session and weekly).

    Note: Currently returns empty string as Claude Code usage API is not yet available.
    This segment is ready to display usage data once the API is implemented.
    """

    def __init__(self, config: StatusLineConfig, theme: Optional[Theme] = None):
        """Initialize segment.

        Args:
            config: StatusLineConfig instance
            theme: Theme object (loads from config if None)
        """
        self.config = config
        self.theme = theme or get_theme(config.get('theme.name', 'purple-charcoal'))
        self.tracker = UsageTracker()

    def render(self) -> str:
        """Render usage tracking segment.

        Returns:
            Formatted usage string or empty if disabled/unavailable
        """
        # Check if usage display is enabled
        show_session = self.config.get('display.show_session_usage', True)
        show_weekly = self.config.get('display.show_weekly_usage', True)

        if not show_session and not show_weekly:
            return ""

        # Get usage data
        session = self.tracker.get_session_usage() if show_session else None
        weekly = self.tracker.get_weekly_usage() if show_weekly else None

        if not session and not weekly:
            # No data available yet
            return ""

        # Format output
        parts = []

        if session:
            color = get_usage_color(session, self.config.get('usage.warning_threshold', 80))
            parts.append(f"S:{session.current}/{session.limit}({session.time_until_reset()})")

        if weekly:
            color = get_usage_color(weekly, self.config.get('usage.warning_threshold', 80))
            parts.append(f"W:{weekly.current}/{weekly.limit}({weekly.time_until_reset()})")

        if not parts:
            return ""

        # Combine and add separator
        usage_str = " ".join(parts)
        return f" \033[{self.theme.separator_fg}m│\033[0m \033[38;5;2m📊{usage_str}\033[0m"
