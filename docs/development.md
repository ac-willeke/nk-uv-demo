# Development Guide

This guide covers development workflow, tools, and practices for the nk-uv-demo project.

## Setup

Complete development setup:
```bash
task dev-setup    # Install dependencies, hooks, and run initial checks
```

For commands reference, see [Command Cheatsheet](../command-cheatsheet.md).

## Code Quality

### Tools
- **Ruff** - Python linting and formatting
- **mypy** - Static type checking
- **Deptry** - Dependency analysis

### Configuration
All tools are configured in `pyproject.toml`:
- **Line length:** 88 characters
- **Type checking:** Strict mode enabled
- **Docstring format:** reStructuredText (reST)

### Workflow
```bash
task format       # Format code
task check        # Run all quality checks
task lint-fix     # Auto-fix linting issues
```

### Standards
- **Naming:** snake_case for functions/variables, PascalCase for classes
- **Imports:** Sorted and organized automatically
- **Type hints:** Required for all functions
- **Docstrings:** Required for public functions and classes

## Testing

### Framework
- **pytest** with coverage reporting
- **Coverage target:** >80%
- **Test discovery:** Files matching `test_*.py` pattern

### Structure
```
tests/
├── conftest.py           # Shared fixtures
└── nk_uv_demo/
    └── test_main.py      # Tests for main module
```

### Best Practices
- One test class per module
- Clear test names describing behavior
- Use fixtures for reusable test data
- Parametrize tests for multiple inputs
- Mock external dependencies

### Running Tests
```bash
task test-html    # Tests with HTML coverage report
task test         # Run tests only
```

## Security

### Tools
- **Safety** - Dependency vulnerability scanning
- **CodeQL** - Semantic code analysis
- **Dependabot** - Automated dependency updates
- **Zizmor** - GitHub Actions workflow security

### Setup
Safety requires authentication:
```bash
uv run safety auth login --headless
```

### Best Practices
- Pin dependency versions with ranges
- Use environment variables for secrets
- Validate all user inputs
- Use secure file handling with pathlib
- Regular security updates

## Pre-commit Hooks

### Purpose
Automatically enforce quality standards before each commit.

### Hooks Enabled
- **File quality:** Remove trailing whitespace, ensure newlines
- **Syntax validation:** YAML and TOML files
- **Code quality:** Ruff formatting and linting
- **Type checking:** mypy validation
- **Security:** Zizmor workflow scanning

### Usage
Hooks run automatically on `git commit`. Manual execution:
```bash
task pre-commit          # Run all hooks
uv run pre-commit run    # Run on staged files only
```

### Bypass (Emergency Only)
```bash
git commit --no-verify -m "Emergency commit"
```

## Development Workflow

### Standard Process
1. **Create branch:** `git checkout -b feature/name`
2. **Make changes:** Follow code quality standards
3. **Test locally:** `task check` and `task test`
4. **Commit:** Pre-commit hooks run automatically
5. **Push:** `git push origin feature/name`
6. **Create PR:** CI checks run automatically

### Quality Gates
Code must pass:
- Ruff formatting and linting
- mypy type checking
- pytest test suite (>80% coverage)
- Security scans
- Dependency analysis

### Local CI Simulation
```bash
task ci-local    # Run complete CI pipeline locally
```

## IDE Setup

### VS Code (Recommended)
Project includes configuration for:
- **Extensions:** Python, Ruff, mypy integration
- **Settings:** Auto-format on save, real-time linting
- **Tasks:** Integrated task runner
- **Debugging:** Python debug configuration

### Python Environment
VS Code should automatically detect `.venv`. If not:
1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose `./.venv/bin/python`

## Versioning

### Automatic Versioning
Uses setuptools-scm with git tags:
- **Development:** `1.0.1.dev1+g123abc` (post-commit)
- **Release:** `1.0.0` (tagged)

### Creating Releases
```bash
git tag v1.0.0
git push --tags    # Triggers deployment
```

## Troubleshooting

### Common Issues

**Environment problems:**
```bash
rm -rf .venv
task dev-setup
```

**Pre-commit failures:**
```bash
task lint-fix     # Auto-fix issues
git add .
git commit -m "Fix quality issues"
```

**Test failures:**
```bash
task test-html    # View coverage report in htmlcov/
```

**Import errors:**
```bash
uv pip install -e .    # Reinstall package in dev mode
```

### Cache Issues
```bash
uv cache clean           # Clear uv cache
rm -rf .mypy_cache       # Clear mypy cache
rm -rf .pytest_cache     # Clear pytest cache
```

## Configuration Files

### Key Files
- **`pyproject.toml`** - Tool configuration, dependencies, project metadata
- **`.pre-commit-config.yaml`** - Pre-commit hook configuration
- **`.safety-project.ini`** - Safety scanner configuration
- **`.vscode/`** - VS Code workspace settings
- **`Taskfile.yml`** - Task runner configuration

### Tool Configuration Locations
- **Ruff:** `[tool.ruff]` in pyproject.toml
- **mypy:** `[tool.mypy]` in pyproject.toml
- **pytest:** `[tool.pytest.ini_options]` in pyproject.toml
- **Coverage:** `[tool.coverage]` in pyproject.toml

## Contributing Guidelines

### Code Style
- Follow PEP 8 with 88-character line limit
- Add type hints to all functions
- Write docstrings for public APIs
- Use descriptive variable names
- Keep functions focused and small

### Commit Messages
- Use clear, descriptive messages
- Start with verb in present tense
- Reference issues when applicable
- Keep first line under 72 characters

### Pull Requests
- Include description of changes
- Reference related issues
- Ensure all CI checks pass
- Request review from maintainers
- Update documentation if needed
