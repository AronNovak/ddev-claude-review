# DDEV AI Review

AI-powered pull request code reviews using pluggable AI CLI tools in your DDEV projects.

## What does this add-on do?

This DDEV add-on provides a `ddev review` command that uses AI tools to perform comprehensive code reviews on GitHub pull requests. It automatically checks out the PR branch, fetches the diff, and provides detailed feedback on code quality, security, performance, and best practices.

## Installation

```bash
ddev get AronNovak/ddev-claude-review
```

## Requirements

This add-on requires the following tools to be installed on your host system:

- [GitHub CLI (gh)](https://cli.github.com/) - for fetching PR information
- Python 3.6+ - for running the review script (standard on most systems)
- One of the supported AI CLI tools:
  - [Claude CLI](https://docs.anthropic.com/en/docs/claude-code) (default)
  - [OpenAI Codex CLI](https://platform.openai.com/docs/guides/codex)
  - [Google Gemini CLI](https://ai.google.dev/)

## Usage

```bash
# Review by PR number (display only) - uses default (Claude)
ddev review 123

# Review by PR URL (display only)
ddev review https://github.com/org/repo/pull/123

# Review and post comments to GitHub automatically
ddev review --post 123
ddev review -p 123

# Post inline comments only (skip summary comment)
ddev review --post --no-summary 123

# Use a different AI CLI tool
ddev review --cli codex 123
ddev review --cli gemini --post 123
```

### Configuring the Default AI CLI Tool

The default AI tool is Claude. You can change it using the `DDEV_REVIEW_CLI` environment variable:

```bash
# Set for current session
export DDEV_REVIEW_CLI=gemini
ddev review 123

# Set for single command
DDEV_REVIEW_CLI=codex ddev review 123

# Add to your shell profile (~/.bashrc, ~/.zshrc) for persistence
echo 'export DDEV_REVIEW_CLI=gemini' >> ~/.bashrc
```

**Supported CLI tools:**
- `claude` (default) - Claude CLI
- `codex` - OpenAI Codex CLI
- `gemini` - Google Gemini CLI

**Priority order:**
1. `--cli` flag (highest priority)
2. `DDEV_REVIEW_CLI` environment variable
3. Default: `claude`

The command will:
1. Check out the PR branch
2. Fetch PR metadata (title, author, description)
3. Instruct the AI CLI tool to fetch and review the PR diff using `gh pr diff`
   - For large diffs, the AI may use a temporary file to handle the content
4. The AI returns a structured JSON response with review findings
5. The script validates the JSON (retries up to 3 times if invalid)
6. If `--post` flag is used:
   - Parse the JSON and post inline comments to GitHub using the GitHub API
   - Post an overall summary comment (unless `--no-summary` is used)
   - Display confirmation
7. If `--post` is NOT used:
   - Display a nicely formatted review in the terminal
   - No comments are posted to GitHub

**Options:**
- `--post` / `-p`: Post review comments to GitHub
- `--no-summary`: Skip posting the summary comment (only post inline comments)
- `--cli TOOL`: Specify which AI CLI tool to use

## Review Focus Areas

The review covers:
- Code quality and best practices
- Potential bugs or issues
- Security concerns
- Performance implications
- Drupal coding standards compliance (default, can be customized)

## Customization

You can customize the review command by editing the file in `.ddev/commands/host/review` after installation. Modify the `REVIEW_PROMPT` variable to adjust the focus areas or add project-specific requirements.

## How It Works

This add-on uses a structured JSON approach for reliable, automated code reviews:

1. **Pluggable AI CLI**: Uses a CLI adapter pattern to support multiple AI tools (Claude, Codex, Gemini, etc.)
2. **Dynamic diff fetching**: Instructs the AI to fetch the PR diff dynamically using `gh pr diff` (handles large diffs via temp files)
3. **Structured JSON output**: The AI returns a strict JSON structure with review findings (retries if invalid)
4. **Separation of concerns**: The AI does the analysis, the Python script handles GitHub posting
5. **No approval prompts**: All GitHub API calls happen in the Python script, not in the AI session
6. **Validation & retry**: Automatically validates JSON and retries up to 3 times if malformed

### JSON Response Structure

```json
{
  "summary": "Overall assessment of the PR",
  "risk_level": "low|medium|high",
  "passed": true,
  "comments": [
    {
      "path": "path/to/file.php",
      "line": 123,
      "body": "Specific issue description"
    }
  ]
}
```

**Important Notes:**
- Empty `comments` array means no issues found (`passed: true`)
- Line numbers must be exact line numbers from the diff output
- Paths must exactly match what appears in the diff
- The Python script parses this JSON and posts to GitHub when `--post` is used
- When `--post` is NOT used, it formats the JSON nicely for terminal display
- The script automatically handles JSON wrapped in markdown code blocks (` ```json ... ``` `)

## Project Structure

The review command is organized into modular components:

```
commands/host/
├── review              # Main executable script (entry point)
└── review_lib/         # Library modules
    ├── __init__.py     # Package initialization
    └── adapters.py     # AI CLI adapter implementations
```

This modular structure makes it easy to:
- Add new AI CLI adapters without cluttering the main script
- Test adapters independently
- Maintain clean separation of concerns

## Adding Support for New AI CLI Tools

To add support for a new AI CLI tool, edit `.ddev/commands/host/review_lib/adapters.py`:

1. Create a new adapter class that inherits from `CLIAdapter`
2. Implement the `build_command()` method with the correct CLI syntax
3. Add the adapter to the `adapters` dictionary in `get_cli_adapter()`

Example in `review_lib/adapters.py`:
```python
class MyAIAdapter(CLIAdapter):
    """Adapter for MyAI CLI."""

    def __init__(self):
        super().__init__("myai")

    def build_command(self, prompt):
        return f'myai-cli --prompt {json.dumps(prompt)}'
```

Then add it to the adapters dictionary in the `get_cli_adapter()` function:
```python
adapters = {
    'claude': ClaudeAdapter,
    'codex': CodexAdapter,
    'gemini': GeminiAdapter,
    'myai': MyAIAdapter,  # Add your new adapter
}
```

The adapter will automatically be available via:
```bash
ddev review --cli myai 123
# Or set as default
export DDEV_REVIEW_CLI=myai
ddev review 123
```

## Author

**Aron Novak** ([AronNovak](https://github.com/AronNovak))

## License

This project is licensed under the Apache License 2.0.
