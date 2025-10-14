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
| **Testing** | `ci-test-build.yml` | Push to main/develop, PR | Tests, coverage, dependency analysis |
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

### Automated Deployment

**Release Deployment:**
```bash
git tag v1.0.0
git push origin v1.0.0    # Triggers deployment workflow
```

**Main Branch Deployment:**
Every push to `main` automatically deploys to Test PyPI.

**Manual Deployment:**
Use GitHub Actions UI → "CD | Publish to Test PyPI" → "Run workflow"

### Version Management
Uses setuptools-scm for automatic versioning:
- **Development:** `1.0.1.dev1+g123abc` (commits after tag)
- **Release:** `1.0.0` (clean tagged version)

### Testing Deployment
After deployment, verify package:
```bash
pip install -i https://test.pypi.org/simple/ nk-uv-demo
nk-uv-demo    # Should output: Hello from nk-uv-demo!
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

## Environment Configuration

### Repository Secrets
Configure in GitHub repository settings:
| Secret | Purpose | Used By |
|--------|---------|---------|
| `SAFETY_API_KEY` | Safety vulnerability scanning | Security workflows |
| `CODECOV_TOKEN` | Coverage report uploads | Test workflows |

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

### Workflow Debugging
- Check workflow logs in GitHub Actions tab
- Use `task ci-local` to reproduce issues locally
- Clear workflow caches if needed (GitHub repository settings)

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
