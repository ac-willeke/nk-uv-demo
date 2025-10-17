# Troubleshooting

This guide helps you diagnose and resolve common issues when working with uv-demo.

## Quick Diagnostics

Run these commands to gather information about your setup:

```bash
# Check tool versions
uv --version
uv python pin --resolved # Python version of current .venv

# Check project status
uv run python -m setuptools_scm  # Current version
task check  # Overall project health

# Check environment
uv run python -c "import sys; print(sys.path)"
ls -la .venv/  # Virtual environment exists
```

## Development Environment Issues

### VS Code not detecting Python environment

**Problem**: VS Code uses wrong Python interpreter

**Solutions**:
1. **Command Palette** (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose `./.venv/bin/python` (Linux/macOS) or `.\.venv\Scripts\python.exe` (Windows)

**Alternative**:
```bash
# Check interpreter path
which python  # Should point to .venv

# Restart VS Code
# CTRL+SHIFT+P → "Reload Window"
```

### Import errors in notebooks

**Problem**: Cannot import uv_demo in Jupyter notebooks

**Solutions**:
```bash
# Install package in development mode
uv pip install -e .

# Ensure ipykernel is installed
uv add --group dev "ipykernel>=6.29.5"

# Restart Jupyter kernel
# In notebook: Kernel → Restart Kernel

# Check kernel in VS Code
# Select .venv kernel when opening notebook
```

## Security and Safety Issues

### Safety authentication issues

**Problem**: Safety scan fails with authentication errors

**Solutions**:
```bash
# Login to Safety (required for free account)
uv run safety auth login --headless

# Check Safety configuration
cat .safety-project.ini

# Run Safety with debug output
uv run safety scan --debug
```

### Deployment failures

**Problem**: Package deployment to Test PyPI fails

**Common Issues**:

**Trusted publishing not configured**:
1. Go to [Test PyPI trusted publishers](https://test.pypi.org/manage/account/publishing/)
2. Add repository: `ac-willeke/nk-uv-demo`
3. Workflow name: `cd-publish-testpypi.yml`

**Version conflicts**:

Only "clean" version tags can be deployed. Ensure no existing release with the same version exists and that the version follows semantic versioning.

```bash
# Check existing versions on Test PyPI

# Check current version
uv run python -m setuptools_scm

# Create new "clean" version tag
git tag vx.y.z
git push origin vx.y.z
```
