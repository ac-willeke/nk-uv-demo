# Installation Guide

This guide will walk you through setting up the nk-uv-demo project on your local machine.

## Prerequisites

Before starting, ensure you have the [required tools](requirements.md) installed on your system.

## Clone the Repository

```bash
# Clone from GitHub
gh repo clone ac-willeke/nk-uv-demo
cd nk-uv-demo

# Alternative: using git directly
git clone https://github.com/ac-willeke/nk-uv-demo.git
cd nk-uv-demo
```

## Installation Methods

Choose the method that best fits your workflow:

### Method 1: Using Taskfile (Recommended)

If you have [Task](https://taskfile.dev/installation/) installed:

```bash
# Complete development setup (installs dependencies, hooks, and runs checks)
task dev-setup

# See all available tasks
task --list
```

The `dev-setup` task will:
- Install Python dependencies with uv
- Set up pre-commit hooks
- Run initial code quality checks
- Install the package in development mode

### Method 2: Manual Setup with uv

If you prefer manual control or don't have Task installed:

See [Command Cheatsheet](../command-cheatsheet.md) for individual setup commands.

## Verify Installation

```bash
task run                 # Test the CLI command
task check              # Run all quality checks
```

See [Command Cheatsheet](../command-cheatsheet.md) for individual verification commands.

## Development Environment Setup

### VS Code Integration

The project includes VS Code configuration for optimal development experience:

1. **Extensions**: Install recommended extensions (VS Code will prompt you)
2. **Python Environment**: VS Code should automatically detect the `.venv` created by uv
3. **Settings**: Code formatting, linting, and type checking are pre-configured

#### Manual Python Environment Selection (if needed)

If VS Code doesn't automatically detect the virtual environment:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Python: Select Interpreter"
3. Choose the interpreter in `./.venv/bin/python` (Linux/macOS) or `.\.venv\Scripts\python.exe` (Windows)

### Terminal Environment

To activate the virtual environment in your terminal:

```bash
# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Verify activation (should show the project's Python)
which python
python --version
```

### Jupyter Notebook Setup

To use the project package in Jupyter notebooks:

1. Open the demo notebook: `notebooks/demo.ipynb`
2. Select the `.venv` kernel when prompted
3. The `ipykernel` dependency is already included in the dev dependencies

## Troubleshooting

### Common Issues

**Python version mismatch:**
```bash
# Check Python version
uv python list
uv python install 3.12  # Install if needed
```

**Permission issues:**
```bash
# On Linux/macOS, you might need to make scripts executable
chmod +x run.sh
```

**uv not found:**
```bash
# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc, ~/.profile
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](../troubleshooting.md)
2. Review the GitHub Issues for known problems
3. Run `task help` for detailed workflow information

## Next Steps

Now that you have the project set up:

- Try the [Quick Start Guide](quickstart.md) to explore features
- Learn about the [Development Workflow](../development.md)
