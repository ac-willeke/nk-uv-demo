# Code Quality

This document explains the code quality tools and standards used in nk-uv-demo to ensure consistent, maintainable, and error-free Python code.

## Overview

Code quality is enforced through multiple layers:

1. **Local Development**: Real-time feedback in VS Code
2. **Pre-commit Hooks**: Checks before each commit
3. **CI/CD Pipeline**: Automated validation on push/PR
4. **IDE Integration**: Continuous feedback while coding

## Tools and Configuration

### Ruff - Fast Python Linter and Formatter

[Ruff](https://docs.astral.sh/ruff/) replaces multiple tools (Black, Flake8, isort) with a single, fast implementation.

**Configuration**: `pyproject.toml` → `[tool.ruff]`

#### Key Features
- **Formatting**: Consistent code style (88-character line length)
- **Linting**: 500+ rules covering code correctness and style
- **Import Sorting**: Automatic import organization
- **Fast**: 10-100x faster than traditional tools

#### Usage

See [Command Cheatsheet](../command-cheatsheet.md#code-quality-commands) for all Ruff commands.

#### Enabled Rules

| Category | Rules | Description |
|----------|--------|-------------|
| **E4, E7, E9** | pycodestyle | Indentation, statements, runtime errors |
| **F** | pyflakes | Code correctness (unused imports, undefined names) |
| **B** | flake8-bugbear | Likely bugs and design problems |
| **D** | pydocstyle | Docstring conventions (PEP 257) |
| **N** | pep8-naming | Naming conventions |
| **ERA** | eradicate | Commented-out code detection |

#### Ignored Rules
- `D107`: Missing docstring in `__init__` (optional for simple constructors)
- `D213`: Multi-line summary format (prefer D212)
- `E501`: Line too long (handled by formatter)
- `F401`: Module imported but unused (in `__init__.py` files)

### Mypy - Static Type Checker

[Mypy](https://mypy-lang.org/) analyzes type hints to catch type-related errors before runtime.

**Configuration**: `pyproject.toml` → `[tool.mypy]`

#### Benefits
- **Early Error Detection**: Catch type mismatches before runtime
- **Better Documentation**: Type hints serve as documentation
- **IDE Support**: Enhanced autocomplete and refactoring
- **Maintainability**: Easier to understand and modify code

#### Usage

See [Command Cheatsheet](../command-cheatsheet.md#code-quality-commands) for mypy commands.

#### Best Practices

```python
# Good: Clear type hints
def calculate_total(prices: list[float]) -> float:
    """Calculate total price from a list of prices."""
    return sum(prices)

# Good: Optional parameters
from typing import Optional

def greet(name: str, title: Optional[str] = None) -> str:
    """Greet a person with optional title."""
    if title:
        return f"Hello, {title} {name}!"
    return f"Hello, {name}!"

# Good: Generic types
from typing import Dict, List

def process_data(data: Dict[str, List[int]]) -> Dict[str, float]:
    """Process numerical data and return averages."""
    return {key: sum(values) / len(values) for key, values in data.items()}
```

### Deptry - Dependency Analysis

[Deptry](https://deptry.com/) analyzes your project to find:
- **Unused dependencies**: Installed but not imported
- **Missing dependencies**: Imported but not declared
- **Misplaced dependencies**: Dev dependencies used in production code

**Configuration**: `pyproject.toml` → `[tool.deptry]`

#### Usage

See [Command Cheatsheet](../command-cheatsheet.md#code-quality-commands) for dependency analysis commands.

## Code Style Standards

### PEP 8 Compliance

| Standard | Configuration | Enforcement |
|----------|--------------|-------------|
| **Line Length** | 88 characters | Ruff formatter |
| **Indentation** | 4 spaces | Ruff formatter |
| **Naming** | snake_case functions, PascalCase classes | Ruff N-rules |
| **Imports** | Sorted, grouped | Ruff formatter |
| **Docstrings** | PEP 257 (reST format) | Ruff D-rules |

### Docstring Standards

We use **reStructuredText (reST)** format for docstrings:

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price.

    Apply a percentage discount to a given price and return the
    discounted amount.

    :param price: Original price before discount
    :param discount_percent: Discount percentage (0-100)
    :return: Price after applying discount
    :raises ValueError: If discount_percent is not between 0 and 100

    Examples:
        >>> calculate_discount(100.0, 10.0)
        90.0
        >>> calculate_discount(50.0, 25.0)
        37.5
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount percent must be between 0 and 100")

    return price * (1 - discount_percent / 100)
```

## Local Development Workflow

### VS Code Integration

The project includes VS Code settings (`.vscode/settings.json`) that automatically:

- **Format on Save**: Runs Ruff formatter
- **Show Problems**: Displays lint errors inline
- **Type Checking**: Shows Mypy errors
- **Auto-fix**: Fixes issues when possible

### Manual Workflow

1. **Write Code**: Focus on functionality first
2. **Format**: `task format` or save in VS Code
3. **Check**: `task check` to run all quality checks
4. **Fix**: `task lint-fix` for auto-fixable issues
5. **Type Check**: Address any Mypy errors
6. **Test**: Run tests to ensure functionality

### Pre-commit Integration

Quality checks run automatically before each commit:

```bash
# Install hooks (done by dev-setup)
uv run pre-commit install

# Run manually on all files
task pre-commit
# or: uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run
```

## Quality Metrics and Targets

### Code Quality Targets

| Metric | Target | Tool | Command |
|--------|--------|------|---------|
| **Ruff Issues** | 0 errors | Ruff | `task check` |
| **Type Coverage** | 100% | Mypy | `task typecheck` |
| **Test Coverage** | >80% | pytest-cov | `task test-html` |
| **Dependency Health** | 0 issues | Deptry | `task deps-check` |

### Quality Reports

```bash
# Generate comprehensive quality report
task ci-local

# Individual reports
task format          # Shows formatting issues
task typecheck       # Shows type errors
task deps-check      # Shows dependency issues
task test-html       # Generates coverage report in htmlcov/
```

## Troubleshooting

### Common Issues

**Ruff formatting conflicts:**
```bash
# Reset formatting
task format
git add .
git commit -m "Fix formatting"
```

**Mypy cache issues:**
```bash
# Clear Mypy cache
rm -rf .mypy_cache
task typecheck
```

**Pre-commit failures:**
```bash
# Skip pre-commit temporarily (not recommended)
git commit --no-verify -m "Emergency commit"

# Fix issues and commit properly
task lint-fix
git add .
git commit -m "Fix quality issues"
```

**Dependency conflicts:**
```bash
# Regenerate lock file
uv lock --upgrade
uv sync
```

### Configuration Customization

You can customize quality settings in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88  # Adjust line length

[tool.ruff.lint]
ignore = ["E501"]  # Add rules to ignore

[tool.mypy]
strict = true  # Enable strict mode
```

## Integration with CI/CD

Quality checks are enforced in GitHub Actions:

- **Pre-commit CI**: Runs on every push/PR
- **Test CI**: Includes coverage and dependency checks
- **Security CI**: Scans for vulnerabilities

See [CI/CD Workflows](../ci-cd/workflows.md) for details.

---

**Next Steps**: Learn about [Testing](testing.md) to ensure your code works correctly.
