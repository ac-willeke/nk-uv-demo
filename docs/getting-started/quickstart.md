# Quick Start Guide

Get up and running with nk-uv-demo using the Taskfile workflow.

## Prerequisites

- Complete the [installation](installation.md)
- Have [Task](https://taskfile.dev/installation/) installed

## Demo

### 1. Test the Package

```bash
# Run the main CLI command
task run
# Expected output: Hello from nk-uv-demo!

# Alternative without Task
uv run nk-uv-demo
```

### 2. Explore Development Commands

```bash
# See all available tasks
task --list

# Run development checks
task check
# This runs: formatting, linting, type checking, tests, and dependency analysis

# Format and fix code issues
task lint-fix
```

### 3. Try the Jupyter Notebook

```bash
# Open the demo notebook (if you have Jupyter installed)
jupyter notebook notebooks/demo.ipynb

# Or use VS Code to open notebooks/demo.ipynb
code notebooks/demo.ipynb
```

## Common Taskfile Commands

### Development Workflow

```bash
task dev-setup           # Complete development setup (one-time)
task check              # Run all quality checks
task test-html          # Run tests with HTML coverage
task build              # Build the package
```

For complete command reference, see [Command Cheatsheet](../command-cheatsheet.md).

## Testing Different Features

### 1. Code Quality Tools

```bash
# See linting in action (introduce an error first)
echo "import os  # unused import" >> src/nk_uv_demo/__init__.py
task check  # Should show the linting error

# Fix it automatically
task lint-fix
```

### 2. Testing Framework

```bash
# Run tests with coverage
task test-html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### 3. Pre-commit Hooks

```bash
# Test pre-commit hooks
echo "bad_code = 'not formatted'" >> src/nk_uv_demo/__init__.py
git add .
git commit -m "Test commit"  # Should trigger pre-commit checks
```

### 4. Package Building

```bash
# Build and inspect the package
task build
ls dist/  # Should show .tar.gz and .whl files

# Test installation
pip install dist/nk_uv_demo-*.whl
nk-uv-demo  # Should work
pip uninstall nk-uv-demo
```

## Next Steps

1. **Learn development workflow**: Read the [Development Guide](../development.md)
2. **Understand CI/CD**: Check out [Workflows](../ci-cd/workflows.md)
3. **Contribute**: Follow the development practices in the guide

## Command Reference

See [Command Cheatsheet](../command-cheatsheet.md) for all available commands organized by tool.
