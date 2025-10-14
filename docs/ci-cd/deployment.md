# Deployment

This document covers the deployment process, testing procedures, and management of the nk-uv-demo package.

## Overview

The deployment strategy focuses on **Test PyPI** for demonstration purposes, providing a safe environment to showcase CI/CD practices without affecting production systems.

## Deployment Targets

### Test PyPI (Primary)

- **Purpose**: Demonstration and testing environment
- **URL**: https://test.pypi.org/project/nk-uv-demo/
- **Access**: Public, safe for experimentation
- **Retention**: Packages may be removed periodically

### Production PyPI (Future)

- **Purpose**: Real package distribution (if needed)
- **URL**: https://pypi.org/
- **Access**: Requires production configuration
- **Setup**: Commented out in current configuration

## Deployment Methods

### 1. Automated Deployment (Recommended)

Deployments are triggered automatically through GitHub Actions:

#### Release-based Deployment

```bash
# Create a new release tag
git tag v1.0.0
git push origin v1.0.0

# Or create release through GitHub UI:
# 1. Go to Releases tab in GitHub
# 2. Click "Create a new release"
# 3. Choose tag (v1.0.0) and release title
# 4. Click "Publish release"
```

This triggers the `cd-publish-testpypi.yml` workflow which:
1. Checks out the code with full git history
2. Sets up the Python environment with uv
3. Builds the package using `uv build`
4. Publishes to Test PyPI using trusted publishing

#### Main Branch Deployment

```bash
# Push to main branch
git checkout main
git merge feature-branch
git push origin main
```

Every push to `main` automatically deploys to Test PyPI, enabling continuous delivery.

#### Manual Deployment

```bash
# Trigger deployment manually through GitHub Actions:
# 1. Go to Actions tab
# 2. Select "CD | Publish to Test PyPI" workflow
# 3. Click "Run workflow"
# 4. Choose branch and click "Run workflow"
```

### 2. Local Deployment (Development)

For testing the deployment process locally:

```bash
# Build the package
task build
# or: uv build

# Check the built artifacts
ls dist/
# Should show: nk_uv_demo-*.tar.gz and nk_uv_demo-*.whl

# Test local installation
pip install dist/*.whl
nk-uv-demo  # Test the CLI
pip uninstall nk-uv-demo
```

## Version Management

### Automated Versioning with setuptools-scm

The project uses [setuptools-scm](https://setuptools-scm.readthedocs.io/) for automatic version generation based on git tags:

#### Version Scheme

```bash
# Clean release (tagged)
git tag v1.0.0
git push --tags
# → Package version: 1.0.0

# Development versions (post-tag commits)
git commit -m "Add new feature"
# → Package version: 1.0.1.dev1+g123abc

git commit -m "Fix bug"
# → Package version: 1.0.1.dev2+g456def
```

#### Version Commands

```bash
# Check current version
task version
# or: uv run python -m setuptools_scm

# Create and push a new version tag
task tag VERSION=v1.1.0
# This creates and pushes the tag, triggering deployment

# List recent tags
git tag --list --sort=-version:refname | head -10
```

### Version Configuration

**File**: `pyproject.toml`

```toml
[tool.setuptools_scm]
write_to = "src/nk_uv_demo/_version.py"
fallback_version = "0.0.0"
```

This configuration:
- Writes version to `_version.py` file
- Uses `0.0.0` as fallback if no git tags exist
- Generates development versions for uncommitted changes

## Package Building

### Build Process

The build process creates two distribution formats:

```bash
# Build both source and wheel distributions
task build
# or: uv build

# Build specific format
uv build --wheel    # Wheel only (.whl)
uv build --sdist    # Source distribution only (.tar.gz)
```

### Build Artifacts

```bash
dist/
├── nk_uv_demo-1.0.0-py3-none-any.whl    # Wheel distribution
└── nk_uv_demo-1.0.0.tar.gz              # Source distribution
```

#### Wheel Distribution (.whl)
- **Purpose**: Fast installation, pre-built
- **Contains**: Compiled Python bytecode, metadata
- **Best for**: End-user installations

#### Source Distribution (.tar.gz)
- **Purpose**: Source code archive
- **Contains**: Source files, build instructions
- **Best for**: Development, custom builds

### Build Verification

```bash
# Inspect wheel contents
unzip -l dist/nk_uv_demo-*.whl

# Inspect source distribution
tar -tzf dist/nk_uv_demo-*.tar.gz

# Test wheel installation
pip install dist/*.whl --force-reinstall
python -c "import nk_uv_demo; print(nk_uv_demo.__version__)"
```

## Testing Deployment

### 1. Pre-deployment Testing

Before each deployment, run comprehensive tests:

```bash
# Complete local CI simulation
task ci-local

# This includes:
# - Code quality checks
# - Full test suite with coverage
# - Dependency analysis
# - Security scanning
# - Package building
```

### 2. Test PyPI Installation

After deployment, verify the package works correctly:

```bash
# Install from Test PyPI in a clean environment
python -m venv test-env
source test-env/bin/activate  # Linux/macOS
# or: test-env\Scripts\activate  # Windows

# Install the package
pip install -i https://test.pypi.org/simple/ nk-uv-demo

# Test basic functionality
nk-uv-demo
# Expected output: Hello from nk-uv-demo!

# Test programmatic usage
python -c "
import nk_uv_demo
print(f'Version: {nk_uv_demo.__version__}')
print(nk_uv_demo.main())
"

# Clean up
deactivate
rm -rf test-env
```

### 3. Integration Testing

Test package integration in different environments:

```bash
# Test in different Python versions
docker run --rm python:3.12 bash -c "
  pip install -i https://test.pypi.org/simple/ nk-uv-demo &&
  nk-uv-demo
"

docker run --rm python:3.13 bash -c "
  pip install -i https://test.pypi.org/simple/ nk-uv-demo &&
  nk-uv-demo
"
```

## Deployment Configuration

### GitHub Actions Configuration

**File**: `.github/workflows/cd-publish-testpypi.yml`

```yaml
name: CD | Publish to Test PyPI

on:
  release:
    types: [published]    # Trigger on GitHub releases
  push:
    branches: [main]      # Trigger on main branch pushes
  workflow_dispatch:      # Allow manual triggering

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write     # Required for trusted publishing

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full git history for setuptools-scm

      - uses: astral-sh/setup-uv@v3

      - name: Build package
        run: uv build

      - name: Publish to Test PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/
```

### Trusted Publishing Setup

The project uses PyPI's trusted publishing for secure, keyless deployment:

1. **GitHub Repository**: Configured as trusted publisher
2. **OIDC Token**: Automatic authentication via GitHub Actions
3. **No Secrets**: No API keys or passwords needed
4. **Secure**: Enhanced security compared to API tokens

#### Setup Steps

1. Go to [Test PyPI trusted publishers](https://test.pypi.org/manage/account/publishing/)
2. Add GitHub repository: `ac-willeke/nk-uv-demo`
3. Specify workflow: `cd-publish-testpypi.yml`
4. Configure environment (optional): production

## Production Deployment (Future)

To deploy to production PyPI:

### 1. Update Workflow Configuration

```yaml
# Uncomment in cd-publish-testpypi.yml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  # Remove repository-url for production PyPI
```

### 2. Configure Trusted Publishing

1. Go to [PyPI trusted publishers](https://pypi.org/manage/account/publishing/)
2. Add the same repository configuration
3. Update environment to `production` if using environments

### 3. Production Checklist

- [ ] Comprehensive testing on Test PyPI
- [ ] Security review and penetration testing
- [ ] Documentation review and updates
- [ ] License and legal review
- [ ] Backup and rollback procedures
- [ ] Monitoring and alerting setup
- [ ] User communication plan

## Release Process

### Standard Release Workflow

1. **Development Phase**
   ```bash
   # Work on feature branch
   git checkout -b feature/new-feature
   # ... make changes ...
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

2. **Quality Assurance**
   ```bash
   # Create pull request (triggers CI)
   # Review CI results
   # Address any issues
   # Get code review approval
   ```

3. **Integration**
   ```bash
   # Merge to main (triggers deployment to Test PyPI)
   git checkout main
   git merge feature/new-feature
   git push origin main
   ```

4. **Release Creation**
   ```bash
   # Test the deployed package from Test PyPI
   # If satisfied, create official release
   git tag v1.1.0
   git push origin v1.1.0

   # Or use GitHub UI to create release
   ```

5. **Verification**
   ```bash
   # Verify release deployment
   pip install -i https://test.pypi.org/simple/ nk-uv-demo==1.1.0
   nk-uv-demo
   ```

### Hotfix Release Workflow

For critical fixes that need immediate deployment:

```bash
# Create hotfix branch from main
git checkout -b hotfix/critical-fix main

# Make minimal changes
git commit -m "Fix critical security issue"

# Fast-track testing
task ci-local

# Merge to main
git checkout main
git merge hotfix/critical-fix
git push origin main

# Create patch release
git tag v1.0.1
git push origin v1.0.1
```

## Monitoring and Maintenance

### Package Monitoring

- **Test PyPI Dashboard**: Monitor download statistics
- **GitHub Releases**: Track release adoption
- **Issue Tracking**: Monitor bug reports and feature requests
- **Security Alerts**: Watch for vulnerability notifications

### Maintenance Tasks

#### Regular Maintenance
```bash
# Weekly: Update dependencies
uv lock --upgrade
git commit -am "Update dependencies"

# Monthly: Dependency audit
task security
task deps-check
```

#### Annual Maintenance
- Review and update documentation
- Assess tool and dependency choices
- Update CI/CD workflows and actions
- Review security configurations

### Rollback Procedures

If a deployment causes issues:

1. **Immediate**: Remove problematic release from Test PyPI
2. **Communication**: Notify users via GitHub issues/releases
3. **Fix**: Create hotfix and new release
4. **Prevention**: Update CI/CD to catch similar issues

## Troubleshooting Deployment Issues

### Common Deployment Failures

#### Build Failures
```bash
# Check build locally
task build
ls -la dist/

# Common issues:
# - Missing files in package (check MANIFEST.in)
# - Version conflicts (check setuptools-scm)
# - Import errors (check package structure)
```

#### Publishing Failures
```bash
# Check workflow logs in GitHub Actions
# Common issues:
# - Trusted publishing not configured
# - Permission issues (check workflow permissions)
# - Network timeouts (retry workflow)
# - Package already exists (version conflict)
```

#### Installation Failures
```bash
# Test installation locally
pip install -i https://test.pypi.org/simple/ nk-uv-demo

# Common issues:
# - Missing dependencies on Test PyPI
# - Platform compatibility issues
# - Python version incompatibility
```

### Debug Commands

```bash
# Check package metadata
pip show nk-uv-demo

# Inspect package files
pip show -f nk-uv-demo

# Test import paths
python -c "
import nk_uv_demo
print(nk_uv_demo.__file__)
print(nk_uv_demo.__version__)
"

# Check setuptools-scm version detection
uv run python -m setuptools_scm
```

## Security Considerations

### Deployment Security

- **Trusted Publishing**: No long-lived API tokens
- **Minimal Permissions**: Workflow uses least-privilege principle
- **Secure Dependencies**: Regular security scanning
- **Audit Trail**: All deployments logged in GitHub Actions

### Package Security

- **Dependency Scanning**: Automated vulnerability detection
- **Code Analysis**: Static security analysis with CodeQL
- **Supply Chain**: Verified dependencies and build process
- **Provenance**: Clear build and release lineage

---

**Next Steps**: Learn about [Release Process](release-process.md) for detailed procedures on creating and managing releases.
