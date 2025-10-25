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
- [jq](https://stedolan.github.io/jq/) - for JSON parsing

## Usage

```bash
# Review by PR number (display only)
ddev review 123

# Review by PR URL (display only)
ddev review https://github.com/org/repo/pull/123

# Review and post comments to GitHub automatically
ddev review --post 123
ddev review -p 123
```

The command will:
1. Check out the PR branch
2. Fetch PR metadata (title, author, description)
3. Instruct Claude to fetch the PR diff using `gh pr diff`
   - For large diffs, Claude will use a temporary file to handle the content
4. Send the review request to Claude
5. Display a comprehensive code review
6. If `--post` flag is used, Claude will automatically post review comments to GitHub using `gh pr review`

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

Unlike traditional approaches that pass the entire PR diff in the prompt (which can hit token limits), this add-on:
- Instructs Claude to fetch the PR diff dynamically using `gh pr diff`
- Handles large diffs by writing them to temporary files when needed
- Allows Claude to post review comments directly to GitHub using `gh pr review` (when `--post` flag is used)
- Gives you control over whether reviews are posted automatically or just displayed

## Author

**Aron Novak** ([AronNovak](https://github.com/AronNovak))

## License

This project is licensed under the Apache License 2.0.
