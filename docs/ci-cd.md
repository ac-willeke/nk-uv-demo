# CI/CD Guide

This guide covers Continuous Integration and Continuous Deployment workflows using GitHub Actions.

## Overview

The CI/CD pipeline provides:
- **Continuous Integration (CI)** - Automated testing and quality checks
- **Continuous Deployment (CD)** - Automated package building and publishing
- **Security Scanning** - Regular vulnerability assessment
- **Automated Maintenance** - Dependency updates and workflow auditing

For commands, see [Command Cheatsheet](../command-cheatsheet.md#github-actions-commands).

## Workflows

### CI Workflows (Quality Assurance)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Quality Checks** | `ci-quality.yml` | Push, PR | Pre-commit hooks, formatting, linting |
| **Testing** | `ci-test-build.yml` | Push to main, PR | Tests, coverage, dependency analysis |
| **Security Scan** | `scan-safety.yml` | Push, PR, Weekly | Dependency vulnerability scanning |
| **CodeQL Analysis** | `scan-codeql.yml` | PR to main/develop, Scheduled | Semantic code security analysis |
| **Workflow Security** | `scan-zizmor.yml` | Push to main, PR | GitHub Actions workflow auditing |

### CD Workflows (Deployment)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Package Publishing** | `cd-publish-testpypi.yml` | Release, Push to main, Manual | Build and publish to Test PyPI |

### Maintenance

| Tool | Configuration | Schedule | Purpose |
|------|--------------|----------|---------|
| **Dependabot** | `dependabot.yaml` | Weekly | Automated dependency updates |

## Workflow Details

### Quality Checks
- **Triggers:** Every push and PR
- **Runs:** All pre-commit hooks (Ruff, mypy, file checks, security scans)
- **Purpose:** Ensure code quality standards

### Testing and Build
- **Triggers:** Push to main/develop branches, all PRs
- **Matrix:** Multiple Python versions (3.12, 3.13) and OS (Ubuntu, Windows, macOS)
- **Steps:** Install dependencies, run tests with coverage, check dependencies, upload coverage
- **Quality Gate:** Must pass for PR merge

### Security Scanning
- **Safety:** Scans Python dependencies for vulnerabilities
- **CodeQL:** Semantic code analysis for security issues
- **Zizmor:** Audits GitHub Actions workflows for security
- **Schedule:** Weekly automated scans

### Package Publishing
- **Target:** Test PyPI (demonstration environment)
- **Authentication:** Trusted publishing (no API keys required)
- **Versioning:** Automatic with setuptools-scm based on git tags
- **Artifacts:** Source distribution (.tar.gz) and wheel (.whl)

## Deployment Process

### Local Development Deployment

**Build Package Locally:**
```bash
# Build package for testing
uv build

# Check what version will be created
uv run python -m setuptools_scm

# Test package installation locally
pip install dist/nk_uv_demo-*.whl
```

**Manual Upload to Test PyPI (Local):**
```bash
# Install twine for uploading
uv add --group dev twine

# Build package
uv build

# Upload to Test PyPI (requires account and API token)
uv run twine upload --repository testpypi dist/*
```

### CI/CD Automated Deployment

**Method 1: Git Tag Release**
```bash
# Create and push version tag
git tag v1.6.0 -m "Release v1.6.0 - New features and fixes"
git push origin v1.6.0    # Triggers CD workflow automatically
```

**Method 2: GitHub Release**
1. Go to GitHub repository → Releases → "Create a new release"
2. Choose a tag (e.g., `v1.6.0`) or create new tag
3. Fill release notes and click "Publish release"
4. CD workflow triggers automatically

**Method 3: Manual Workflow Dispatch**
1. Go to GitHub → Actions → "CD | Python Build and Publish"
2. Click "Run workflow" → Select branch → Run
3. Choose deployment target (testpypi only for this demo)

### Deployment Triggers

| Method | Trigger | When to Use |
|--------|---------|-------------|
| **Git Tags** | Push tags matching `v*.*.*` | Automated releases from command line |
| **GitHub Releases** | Publishing a release | Releases with notes and changelogs |
| **Manual Dispatch** | GitHub Actions UI | Testing, hotfixes, or manual control |
| **Local Build** | `uv build` locally | Development testing and validation |

### Version Management

**setuptools-scm Automatic Versioning:**
- **Clean tag:** `v1.6.0` → Package version: `1.6.0` ✅ **Publishes**
- **After tag:** `v1.6.0-3-gabc123-dirty` → Package version: `1.6.1.dev3+gabc123.d20241017` ❌ **No publish**
- **Development:** Commits without tags → Development versions ❌ **No publish**

**Check Current Version:**
```bash
# Git tag status
git describe --tags --dirty --always

# Package version that would be built
uv run python -m setuptools_scm

# Current installed package version
uv run python -c "import nk_uv_demo; print(nk_uv_demo.__version__)"
```

### Testing Deployment

**After CI/CD Deployment:**
```bash
# Install from Test PyPI
pip install -i https://test.pypi.org/simple/ nk-uv-demo

# Test package works
nk-uv-demo    # Should output: Hello from nk-uv-demo!

# Check version matches tag
python -c "import nk_uv_demo; print(nk_uv_demo.__version__)"
```

**After Local Build:**
```bash
# Install local wheel
pip install dist/nk_uv_demo-*.whl

# Test functionality
nk-uv-demo
```

## Quality Gates and Branch Protection

### Branch Protection Rules
Configure in repository settings:
- Require status checks: CI workflows must pass
- Require code owner reviews
- Require up-to-date branches
- Dismiss stale reviews

### Quality Thresholds
| Check | Threshold | Tool |
|-------|-----------|------|
| **Test Coverage** | >80% | pytest-cov |
| **Security Issues** | 0 critical/high | Safety, CodeQL |
| **Code Quality** | 0 errors | Ruff, mypy |
| **Dependencies** | 0 issues | Deptry |

## Deployment Environments

### Test PyPI (Current Setup)
- **Purpose:** Testing and demonstration environment
- **URL:** https://test.pypi.org/project/nk-uv-demo/
- **Authentication:** GitHub OIDC trusted publishing (no API keys)
- **Retention:** Packages may be deleted after 90 days of inactivity
- **Installation:** `pip install -i https://test.pypi.org/simple/ nk-uv-demo`

### Production PyPI (Future Setup)
To deploy to production PyPI:
1. Configure trusted publishing for PyPI (not TestPyPI)
2. Update workflow `repository-url` setting
3. Add production environment protection rules
4. Set up production-specific quality gates

```yaml
# For production PyPI deployment
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@v1
  # Remove repository-url for production PyPI
```

## Environment Configuration

### Repository Secrets
Configure in GitHub repository settings:
| Secret | Purpose | Used By |
|--------|---------|---------|
| `SAFETY_API_KEY` | Safety vulnerability scanning | Security workflows |
| `CODECOV_TOKEN` | Coverage report uploads | Test workflows |

### Local Development Secrets
For local publishing (optional):
```bash
# Create ~/.pypirc for local uploads
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <TestPyPI API token>

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <PyPI API token>
```

### Permissions
Workflows use minimal required permissions:
- **contents: read** - Read repository contents
- **security-events: write** - Upload security scan results
- **id-token: write** - OIDC token for PyPI publishing

## Local CI Simulation

Test workflows locally before pushing:
```bash
task ci-local    # Simulate full CI pipeline
```

This runs the same checks as CI:
1. Pre-commit hooks
2. Full test suite with coverage
3. Dependency analysis
4. Package building
5. Security scanning

## Monitoring and Status

### Status Badges
Add to README for build status visibility:
```markdown
![CI](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-quality.yml/badge.svg)
![Tests](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-test-build.yml/badge.svg)
```

### Monitoring Locations
- **Actions Tab:** View all workflow runs
- **Security Tab:** CodeQL alerts and Dependabot PRs
- **Test PyPI:** Published packages at https://test.pypi.org/project/nk-uv-demo/
- **Email Notifications:** Automatic on workflow failures

## Troubleshooting

### Common Workflow Failures

**Dependency Installation Issues:**
```bash
uv lock --upgrade    # Update lock file locally
uv sync              # Test locally first
```

**Test Failures:**
```bash
task test-html       # Run tests with coverage locally
# Fix issues, then commit
```

**Security Scan Failures:**
```bash
task security        # Run security scans locally
uv add "package>=secure.version"  # Update vulnerable packages
```

**Build Failures:**
```bash
task build           # Test package building locally
uv run python -m setuptools_scm  # Check version detection
```

**Deployment Failures:**
```bash
# Check version calculation
git describe --tags --dirty --always
uv run python -m setuptools_scm

# Verify clean git state
git status

# Test local build
uv build && ls -la dist/

# Verify tag format
git tag --list | grep -E "^v[0-9]+\.[0-9]+\.[0-9]+$"
```

**Version Synchronization Issues:**
```bash
# Remove stale version files
rm -f src/nk_uv_demo/_version.py

# Force reinstall to refresh version
uv pip install -e . --force-reinstall

# Verify version consistency
uv run python -c "import nk_uv_demo; print(nk_uv_demo.__version__)"
```

### Workflow Debugging
- Check workflow logs in GitHub Actions tab
- Use `task ci-local` to reproduce issues locally
- Clear workflow caches if needed (GitHub repository settings)
- For deployment issues, check the "CD | Python Build and Publish" workflow logs

## Production Deployment (Future)

To deploy to production PyPI:
1. Update workflow to remove `repository-url` (defaults to PyPI)
2. Configure trusted publishing for production PyPI
3. Set up production environment protection rules
4. Add production-specific quality gates

## Configuration Files

### Workflow Files Location
All workflows in `.github/workflows/`:
- `ci-quality.yml` - Quality checks
- `ci-test-build.yml` - Testing and building
- `scan-safety.yml` - Security scanning
- `scan-codeql.yml` - Code analysis
- `scan-zizmor.yml` - Workflow security
- `cd-publish-testpypi.yml` - Package publishing

### Dependabot Configuration
File: `.github/dependabot.yaml`
- **Schedule:** Weekly dependency updates
- **Scope:** Python packages in pyproject.toml
- **Auto-merge:** Manual review required
