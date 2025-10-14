# CI/CD Workflows

This document explains the Continuous Integration and Continuous Deployment (CI/CD) workflows implemented in nk-uv-demo using GitHub Actions.

## Overview

The CI/CD pipeline ensures code quality, security, and reliable deployments through automated workflows:

- **Continuous Integration (CI)**: Automated testing and quality checks on every push/PR
- **Continuous Deployment (CD)**: Automated package building and publishing
- **Security Scanning**: Regular vulnerability assessment
- **Automated Maintenance**: Dependency updates and workflow auditing

## Workflow Architecture

### CI Workflows (Quality Assurance)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Quality Checks** | `ci-quality.yml` | Push, PR | Code formatting, linting, type checking |
| **Testing** | `ci-test-build.yml` | Push to main/develop, PR | Unit tests, coverage, dependency analysis |
| **Security Scan** | `scan-safety.yml` | Push, PR, Weekly | Python dependency vulnerability scanning |
| **CodeQL Analysis** | `scan-codeql.yml` | PR to main/develop, Scheduled | Semantic code security analysis |
| **Workflow Security** | `scan-zizmor.yml` | Push to main, PR | GitHub Actions workflow auditing |

### CD Workflows (Deployment)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Package Publishing** | `cd-publish-testpypi.yml` | Release, Push to main, Manual | Build and publish to Test PyPI |

### Maintenance Workflows

| Tool | Configuration | Schedule | Purpose |
|------|--------------|----------|---------|
| **Dependabot** | `dependabot.yaml` | Weekly | Automated dependency updates |
| **Pre-commit Updates** | `ci-quality.yml` | Weekly | Pre-commit hook updates |

## Detailed Workflow Descriptions

### 1. Quality Checks Workflow

**File**: `.github/workflows/ci-quality.yml`

**Purpose**: Ensures code quality standards on every push and pull request.

```yaml
name: CI | Quality Checks

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - uses: pre-commit/action@v3.0.1
```

**What it does**:
- Runs all pre-commit hooks (Ruff, mypy, file checks)
- Validates code formatting and style
- Performs type checking
- Checks YAML/TOML syntax
- Scans workflow files for security issues

### 2. Testing and Build Workflow

**File**: `.github/workflows/ci-test-build.yml`

**Purpose**: Comprehensive testing with coverage analysis and dependency validation.

```yaml
name: CI | Test and Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
        os: [ubuntu-latest, windows-latest, macos-latest]

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync
      - name: Run tests with coverage
        run: uv run pytest --cov --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
      - name: Check dependencies
        run: uv run deptry .
```

**What it does**:
- Tests on multiple Python versions (3.12, 3.13)
- Tests on multiple operating systems (Ubuntu, Windows, macOS)
- Runs complete test suite with coverage
- Uploads coverage reports to Codecov
- Analyzes dependencies for issues
- Validates package can be built

### 3. Security Scanning Workflows

#### Safety - Dependency Vulnerability Scanning

**File**: `.github/workflows/scan-safety.yml`

```yaml
name: Security | Safety Scan

on:
  push:
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Mondays

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync
      - name: Run Safety scan
        env:
          SAFETY_API_KEY: ${{ secrets.SAFETY_API_KEY }}
        run: uv run safety scan --output json
```

#### CodeQL - Semantic Code Analysis

**File**: `.github/workflows/scan-codeql.yml`

```yaml
name: Security | CodeQL Analysis

on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 6 * * 2'  # Weekly on Tuesdays

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-extended
      - uses: github/codeql-action/analyze@v3
```

#### Zizmor - Workflow Security Auditing

**File**: `.github/workflows/scan-zizmor.yml`

```yaml
name: Security | Workflow Audit

on:
  push:
    branches: [main]
    paths: ['.github/workflows/**']
  pull_request:
    paths: ['.github/workflows/**']

jobs:
  zizmor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install zizmor
        run: uv tool install zizmor
      - name: Run zizmor
        run: uv tool run zizmor .github/workflows/
```

### 4. Package Publishing Workflow

**File**: `.github/workflows/cd-publish-testpypi.yml`

**Purpose**: Builds and publishes the Python package to Test PyPI.

```yaml
name: CD | Publish to Test PyPI

on:
  release:
    types: [published]
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for setuptools-scm
      - uses: astral-sh/setup-uv@v3
      - name: Build package
        run: uv build
      - name: Publish to Test PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/
```

## Workflow Triggers

### Push Triggers

```yaml
on:
  push:
    branches: [main, develop]     # Quality checks on main branches
    paths: ['.github/workflows/**']  # Security scan on workflow changes
```

### Pull Request Triggers

```yaml
on:
  pull_request:
    branches: [main, develop]     # All CI checks on PRs
    paths: ['src/**', 'tests/**'] # Only when code changes
```

### Scheduled Triggers

```yaml
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly security scans
    - cron: '0 2 * * *'  # Daily dependency checks
```

### Manual Triggers

```yaml
on:
  workflow_dispatch:  # Allow manual triggering
    inputs:
      environment:
        description: 'Deployment environment'
        required: false
        default: 'test'
```

## Environment Configuration

### Repository Secrets

Configure these secrets in GitHub repository settings:

| Secret | Purpose | Required For |
|--------|---------|--------------|
| `SAFETY_API_KEY` | Safety vulnerability scanning | Security workflows |
| `CODECOV_TOKEN` | Coverage report uploads | Test workflows |

### Environment Variables

```yaml
env:
  PYTHON_VERSION: "3.12"
  UV_CACHE_DIR: /tmp/.uv-cache
  SAFETY_API_KEY: ${{ secrets.SAFETY_API_KEY }}
```

### Permissions

```yaml
permissions:
  contents: read          # Read repository contents
  security-events: write  # Upload security scan results
  id-token: write        # OIDC token for PyPI publishing
  pull-requests: write   # Comment on PRs with results
```

## Quality Gates and Branch Protection

### Branch Protection Rules

Configure in GitHub repository settings:

```yaml
# Require these checks before merging to main
required_status_checks:
  - "CI | Quality Checks / pre-commit"
  - "CI | Test and Build / test (3.12, ubuntu-latest)"
  - "CI | Test and Build / test (3.13, ubuntu-latest)"
  - "Security | Safety Scan / security"

# Additional protection rules
dismiss_stale_reviews: true
require_code_owner_reviews: true
require_up_to_date_branch: true
```

### Quality Thresholds

Workflows fail if these thresholds are not met:

| Check | Threshold | Enforced By |
|-------|-----------|-------------|
| **Test Coverage** | >80% | pytest-cov |
| **Security Issues** | 0 critical/high | Safety, CodeQL |
| **Code Quality** | 0 errors | Ruff, mypy |
| **Type Coverage** | 100% | mypy --strict |

## Local CI Simulation

Test CI workflows locally before pushing:

```bash
# Simulate full CI pipeline
task ci-local

# This runs:
# 1. Pre-commit hooks (formatting, linting, type checking)
# 2. Full test suite with coverage
# 3. Dependency analysis
# 4. Package building
# 5. Security scanning (if configured)

# Individual CI steps
task check          # Quality checks
task test-html      # Testing with coverage
task security       # Security scans
task build          # Package building
```

## Monitoring and Notifications

### GitHub Actions Dashboard

Monitor workflow runs:
- **Actions Tab**: View all workflow runs and results
- **Status Badges**: Add badges to README for build status
- **Email Notifications**: Automatic notifications on failures

### Status Badges

Add to README.md:

```markdown
![CI](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-quality.yml/badge.svg)
![Tests](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-test-build.yml/badge.svg)
![Security](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/scan-safety.yml/badge.svg)
[![codecov](https://codecov.io/gh/ac-willeke/nk-uv-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/ac-willeke/nk-uv-demo)
```

### Failure Notifications

Configure notifications in repository settings:
- **Email**: On workflow failures
- **Slack/Teams**: Integration with team communication tools
- **GitHub Mobile**: Push notifications for critical issues

## Deployment Process

### Test PyPI Deployment

1. **Automatic**: Triggered on releases and main branch pushes
2. **Manual**: Use workflow_dispatch for on-demand deployment
3. **Verification**: Automated testing of deployed package

```bash
# Test deployed package
pip install -i https://test.pypi.org/simple/ nk-uv-demo
nk-uv-demo  # Should work
```

### Release Process

1. **Update Version**: Use setuptools-scm (automatic from git tags)
2. **Create Release**: GitHub release triggers deployment
3. **Verify Deployment**: Check Test PyPI and run integration tests

```bash
# Create and push release tag
git tag v1.0.0
git push origin v1.0.0

# Or create release through GitHub UI
# This automatically triggers the CD workflow
```

## Troubleshooting CI/CD Issues

### Common Workflow Failures

#### Dependency Installation Issues

```bash
# Local debugging
uv lock --upgrade
uv sync
task check  # Verify everything works locally
```

#### Test Failures

```bash
# Run tests with verbose output
task test-html
# Check htmlcov/index.html for coverage details

# Debug specific failing tests
uv run pytest tests/test_specific.py -v
```

#### Security Scan Failures

```bash
# Check for vulnerabilities locally
task security

# Review and update dependencies
uv add "package>=secure.version"
```

#### Build Failures

```bash
# Test package building locally
task build
ls dist/  # Should contain .tar.gz and .whl files

# Test installation
pip install dist/*.whl
```

### Workflow Debugging

```yaml
# Add debug steps to workflows
- name: Debug information
  run: |
    echo "Python version: $(python --version)"
    echo "uv version: $(uv --version)"
    echo "Working directory: $(pwd)"
    echo "Files: $(ls -la)"

- name: Environment info
  run: env | sort
```

### Performance Optimization

```yaml
# Cache dependencies between runs
- name: Cache uv
  uses: actions/cache@v4
  with:
    path: /tmp/.uv-cache
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}

# Use matrix strategy for parallel execution
strategy:
  matrix:
    python-version: ["3.12", "3.13"]
    os: [ubuntu-latest, windows-latest]
```

## Advanced CI/CD Features

### Conditional Workflows

```yaml
# Only run on specific file changes
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'

# Skip CI on certain commits
if: "!contains(github.event.head_commit.message, '[skip ci]')"
```

### Parallel Job Execution

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    # ... quality checks

  security:
    runs-on: ubuntu-latest
    # ... security scans

  deploy:
    needs: [quality, security]  # Wait for both to complete
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    # ... deployment steps
```

### Multi-environment Deployment

```yaml
strategy:
  matrix:
    environment: [test, staging]
    include:
      - environment: test
        python-version: "3.12"
      - environment: staging
        python-version: "3.13"
```

---

**Next Steps**: Learn about [Deployment](deployment.md) for detailed deployment procedures and testing.
