# GitHub Actions (GHA) for CI/CD - nk-uv-demo

GitHub Actions workflows automate code quality, security scanning, and dependency management for the Python package `nk-uv-demo`.

**TODO:**
- [ ] Add pytest workflow for testing
- [ ] Add Docker workflow for containerization
- [ ] Add deployment workflow
- [ ] Enable branch protection rules

## Git - Feature Branch Workflow

Our CI/CD is configured for a **feature branch workflow**:

- **`main`**: Production branch (protected)
- **`develop`**: Integration branch
- **`feature/*`**: Development branches

### Workflow:

1. **Feature Development**
   - Create branch: `feature/your-feature`
   - Update code
   - Run checks locally: `pre-commit run --all-files`
   - Push changes → **CI runs** (pre-commit, security scans)

2. **Pull Request to `main`**
   - All CI checks must pass
   - Code review required
   - Security scans must pass

3. **Merge to `main`**
   - Triggers production workflows
   - Creates releases (when configured)

### Branch Protection (Recommended Setup)

- **`main` branch**:
  - Requires PR review
  - All CI checks must pass
  - No direct pushes allowed
  - Up-to-date branch required

## GitHub Actions Workflows

### Workflow Details

#### CI (Testing) - Runs on feature branches and PRs

- **R CMD Check**: Cross-platform package validation
- **Linting**: Code style and quality enforcement
- **Docker CI**: Container build verification and functionality tests

#### CD (Deployment) - Runs on main branch only

- **Docker CD**: Builds and publishes production images to `ghcr.io/ac-willeke/rgaupe`

<br>

### Workflows

| Workflow | Type | Trigger | Description | Filename | CI/CD |
|----------|------|---------|-------------|----------|-------|
| Pre-commit | Code Quality | Push to main, PRs | Runs all pre-commit hooks (Ruff, mypy, etc.) | `ci-pre-commit.yml` | CI |
| Pytests | Testing | Push to main/develop, PRs | Pytest with coverage + deptry dependency check | `ci-pytest.yml` | CI |
| Security Scan | Security | Push (not main), PRs, Weekly | Python dependency vulnerability scanning (uv-native) | `ci-safety-action.yml` | CI |
| CodeQL Analysis | Security | PRs to main/develop, Scheduled | Semantic code analysis for vulnerabilities | `cicd-codeql-analysis.yaml` | Both |
| Zizmor | Security | Push to main, PRs | GitHub Actions workflow security audit | `cicd-zizmor.yml` | Both |
| Dependabot | Security | Scheduled (weekly) | Automated updates for GitHub Actions + Python deps | `dependabot.yaml` | Both |
| Automated Package Release | Release | Push to main (tags) | Automatically creates GitHub releases and changelogs | `cd-release.yml` | CD |
| Package Deployment to PyPI | Deployment | Release creation | Builds and publishes Python package to PyPI | `cd-pypi-publish.yml` | CD |
| Container Building/Publishing | Deployment | Push to main, Release | Builds and publishes Docker images to registry | `cd-docker-publish.yml` | CD |
