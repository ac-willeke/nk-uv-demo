# Troubleshooting

This guide helps you diagnose and resolve common issues when working with nk-uv-demo.

## Quick Diagnostics

Run these commands to gather information about your setup:

```bash
# Check tool versions
uv --version
python --version
git --version

# Check project status
uv run python -m setuptools_scm  # Current version
task check  # Overall project health

# Check environment
uv run python -c "import sys; print(sys.path)"
ls -la .venv/  # Virtual environment exists
```

## Installation Issues

### uv not found

**Problem**: `uv: command not found`

**Solutions**:
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc

# Check PATH
echo $PATH | grep -o "[^:]*uv[^:]*"
```

### Python version issues

**Problem**: Wrong Python version or `python not found`

**Solutions**:
```bash
# Check available Python versions
uv python list

# Install specific Python version
uv python install 3.12

# Set project Python version
echo "3.12" > .python-version
uv sync
```

### Virtual environment issues

**Problem**: Virtual environment not created or corrupted

**Solutions**:
```bash
# Remove and recreate virtual environment
rm -rf .venv
uv sync

# Check virtual environment
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

python --version  # Should show expected version
deactivate
```

### Dependency installation failures

**Problem**: `uv sync` or `uv add` fails

**Solutions**:
```bash
# Clear uv cache
uv cache clean

# Update lock file
uv lock --upgrade

# Reinstall from scratch
rm uv.lock .venv -rf
uv sync

# Check for conflicts
uv tree  # Show dependency tree
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
code . --new-window
```

### Pre-commit hooks not working

**Problem**: Pre-commit hooks don't run or fail unexpectedly

**Solutions**:
```bash
# Reinstall pre-commit hooks
uv run pre-commit uninstall
uv run pre-commit install

# Clear pre-commit cache
uv run pre-commit clean

# Test hooks manually
uv run pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "Emergency commit"
```

### Import errors in notebooks

**Problem**: Cannot import nk_uv_demo in Jupyter notebooks

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

## Code Quality Issues

### Ruff formatting conflicts

**Problem**: Code formatting keeps changing or conflicts

**Solutions**:
```bash
# Apply consistent formatting
task format
git add .
git commit -m "Apply consistent formatting"

# Check Ruff configuration
uv run ruff config

# Reset formatting to project standards
uv run ruff format --check
uv run ruff format .
```

### Mypy type checking errors

**Problem**: Mypy reports type errors

**Common Solutions**:

```python
# Add missing type annotations
def my_function(x: int) -> str:  # Add return type
    return str(x)

# Handle optional values
from typing import Optional

def process_data(data: Optional[str] = None) -> str:
    if data is None:
        return "No data"
    return data.upper()

# Import type hints for third-party libraries
# Add to dev dependencies:
# uv add --group dev types-requests
```

**Configuration Issues**:
```bash
# Clear mypy cache
rm -rf .mypy_cache
uv run mypy src/

# Check mypy configuration
uv run mypy --config-file pyproject.toml --show-config
```

### Test failures

**Problem**: Tests fail unexpectedly

**Debugging Steps**:
```bash
# Run tests with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_main.py::test_specific_function -v

# Run tests with debug output
uv run pytest -s  # Show print statements

# Run tests with coverage details
uv run pytest --cov --cov-report=term-missing

# Debug test environment
uv run python -c "
import sys
print('Python path:', sys.path)
try:
    import nk_uv_demo
    print('Package location:', nk_uv_demo.__file__)
except ImportError as e:
    print('Import error:', e)
"
```

### Dependency conflicts

**Problem**: `deptry` reports unused or missing dependencies

**Solutions**:
```bash
# Check dependency usage
uv run deptry . --verbose

# Add missing dependency
uv add missing-package

# Remove unused dependency
uv remove unused-package

# Check if dependency is used in tests only
uv add --group dev test-only-package

# Ignore specific dependencies (in pyproject.toml)
[tool.deptry]
ignore_missing = ["known-false-positive"]
ignore_unused = ["development-tool"]
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

# Skip Safety temporarily (not recommended)
SKIP=safety git commit -m "Skip safety check"
```

### CodeQL analysis issues

**Problem**: CodeQL workflow fails in GitHub Actions

**Solutions**:
- Check GitHub Actions logs for specific errors
- Ensure repository has CodeQL enabled in Security tab
- Verify workflow has proper permissions:
  ```yaml
  permissions:
    security-events: write
  ```

### Dependabot issues

**Problem**: Dependabot PRs failing or not created

**Solutions**:
- Check `.github/dependabot.yaml` configuration
- Verify Dependabot is enabled in repository settings
- Check for dependency conflicts in PRs
- Manually update problematic dependencies:
  ```bash
  uv lock --upgrade
  ```

## CI/CD Issues

### GitHub Actions failures

**Problem**: Workflows fail in CI but work locally

**Common Causes and Solutions**:

**Cache issues**:
```yaml
# Clear workflow caches in GitHub Actions settings
# Or update cache key in workflow files
```

**Environment differences**:
```bash
# Test in clean environment locally
docker run --rm -v $(pwd):/app -w /app python:3.12 bash -c "
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH=~/.local/bin:$PATH
  uv sync
  uv run task ci-local
"
```

**Permission issues**:
```yaml
# Check workflow permissions
permissions:
  contents: read
  id-token: write  # For PyPI publishing
```

### Package building issues

**Problem**: `uv build` or `task build` fails

**Debugging Steps**:
```bash
# Check package structure
find src/ -name "*.py" | head -10

# Verify setuptools-scm can determine version
uv run python -m setuptools_scm

# Check for missing files
uv build --verbose

# Inspect built package
ls -la dist/
unzip -l dist/*.whl  # Check wheel contents
```

### Deployment failures

**Problem**: Package deployment to Test PyPI fails

**Common Issues**:

**Trusted publishing not configured**:
1. Go to [Test PyPI trusted publishers](https://test.pypi.org/manage/account/publishing/)
2. Add repository: `ac-willeke/nk-uv-demo`
3. Workflow name: `cd-publish-testpypi.yml`

**Version conflicts**:
```bash
# Check existing versions on Test PyPI
# Create new version tag
git tag v1.0.1
git push origin v1.0.1
```

**Network issues**:
- Retry the workflow manually
- Check GitHub Actions status page

## Performance Issues

### Slow test execution

**Problem**: Tests take too long to run

**Solutions**:
```bash
# Run tests in parallel (if supported)
uv run pytest -n auto  # Requires pytest-xdist

# Skip slow tests during development
uv run pytest -m "not slow"

# Profile test execution
uv run pytest --durations=10

# Run specific test subset
uv run pytest tests/unit/  # Fast unit tests only
```

### Slow pre-commit hooks

**Problem**: Pre-commit hooks are too slow

**Solutions**:
```bash
# Run hooks in parallel
uv run pre-commit run --all-files -j auto

# Skip slow hooks during development
SKIP=mypy git commit -m "Quick fix"

# Update pre-commit hooks for better performance
uv run pre-commit autoupdate
```

## File and Directory Issues

### Permission errors

**Problem**: Permission denied errors when running commands

**Solutions**:
```bash
# Linux/macOS: Fix file permissions
chmod +x scripts/*.sh
chmod -R u+w .venv/

# Windows: Run as administrator or check file locks
# Ensure no processes are using files in .venv
```

### Large file issues

**Problem**: Git rejects large files or pre-commit hook fails

**Solutions**:
```bash
# Check for large files
find . -type f -size +100M | grep -v .git

# Remove large files from git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all

# Use Git LFS for large files (if needed)
git lfs track "*.pdf"
echo "*.pdf filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
```

### Import path issues

**Problem**: Module import errors or circular imports

**Solutions**:
```python
# Use absolute imports in package
from nk_uv_demo.module import function

# Avoid circular imports
# Move shared code to separate module
# Use TYPE_CHECKING for type-only imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .other_module import SomeClass
```

## Platform-Specific Issues

### Windows-specific issues

**PowerShell execution policy**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path separators**:
```python
from pathlib import Path
# Use Path instead of string concatenation
config_path = Path(__file__).parent / "config.json"
```

### macOS-specific issues

**Command Line Tools**:
```bash
xcode-select --install
```

**Homebrew conflicts**:
```bash
# Use uv-managed Python instead of system Python
uv python install 3.12
```

### Linux-specific issues

**Missing system dependencies**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

## Getting Additional Help

### Information Gathering

When asking for help, include:

```bash
# System information
uname -a  # Operating system
uv --version
python --version

# Project status
uv run python -m setuptools_scm
task check 2>&1 | head -20

# Error logs
uv run pytest --tb=long  # Full traceback
```

### Resources

- **GitHub Issues**: Report bugs and ask questions
- **GitHub Discussions**: Community support and best practices
- **Tool Documentation**:
  - [uv Documentation](https://docs.astral.sh/uv/)
  - [Ruff Documentation](https://docs.astral.sh/ruff/)
  - [pytest Documentation](https://docs.pytest.org/)
  - [pre-commit Documentation](https://pre-commit.com/)

### Creating Reproducible Bug Reports

```bash
# Create minimal reproduction case
git checkout -b bug-reproduction
# ... minimal code to reproduce issue ...
git commit -m "Reproduce issue"
git push origin bug-reproduction
# Include link in GitHub issue
```

---

**Need more help?** Check the [GitHub Issues](https://github.com/ac-willeke/nk-uv-demo/issues) or create a new issue with detailed information about your problem.
