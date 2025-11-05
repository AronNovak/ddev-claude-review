"""AI CLI tool adapters for code review."""

import json
import os
import subprocess


class CLIAdapter:
    """Base class for AI CLI tool adapters."""

    def __init__(self, name):
        self.name = name

    def build_command(self, prompt):
        """Build the command to execute. Override in subclasses."""
        raise NotImplementedError

    def execute(self, prompt):
        """Execute the CLI command with the given prompt."""
        cmd = self.build_command(prompt)
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return result


class ClaudeAdapter(CLIAdapter):
    """Adapter for Claude CLI."""

    def __init__(self):
        super().__init__("claude")

    def build_command(self, prompt):
        return f'claude --print {json.dumps(prompt)}'


class CodexAdapter(CLIAdapter):
    """Adapter for OpenAI Codex CLI."""

    def __init__(self):
        super().__init__("codex")

    def build_command(self, prompt):
        return f'codex --input {json.dumps(prompt)}'


class GeminiAdapter(CLIAdapter):
    """Adapter for Google Gemini CLI."""

    def __init__(self):
        super().__init__("gemini")

    def build_command(self, prompt):
        return f'gemini chat {json.dumps(prompt)}'


def get_cli_adapter(cli_name=None):
    """Get the appropriate CLI adapter based on name or environment variable.

    The CLI tool can be specified via:
    1. cli_name parameter (highest priority)
    2. DDEV_REVIEW_CLI environment variable
    3. Default: 'claude'
    """
    if cli_name is None:
        cli_name = os.environ.get('DDEV_REVIEW_CLI', 'claude')

    adapters = {
        'claude': ClaudeAdapter,
        'claude-code': ClaudeAdapter,  # Alias for backward compatibility
        'codex': CodexAdapter,
        'gemini': GeminiAdapter,
    }

    adapter_class = adapters.get(cli_name.lower())
    if adapter_class is None:
        available = ', '.join(sorted(set(adapters.keys()) - {'claude-code'}))  # Hide alias from error message
        raise ValueError(f"Unknown CLI tool: {cli_name}. Available options: {available}")

    return adapter_class()
