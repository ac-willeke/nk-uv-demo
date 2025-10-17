# Naturkart uv demo - Python DevOps best practices

This repository demonstrates best practices for Python project development and packaging. It showcases how to structure a Python project, manage dependencies with uv, setup security scanning and CI/CD pipelines using GitHub Actions and containerize code with Docker.

## Checklist

- [x] Open-source **license** (MIT)
- [x] Repo **naming convention** (`nk-<name>`, `nkf-<name>`, etc.)
- [x] GitHub Action workflows for **CI/CD** (testing, security, deployment)


## Quick Start with Taskfile (Recommended)

If you have [Task](https://taskfile.dev/installation/) installed, you can use the simplified workflow:

```bash
# Clone and setup
gh repo clone ac-willeke/nk-uv-demo
cd nk-uv-demo

# Complete development setup (installs dependencies, hooks, and runs checks)
task dev-setup

# Run the application
task run

# See all available tasks
task --list
```

### Common Taskfile Commands

```bash
# Development
task install          # Install dependencies
task format           # Format code with Ruff
task lint-fix          # Fix linting issues
task test-html         # Run tests with HTML coverage report

# Code quality
task check            # Run all quality checks (lint, typecheck, test, deps)
task pre-commit       # Run pre-commit hooks on all files

# Build and release
task build            # Build the package
task clean            # Clean build artifacts
task tag VERSION=v1.0.0  # Create and push version tag

# Help
task help             # Show detailed workflow help
```

## Demo walk-through

To follow this walk-through you must  **clone** the repository to your local machine.

```bash
# clone from github and navigate to folder
gh repo clone ac-willeke/nk-uv-demo
cd nk-uv-demo
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

**With Taskfile (Recommended):**
```bash
# All-in-one commands
task dev-setup           # Complete development setup
task check               # Run all quality checks
task ci-local            # Simulate CI pipeline locally

# Individual tasks
task format              # Format code
task lint-fix            # Auto-fix linting issues
task typecheck           # Type checking
task deps-check          # Dependency analysis
task test-html           # Tests with HTML coverage
task security            # Security scans
task pre-commit          # Run all pre-commit hooks

# Build and version
task build               # Build package
task version             # Show current version
task tag VERSION=v1.0.0  # Create release tag
```

**Direct uv commands:**
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

# Dynamic versioning - setuptools-scm
# Development
git commit -m "Add feature"  # → 1.0.1.dev1+g123abc
git commit -m "Fix bug"      # → 1.0.1.dev2+g456def

# Release
git tag v1.1.0              # → 1.1.0 (clean release)
git push --tags

# Continue development
git commit -m "New feature"  # → 1.1.1.dev1+g789ghi
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


## CI/CD Workflows

This repository implements comprehensive CI/CD pipelines using GitHub Actions:

### Continuous Integration (CI) - Runs on all branches and PRs

| Workflow | File | Triggers | Description |
|----------|------|----------|-------------|
| **Pre-commit** | `ci-pre-commit.yml` | Push, PR | Code quality checks (Ruff, mypy, etc.) |
| **Pytest** | `ci-pytest.yml` | Push to main/develop, PR | Unit tests with coverage + dependency analysis |
| **Security Scan** | `ci-safety-action.yml` | Push, PR, Weekly | Python dependency vulnerability scanning |
| **CodeQL** | `cicd-codeql-analysis.yaml` | PR to main/develop, Scheduled | Semantic code analysis for vulnerabilities |
| **Zizmor** | `cicd-zizmor.yml` | Push to main, PR | GitHub Actions workflow security audit |

### Continuous Deployment (CD) - Runs on releases and main branch

| Workflow | File | Triggers | Description |
|----------|------|----------|-------------|
| **Package Build & Publish** | `cd-py-package.yml` | Release, Push to main, Manual | Builds and publishes to Test PyPI |

### Automated Maintenance

- **Dependabot**: Automated dependency updates (weekly)
- **Pre-commit hooks**: Local code quality enforcement

## Testing the Deployment

This project is configured to deploy to **Test PyPI** (not production PyPI) for demonstration purposes.

### 1. Test Local Package Installation

```bash
# Install the package in development mode
uv pip install -e .

# Test the CLI command
nk-uv-demo
# Expected output: Hello from nk-uv-demo!
```

### 2. Test Package Build

```bash
# Build the package locally
uv build

# Check the built package
ls dist/
# Should show: nk_uv_demo-*.tar.gz and nk_uv_demo-*.whl
```

### 3. Test Deployment to Test PyPI

#### Automatic Deployment (Recommended)

1. **Create a release** on GitHub:
   ```bash
   # List latests tag
   git tag --list

   # Tag a version and push
   git tag v0.1.0
   git push origin v0.1.0

   # Or create a release through GitHub UI
   ```

2. **Monitor the deployment**:
   - Go to Actions tab in GitHub
   - Watch the "Publish | Build and Publish Package to Test PyPI" workflow
   - Check the deployment at: https://test.pypi.org/p/nk-uv-demo/

#### Manual Deployment Testing

1. **Trigger manual deployment**:
   - Go to Actions tab → "Publish | Build and Publish Package to Test PyPI"
   - Click "Run workflow" → Select branch → "Run workflow"

2. **Verify deployment**:
   ```bash
   # Install from Test PyPI (in a fresh environment)
   pip install -i https://test.pypi.org/simple/ nk-uv-demo

   # Test the installed package
   nk-uv-demo
   ```

### 4. Test CI/CD Pipeline

#### Test CI (Code Quality)

```bash
# Create a feature branch
git checkout -b feature/test-deployment

# Make a small change (e.g., update version or add comment)
echo "# Test comment" >> src/nk_uv_demo/__init__.py
git add .
git commit -m "Test CI pipeline"
git push origin feature/test-deployment

# Create PR and watch CI run:
# - Pre-commit checks
# - Pytest with coverage
# - Security scans
```

#### Test CD (Deployment)

```bash
# Merge to main or create a release tag
git checkout main
git merge feature/test-deployment
git push origin main

# Or create a version tag
git tag v0.1.1
git push origin v0.1.1
```

### 5. Monitoring and Verification

- **GitHub Actions**: Monitor workflow runs in the Actions tab
- **Test PyPI**: Check published packages at https://test.pypi.org/p/nk-uv-demo/
- **Security**: Review Dependabot PRs and CodeQL alerts in Security tab
- **Coverage**: Check coverage reports in CI logs

### Notes on Production Deployment

This demo repository is configured for **Test PyPI only**. For production:

1. Uncomment the PyPI environment in `cd-py-package.yml`
2. Set up PyPI trusted publishing in GitHub repository settings
3. Configure production environment secrets
4. Update the repository URL in the workflow
