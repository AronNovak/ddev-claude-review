# DDEV Claude Review

AI-powered pull request code reviews using Claude CLI in your DDEV projects.

## What does this add-on do?

This DDEV add-on provides a `ddev review` command that uses Claude AI to perform comprehensive code reviews on GitHub pull requests. It automatically checks out the PR branch, fetches the diff, and provides detailed feedback on code quality, security, performance, and best practices.

## Installation

```bash
ddev get AronNovak/ddev-claude-review
```

## Requirements

This add-on requires the following tools to be installed on your host system:

- [GitHub CLI (gh)](https://cli.github.com/) - for fetching PR information
- [Claude CLI](https://docs.anthropic.com/en/docs/claude-cli) - for AI code reviews
- Python 3.6+ - for running the review script (standard on most systems)

## Usage

```bash
# Review by PR number (display only)
ddev review 123

# Review by PR URL (display only)
ddev review https://github.com/org/repo/pull/123

# Review and post comments to GitHub automatically
ddev review --post 123
ddev review -p 123

# Post inline comments only (skip summary comment)
ddev review --post --no-summary 123
```

The command will:
1. Check out the PR branch
2. Fetch PR metadata (title, author, description)
3. Instruct Claude to fetch and review the PR diff using `gh pr diff`
   - For large diffs, Claude will use a temporary file to handle the content
4. Claude returns a structured JSON response with review findings
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

1. **Dynamic diff fetching**: Instructs Claude to fetch the PR diff dynamically using `gh pr diff` (handles large diffs via temp files)
2. **Structured JSON output**: Claude returns a strict JSON structure with review findings (retries if invalid)
3. **Separation of concerns**: Claude does the analysis, the bash script handles GitHub posting
4. **No approval prompts**: All GitHub API calls happen in the bash script, not in the Claude session
5. **Validation & retry**: Automatically validates JSON and retries up to 3 times if malformed

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
- The bash script parses this JSON and posts to GitHub when `--post` is used
- When `--post` is NOT used, it formats the JSON nicely for terminal display
- The script automatically handles JSON wrapped in markdown code blocks (` ```json ... ``` `)

## Author

**Aron Novak** ([AronNovak](https://github.com/AronNovak))

## License

This project is licensed under the Apache License 2.0.
