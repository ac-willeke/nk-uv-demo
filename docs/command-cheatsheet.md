# Command Cheatsheet

## Project Setup Commands

| Description | Command |
|-------------|---------|
| Clone repository | `gh repo clone ac-willeke/nk-uv-demo` |
| Navigate to directory | `cd nk-uv-demo` |
| Complete development setup | `task dev-setup` |
| Install dependencies only | `uv sync` |
| Install package in development mode | `uv pip install -e .` |

## uv Commands

| Description | Command |
|-------------|---------|
| Check uv version | `uv --version` |
| Install Python version | `uv python install 3.12` |
| List Python versions | `uv python list` |
| Sync dependencies | `uv sync` |
| Add dependency | `uv add package_name` |
| Add development dependency | `uv add --group dev package_name` |
| Remove dependency | `uv remove package_name` |
| Update dependencies | `uv lock --upgrade` |
| Run command in environment | `uv run command` |
| Build package | `uv build` |
| Show dependency tree | `uv tree` |
| Clean cache | `uv cache clean` |

## Taskfile Commands

| Description | Command |
|-------------|---------|
| Complete development setup | `task dev-setup` |
| Run application | `task run` |
| List all tasks | `task --list` |
| Show task help | `task help` |
| Run all quality checks | `task check` |
| Run CI simulation | `task ci-local` |
| Format code | `task format` |
| Fix linting issues | `task lint-fix` |
| Run type checking | `task typecheck` |
| Run tests | `task test` |
| Run tests with HTML coverage | `task test-html` |
| Check dependencies | `task deps-check` |
| Run security scans | `task security` |
| Run pre-commit hooks | `task pre-commit` |
| Build package | `task build` |
| Clean build artifacts | `task clean` |
| Show current version | `task version` |
| Create and push version tag | `task tag VERSION=v1.0.0` |

## Code Quality Commands

| Description | Command |
|-------------|---------|
| Format code with Ruff | `uv run ruff format` |
| Check code with Ruff | `uv run ruff check` |
| Auto-fix linting issues | `uv run ruff check --fix` |
| Type check with mypy | `uv run mypy src/` |
| Check dependencies | `uv run deptry .` |

## Testing Commands

| Description | Command |
|-------------|---------|
| Run all tests | `uv run pytest` |
| Run tests with coverage | `uv run pytest --cov` |
| Run tests with HTML coverage | `uv run pytest --cov --cov-report=html` |
| Run tests with XML coverage | `uv run pytest --cov --cov-report=xml` |
| Run specific test file | `uv run pytest tests/test_main.py` |
| Run specific test function | `uv run pytest tests/test_main.py::test_function` |
| Run tests with verbose output | `uv run pytest -v` |
| Run tests with debug output | `uv run pytest -s` |
| Run tests matching pattern | `uv run pytest -k "test_pattern"` |
| Show test durations | `uv run pytest --durations=10` |

## Security Commands

| Description | Command |
|-------------|---------|
| Authenticate with Safety | `uv run safety auth login --headless` |
| Scan dependencies for vulnerabilities | `uv run safety scan` |
| Scan with JSON output | `uv run safety scan --output json` |
| Audit GitHub Actions workflows | `uv run zizmor .github/workflows/` |
| Audit workflows with verbose output | `uv run zizmor --verbose .github/workflows/` |

## Pre-commit Commands

| Description | Command |
|-------------|---------|
| Install pre-commit hooks | `uv run pre-commit install` |
| Run hooks on all files | `uv run pre-commit run --all-files` |
| Run hooks on staged files | `uv run pre-commit run` |
| Run specific hook | `uv run pre-commit run ruff` |
| Run hooks on specific files | `uv run pre-commit run --files src/main.py` |
| Update hook versions | `uv run pre-commit autoupdate` |
| Uninstall hooks | `uv run pre-commit uninstall` |
| Clean pre-commit cache | `uv run pre-commit clean` |
| Skip hooks for one commit | `git commit --no-verify -m "message"` |

## Git Commands

| Description | Command |
|-------------|---------|
| Check git status | `git status` |
| Stage all changes | `git add .` |
| Commit changes | `git commit -m "commit message"` |
| Push to remote | `git push origin main` |
| Pull from remote | `git pull origin main` |
| Create new branch | `git checkout -b branch-name` |
| Switch branches | `git checkout branch-name` |
| View commit history | `git log --oneline` |
| Create version tag | `git tag v1.0.0` |
| Push tags | `git push --tags` |
| List tags | `git tag --list` |

## Version Management Commands

| Description | Command |
|-------------|---------|
| Show current version | `uv run python -m setuptools_scm` |
| Create version tag | `git tag v1.0.0` |
| Push version tag | `git push origin v1.0.0` |
| List recent tags | `git tag --list --sort=-version:refname \| head -10` |

## Package Building Commands

| Description | Command |
|-------------|---------|
| Build package | `uv build` |
| Build wheel only | `uv build --wheel` |
| Build source distribution only | `uv build --sdist` |
| List build artifacts | `ls dist/` |
| Inspect wheel contents | `unzip -l dist/*.whl` |
| Inspect source distribution | `tar -tzf dist/*.tar.gz` |

## Package Testing Commands

| Description | Command |
|-------------|---------|
| Install from local wheel | `pip install dist/*.whl` |
| Test CLI command | `nk-uv-demo` |
| Test from Test PyPI | `pip install -i https://test.pypi.org/simple/ nk-uv-demo` |
| Uninstall package | `pip uninstall nk-uv-demo` |

## Development Environment Commands

| Description | Command |
|-------------|---------|
| Activate virtual environment | `source .venv/bin/activate` (Linux/macOS) |
| Activate virtual environment | `.venv\Scripts\activate` (Windows) |
| Deactivate virtual environment | `deactivate` |
| Check Python interpreter | `which python` |
| Check Python version | `python --version` |
| List installed packages | `pip list` |

## VS Code Commands

| Description | Command |
|-------------|---------|
| Open project in VS Code | `code .` |
| Open specific file | `code filename.py` |
| Reload VS Code window | `Ctrl+Shift+P` → "Developer: Reload Window" |
| Select Python interpreter | `Ctrl+Shift+P` → "Python: Select Interpreter" |

## Jupyter Commands

| Description | Command |
|-------------|---------|
| Start Jupyter notebook | `jupyter notebook` |
| Start Jupyter lab | `jupyter lab` |
| List running servers | `jupyter notebook list` |
| Stop Jupyter server | `jupyter notebook stop` |

## Troubleshooting Commands

| Description | Command |
|-------------|---------|
| Clear Python cache | `find . -name "*.pyc" -delete` |
| Remove virtual environment | `rm -rf .venv` |
| Reset uv cache | `uv cache clean` |
| Clear mypy cache | `rm -rf .mypy_cache` |
| Clear pytest cache | `rm -rf .pytest_cache` |
| Clear ruff cache | `rm -rf .ruff_cache` |
| Check disk usage | `du -sh .venv/` |
| Check file permissions | `ls -la .venv/` |

## GitHub Actions Commands

| Description | Command |
|-------------|---------|
| Trigger manual workflow | GitHub UI → Actions → Select workflow → "Run workflow" |
| View workflow logs | GitHub UI → Actions → Select run → View logs |
| Download workflow artifacts | GitHub UI → Actions → Select run → Artifacts |
| Check workflow status | `gh run list` (with GitHub CLI) |
| View specific run | `gh run view <run-id>` (with GitHub CLI) |

## Docker Commands (Future Enhancement)

| Description | Command |
|-------------|---------|
| Build Docker image | `docker build -t nk-uv-demo .` |
| Run Docker container | `docker run -it nk-uv-demo` |
| List Docker images | `docker images` |
| Remove Docker image | `docker rmi nk-uv-demo` |
| Clean up Docker | `docker system prune` |
