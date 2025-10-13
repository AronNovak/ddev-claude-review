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
# Review by PR number
ddev review 123

# Review by PR URL
ddev review https://github.com/org/repo/pull/123
```

The command will:
1. Check out the PR branch
2. Fetch PR metadata (title, author, description)
3. Generate a diff of the changes
4. Send the code to Claude for review
5. Display a comprehensive code review

## Review Focus Areas

The review covers:
- Code quality and best practices
- Potential bugs or issues
- Security concerns
- Performance implications
- Drupal coding standards compliance (default, can be customized)

## Customization

You can customize the review command by editing the file in `.ddev/commands/host/review` after installation. Modify the `REVIEW_PROMPT` variable to adjust the focus areas or add project-specific requirements.

## Author

**Aron Novak** ([AronNovak](https://github.com/AronNovak))

## License

This project is licensed under the Apache License 2.0.
