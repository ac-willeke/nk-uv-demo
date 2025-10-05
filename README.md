# Naturkart uv demo - Python DevOps best practices

This repository demonstrates best practices for Python project development and packaging. It showcases how to structure a Python project, manage dependencies with uv, implement CI/CD pipelines using GitHub Actions, and containerize code with Docker.

## Checklist

- [x] Open-source **license** (e.g. MIT)
- [x] Repo **naming convention** (`nk-<name>`, `nkf-<name>`, etc.)
- [x] GitHub Action workflow for **code security** (Dependabot, CodeQL)

## Requirements

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [GitHub](https://github.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/engine/install/) (optional)
- [VS Code](https://code.visualstudio.com/) (optional)

## Demo walk-through

To follow this walk-through you must  **clone** the repository to your local machine.

```bash
# clone from github and navigate to folder
gh repo clone naturkart-miljodir/nk-uv-demo
cd ~/git/nk-uv-demo
```

### **Test** the uv python package from CLI

```bash
# Run the entrypoint
uv run nk-uv-demo
# > Hello from nk-uv-demo!
```

For more uv commands check: [CLI Reference](https://docs.astral.sh/uv/reference/cli/)

### **Connect** to the Python environment `.venv`

In Visual Studio Code, the Python extension and Jupyter Notebooks extension detect the `.venv` created by `uv` package manager as the default environment. If not, set the enviroment manually.

#### 1. Connect in Python Scripts

- Open a Python script in VS Code.
- Click on the Python version in the bottom left corner of the VS Code window.
- Click on "Enter interpreter path..." > enter path to python.exe in the .venv environment: `./.venv/Scripts/python.exe` or `./.venv/bin/python.exe`

#### 2. Connect from the terminal

```bash
# connect .venv environment
source .venv/bin/activate
```

#### 3. Connect in Jupyter Notebooks

- Open the notebook [notebooks/demo.ipynb](./notebooks/demo.ipynb)
- Select `.venv` as Kernel
    - Right-upper corner > "Select Kernel" > "add path to Kernel"
- Run the notebook cells to test whether you can use the local package inside the notebook.

**Note:** To use the *.venv* inside notebooks the `ipykernel` must be installed in the *.venv*. You can install it as development dependency using:

```bash
# add specific version of ipykernel to dev
uv add --group dev "ipykernel>=6.29.5,<7"
```

### **Code Quality** and **Security**

This repository implements multiple layers of code quality checks and security measures to ensure reliable, maintainable, and secure code.

#### Code Quality Tools

- **[Ruff](https://docs.astral.sh/ruff/):** Fast Python linter and formatter (replaces flake8, black, isort)
- **[Mypy](https://mypy-lang.org/):** Static type checker for Python type hints
- **[pytest](https://docs.pytest.org/en/stable/):** Testing framework for unit and integration tests
- **[Deptry](https://deptry.com/):** Dependency analyzer to find unused, missing, or misplaced dependencies


#### Security Tools

- **[Dependabot](https://github.com/dependabot):** Automated dependency updates and vulnerability scanning
- **[CodeQL](https://codeql.github.com/):** Semantic code analysis for security vulnerabilities
- **[Safety](https://pypi.org/project/safety/):** Python dependency vulnerability scanner, requires an account which you can link with GitHub.
- **[Zizmor](https://docs.zizmor.sh/):** GitHub Actions workflow security auditing

#### Local Development Commands

```bash
# Code formatting and linting
uv run ruff format        # Format code
uv run ruff check         # Lint code
uv run ruff check --fix   # Auto-fix linting issues

# Type checking
uv run mypy src/

# Dependency analysis
uv run deptry .          # Check for dependency issues

# Testing
uv run pytest           # Run all tests
uv run pytest --cov     # Run tests with coverage
uv run pytest --cov --cov-report=html # Run tests with HTML coverage report

# Security scanning (requires free Safety account)
uv run safety auth login --headless  # First-time setup: authenticate with Safety
uv run safety scan         # Scan for known vulnerabilities
zizmor .github/workflows/  # Audit GitHub Actions workflows

# Pre-commit hooks
pre-commit install        # Install git hooks (one-time setup)
pre-commit run --all-files  # Run all hooks on all files
pre-commit run --files <file1> <file2>  # Run hooks on specific files
```

#### Quality Gates

Code quality is enforced at multiple stages:

- **Local Development:** VS Code [settings](.vscode/settings.json) and [extensions](.vscode/extensions.json) provide real-time feedback
- **Pre-commit Hooks:** Automated checks before each commit
- **GitHub Actions:** Continuous integration checks on push and pull requests
- **Dependabot:** Automated security updates for dependencies
- **CodeQL:** Security vulnerability scanning

#### Style and Convention Rules

Summary of PEP8 style rules and enforcement in this repository:

| Practice | PEP8 | Repository | Tool | Local check | pre-commit | GHA |
|----------|------|------------|------|-------------|------------|-----|
| Max line length | 79  | 88  | Ruff [E501] | `uv run ruff check` | ✅ | ✅ |
| Docstring and comment length | 72  | 78  | not enforced | - | - | - |
| Docstring convention | PEP257 | reStructuredText (reST) | Ruff [D] | `uv run ruff check` | ✅ | ✅ |
| Indentation | 4 spaces | PEP8 | Ruff [E111] | `uv run ruff format --check` | ✅ | ✅ |
| Naming convention - variables, functions, methods | snake_case | PEP8 | Ruff [N] | `uv run ruff check` | ✅ | ✅ |
| Naming convention - variables with constant values | ALL_CAPS | PEP8 | Ruff [N] | `uv run ruff check` | ✅ | ✅ |
| Naming convention - classes | CapWords | PEP8 | Ruff [N] | `uv run ruff check` | ✅ | ✅ |
| Type checking | - | enforced | mypy | `uv run mypy` | ✅ | ✅ |
| Language | English | PEP8 | not enforced | - | - | - |

#### Testing and Security Rules

| Category | Practice | Tool | Local check | GHA File | pre-commit | GHA |
|----------|----------|------|-------------|----------|------------|-----|
| **Testing** | Unit tests | pytest | `uv run pytest` | `ci-pytest.yml` | ❌ | ✅ |
| **Testing** | Test coverage | pytest-cov | `uv run pytest --cov` | `ci-pytest.yml` | ❌ | ✅ |
| **Dependencies** | Dependency analysis | Deptry | `uv run deptry .` | `ci-pytest.yml` | ❌ | ✅ |
| **Security** | Dependency vulnerabilities | Dependabot | - | `dependabot.yaml` | ❌ | ✅ |
| **Security** | Code vulnerabilities | CodeQL | - | `cicd-codeql-analysis.yaml` | ❌ | ✅ |
| **Security** | Python package security | Safety | `uv run safety scan` | `ci-safety-action.yml` | ❌ | ✅ |
| **Security** | GitHub Actions security | Zizmor | `zizmor .github/workflows/` | `cicd-zizmor.yml` | ✅ | ✅ |


TODO:
- GHA - package release
- GHA - docker
- Setup Docker
    - prod container
    - devcontainer
    - GHCR
