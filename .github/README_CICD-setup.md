# GitHub Actions (GHA) for CI/CD - nk-uv-demo

GitHub Actions workflows automate code quality, security scanning, and dependency management for the Python package `nk-uv-demo`.

**TODO:**
- [ ] Add pytest workflow for testing
- [ ] Add Docker workflow for containerization
- [ ] Add deployment workflow
- [ ] Enable branch protection rules

## Git - GitFlow Release Strategy

Our CI/CD is configured for a **GitFlow release strategy** that prevents publishing development versions:

- **`main`**: Production branch (protected, only clean releases)
- **`develop`**: Integration branch (dev versions only)
- **`release/*`**: Release preparation branches
- **`feature/*`**: Development branches
- **`hotfix/*`**: Emergency fix branches

### Release Workflow:

1. **Feature Development**
   - Create branch: `feature/your-feature` from `develop`
   - Update code and test
   - Run checks locally: `pre-commit run --all-files`
   - Push changes → **CI builds dev package** (no publish)
   - PR to `develop` → merge after review

2. **Release Preparation**
   - Create branch: `release/v1.2.3` from `develop`
   - Update version, docs, changelog
   - Test thoroughly
   - PR to `main` → merge after review

3. **Publishing Release**
   - **Tag creation**: `git tag v1.2.3` (semantic versioning required)
   - **Push tag**: `git push origin v1.2.3`
   - **Automatic publishing**: Only triggered by version tags (v*.*.*)
   - **Version validation**: Workflow ensures clean release versions only

4. **Hotfixes**
   - Create branch: `hotfix/v1.2.4` from `main`
   - Fix issue, update version
   - PR to both `main` and `develop`

### Creating a Release (Step-by-Step)

To publish a package version to Test PyPI:

```bash
# 1. Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# 2. Create and push a semantic version tag
git tag v1.2.3  # Replace with your version
git push origin v1.2.3

# 3. Optionally create a GitHub release (triggers same workflow)
# Go to GitHub → Releases → Create a new release → Select the tag
```

**Important**:
- Only **semantic version tags** (v1.2.3 format) trigger publishing
- The workflow validates that versions are clean (no dev/dirty markers)
- Development versions automatically build but don't publish

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
| CodeQL Analysis | Security | PRs to main/develop, Scheduled | Semantic code analysis for vulnerabilities | `codeql.yml` | Both |
| Zizmor | Security | Push to main, PRs | GitHub Actions workflow security audit | `cicd-zizmor.yml` | Both |
| Dependabot | Security | Scheduled (weekly) | Automated updates for GitHub Actions + Python deps | `dependabot.yaml` | Both |
| **Dev Package Build** | **Build** | **Push to develop/feature/release branches** | **Builds dev packages (no publish)** | **`ci-build-dev.yml`** | **CI** |
| **Test PyPI Release** | **Release** | **Version tags (v\*.\*.\*), GitHub releases** | **Version validation + publish to Test PyPI** | **`cd-upload-test-pypi.yml`** | **CD** |
| Test Build Only | Testing | PRs, manual dispatch | Tests package building without publishing | `ci-test-build-pypi.yml` | CI |
