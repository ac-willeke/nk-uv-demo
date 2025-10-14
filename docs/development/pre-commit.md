# Pre-commit Hooks

This document explains the pre-commit hooks configuration and workflow used in nk-uv-demo to ensure code quality and security before commits.

## Overview

[Pre-commit](https://pre-commit.com/) hooks automatically run quality checks before each git commit, ensuring that only clean, secure code enters the repository.

**Configuration**: `.pre-commit-config.yaml`

## Benefits

- **Catch Issues Early**: Fix problems before they reach the repository
- **Consistent Quality**: Enforce standards across all contributors
- **Automated Workflow**: No need to remember to run checks manually
- **Fast Feedback**: Immediate feedback on code quality
- **Prevention**: Stop problematic code from entering git history

## Pre-commit Hooks Configuration

### Current Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace     # Remove trailing whitespace
      - id: end-of-file-fixer      # Ensure files end with newline
      - id: check-yaml             # Validate YAML syntax
      - id: check-added-large-files # Prevent large files
      - id: check-toml             # Validate TOML syntax

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff                   # Ruff linting
        args: [--fix]              # Auto-fix issues where possible
      - id: ruff-format            # Ruff code formatting

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy                   # Type checking
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: zizmor                 # GitHub Actions security scan
        name: Zizmor workflow security scan
        entry: uv run zizmor
        language: system
        files: ^\.github/workflows/.*\.ya?ml$
        pass_filenames: false
        args: ['.github/workflows/']
```

### Hook Categories

| Category | Hook | Purpose | Auto-fix |
|----------|------|---------|----------|
| **File Quality** | trailing-whitespace | Remove trailing spaces | ✅ |
| **File Quality** | end-of-file-fixer | Ensure newline at EOF | ✅ |
| **Syntax** | check-yaml | Validate YAML files | ❌ |
| **Syntax** | check-toml | Validate TOML files | ❌ |
| **Size** | check-added-large-files | Prevent large file commits | ❌ |
| **Code Quality** | ruff (lint) | Python linting | ✅ (partial) |
| **Code Quality** | ruff-format | Code formatting | ✅ |
| **Type Safety** | mypy | Type checking | ❌ |
| **Security** | zizmor | Workflow security | ❌ |

## Installation and Setup

### Automatic Setup (Recommended)

```bash
# Complete setup with Taskfile
task dev-setup
# This installs dependencies AND pre-commit hooks

# Or install just pre-commit hooks
task pre-commit-install
```

### Manual Setup

```bash
# Install pre-commit in the virtual environment
uv add --group dev pre-commit

# Install the git hooks
uv run pre-commit install

# Verify installation
uv run pre-commit --version
```

## Using Pre-commit Hooks

### Normal Git Workflow

Pre-commit hooks run automatically on `git commit`:

```bash
# Make changes to code
echo "print('hello')" > src/nk_uv_demo/new_file.py

# Stage changes
git add .

# Commit (hooks run automatically)
git commit -m "Add new feature"
```

### Hook Execution Results

#### ✅ Success (all hooks pass)
```bash
$ git commit -m "Clean code"
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check Yaml...........................................(no files to check)Skipped
Check for added large files..............................................Passed
Check Toml...........................................(no files to check)Skipped
ruff.....................................................................Passed
ruff-format..............................................................Passed
mypy.....................................................................Passed
[main abc1234] Clean code
 1 file changed, 5 insertions(+)
```

#### ❌ Failure (hooks find issues)
```bash
$ git commit -m "Code with issues"
Trim Trailing Whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fix End of Files.........................................................Passed
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1

src/nk_uv_demo/main.py:10:1: F401 [*] `os` imported but unused
Found 1 error.

ruff-format..............................................................Passed
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

src/nk_uv_demo/main.py:15: error: Function is missing a return type annotation
```

### Manual Hook Execution

```bash
# Run hooks on all files
task pre-commit
# or: uv run pre-commit run --all-files

# Run hooks on staged files only
uv run pre-commit run

# Run specific hook
uv run pre-commit run ruff
uv run pre-commit run mypy

# Run hooks on specific files
uv run pre-commit run --files src/nk_uv_demo/main.py
```

## Hook Behavior and Fixes

### Auto-fixing Hooks

Some hooks automatically fix issues:

```bash
# Example: ruff auto-fixes import sorting
$ git commit -m "Test commit"
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1
- files were modified by this hook

# Files have been automatically fixed, re-add them
$ git add .
$ git commit -m "Test commit"  # Now should pass
```

### Type Checking (mypy)

mypy doesn't auto-fix but provides clear error messages:

```bash
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

src/nk_uv_demo/main.py:10: error: Function is missing a return type annotation
src/nk_uv_demo/main.py:15: error: Incompatible return value type (got "str", expected "int")

# Fix by adding type annotations
def my_function(x: int) -> str:  # Add return type annotation
    return str(x)  # Fix return type
```

### Security Scanning (zizmor)

Runs only when GitHub workflow files are modified:

```bash
# Only runs when .github/workflows/*.yml files change
$ git add .github/workflows/new-workflow.yml
$ git commit -m "Add workflow"
Zizmor workflow security scan...........................................Failed
- hook id: zizmor
- exit code: 1

.github/workflows/new-workflow.yml:15:12: excessive permissions
```

## Skipping Hooks (Use Sparingly)

### Skip All Hooks

```bash
# Emergency commits only (not recommended)
git commit --no-verify -m "Emergency hotfix"
```

### Skip Specific Hooks

```bash
# Skip only specific hooks
SKIP=mypy git commit -m "Skip type checking"
SKIP=ruff,mypy git commit -m "Skip multiple hooks"
```

### When to Skip Hooks

- **Emergency hotfixes**: Critical production issues
- **Work in progress**: Experimental branches (use draft PRs instead)
- **External code**: Third-party code that can't be modified
- **Large refactors**: Split into smaller commits instead

## Common Workflows

### Fix All Issues at Once

```bash
# Run all checks and see what needs fixing
task pre-commit

# Fix auto-fixable issues
task format
task lint-fix

# Address remaining issues manually (mypy, security)
# Then commit normally
git add .
git commit -m "Fix code quality issues"
```

### Incremental Fixes

```bash
# Fix formatting first
uv run ruff format .
git add .
git commit -m "Fix code formatting"

# Fix linting issues
uv run ruff check --fix .
git add .
git commit -m "Fix linting issues"

# Fix type annotations
# (manual work)
git add .
git commit -m "Add type annotations"
```

### Large File Commits

```bash
# Add large files to .gitattributes or split them
echo "*.pdf filter=lfs diff=lfs merge=lfs -text" >> .gitattributes

# Or exclude from pre-commit
# (modify .pre-commit-config.yaml to exclude certain file patterns)
```

## Troubleshooting

### Common Issues

#### Hook Installation Problems

```bash
# Re-install hooks
uv run pre-commit uninstall
uv run pre-commit install

# Update hooks to latest versions
uv run pre-commit autoupdate
```

#### Hook Execution Failures

```bash
# Clear pre-commit cache
uv run pre-commit clean

# Re-run with verbose output
uv run pre-commit run --all-files --verbose
```

#### Mypy Import Errors

```bash
# Install missing type stubs
uv add --group dev types-requests  # For requests library types

# Or ignore specific errors temporarily
# mypy: ignore-errors
```

#### Performance Issues

```bash
# Run hooks in parallel (if supported)
uv run pre-commit run -j auto

# Skip slow hooks for quick commits
SKIP=mypy git commit -m "Quick fix"
```

### Configuration Debugging

```bash
# Validate pre-commit configuration
uv run pre-commit validate-config

# Show hook information
uv run pre-commit hook-impl --config .pre-commit-config.yaml

# Test specific hook
uv run pre-commit try-repo . ruff --files src/nk_uv_demo/main.py
```

## Customization

### Adding New Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/]

  - repo: local
    hooks:
      - id: custom-check
        name: Custom validation
        entry: python scripts/validate.py
        language: system
        pass_filenames: false
```

### Excluding Files

```yaml
# Exclude files from hooks
- id: mypy
  exclude: ^tests/|^scripts/

# Include only specific files
- id: ruff
  files: ^src/.*\.py$
```

### Hook Arguments

```yaml
# Customize hook behavior
- id: ruff
  args: [--fix, --show-fixes]

- id: mypy
  args: [--strict, --ignore-missing-imports]
```

## Integration with IDE

### VS Code Integration

Pre-commit hooks work alongside VS Code extensions:

1. **Real-time**: VS Code extensions provide immediate feedback
2. **Pre-commit**: Hooks provide final validation before commit
3. **Consistent**: Same tools, same rules in both environments

### Manual Trigger in VS Code

Add to VS Code tasks (`.vscode/tasks.json`):

```json
{
  "label": "Run pre-commit",
  "type": "shell",
  "command": "uv run pre-commit run --all-files",
  "group": "test",
  "presentation": {
    "echo": true,
    "reveal": "always"
  }
}
```

## Performance Optimization

### Faster Hook Execution

```bash
# Run hooks in parallel
uv run pre-commit run --all-files -j auto

# Cache dependencies for faster subsequent runs
# (pre-commit handles this automatically)

# Use faster tools where possible (Ruff vs multiple tools)
```

### Selective Hook Execution

```yaml
# Only run on relevant file types
- id: mypy
  files: \.py$
  exclude: ^tests/

- id: ruff-format
  types: [python]
```

## CI/CD Integration

Pre-commit hooks also run in CI to catch any bypassed checks:

```yaml
# .github/workflows/ci-quality.yml
- name: Run pre-commit
  uses: pre-commit/action@v3.0.1
```

This ensures:
- **Consistency**: Same checks locally and in CI
- **Enforcement**: Can't bypass quality checks
- **Documentation**: Clear failure reasons in CI logs

---

**Next Steps**: Learn about [CI/CD Workflows](../ci-cd/workflows.md) to see how these quality checks integrate with continuous integration.
