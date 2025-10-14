# Security

This document outlines the security practices, tools, and scanning implemented in nk-uv-demo to ensure secure code and dependencies.

## Overview

Security is implemented through multiple layers:

1. **Dependency Scanning**: Automated vulnerability detection in packages
2. **Code Analysis**: Static analysis for security vulnerabilities
3. **Workflow Security**: GitHub Actions security auditing
4. **Automated Updates**: Dependency updates with security patches
5. **Best Practices**: Secure coding guidelines

## Security Tools

### Safety - Python Dependency Vulnerability Scanner

[Safety](https://pypi.org/project/safety/) scans Python dependencies for known security vulnerabilities.

**Configuration**: `.safety-project.ini`

#### Features
- **Real-time Scanning**: Check dependencies against vulnerability databases
- **CI/CD Integration**: Automated scanning in GitHub Actions
- **Detailed Reports**: Vulnerability details with fix recommendations
- **Policy Enforcement**: Fail builds on security issues

#### Setup and Usage

```bash
# First-time setup (requires free Safety account)
uv run safety auth login --headless

# Scan dependencies for vulnerabilities
task security
# or: uv run safety scan

# Check specific requirements file
uv run safety check --file pyproject.toml

# Generate JSON report
uv run safety scan --output json
```

#### Safety Configuration

```ini
# .safety-project.ini
[safety]
full-report = true
ignore_scopes = []  # e.g., ["dev-dependencies"] to ignore dev deps
ignore_vulnerabilities = []  # Ignore specific CVE IDs (after review!)
output = "json"
```

### CodeQL - Semantic Code Analysis

[CodeQL](https://codeql.github.com/) performs semantic analysis to find security vulnerabilities and coding errors.

**Configuration**: `.github/workflows/scan-codeql.yml`

#### Features
- **Deep Analysis**: Understands code structure and data flow
- **Security Queries**: Pre-built queries for common vulnerabilities
- **Custom Queries**: Write custom security rules
- **Sarif Reports**: Standard security report format

#### Covered Vulnerability Types
- SQL Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Command Injection
- Insecure Deserialization
- Hard-coded Credentials
- Weak Cryptography

### Zizmor - GitHub Actions Security Auditing

[Zizmor](https://docs.zizmor.sh/) audits GitHub Actions workflows for security issues.

**Usage**: Scans `.github/workflows/` directory

#### Features
- **Workflow Security**: Analyze GitHub Actions for security risks
- **Permission Analysis**: Check for excessive permissions
- **Secret Handling**: Verify secure secret management
- **Supply Chain**: Validate action sources and versions

#### Usage

```bash
# Scan GitHub Actions workflows
uv run zizmor .github/workflows/

# Scan with verbose output
uv run zizmor --verbose .github/workflows/

# Generate JSON report
uv run zizmor --format json .github/workflows/
```

### Dependabot - Automated Dependency Updates

[Dependabot](https://github.com/dependabot) automatically creates pull requests for dependency updates, including security patches.

**Configuration**: `.github/dependabot.yaml`

#### Features
- **Automated Updates**: Regular dependency updates
- **Security Alerts**: Immediate alerts for vulnerable dependencies
- **Version Compatibility**: Smart version resolution
- **PR Integration**: Automated pull requests with changelogs

#### Configuration Example

```yaml
# .github/dependabot.yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "ac-willeke"
```

## Security Best Practices

### 1. Secure Coding Guidelines

#### Input Validation

```python
# Good: Validate and sanitize inputs
def process_user_input(user_input: str) -> str:
    """Process user input safely."""
    if not isinstance(user_input, str):
        raise TypeError("Input must be a string")

    if len(user_input) > 1000:
        raise ValueError("Input too long")

    # Sanitize input
    sanitized = user_input.strip().replace("<", "&lt;").replace(">", "&gt;")
    return sanitized

# Bad: Direct use without validation
def unsafe_process(user_input):
    return eval(user_input)  # Never do this!
```

#### File Operations

```python
import os
from pathlib import Path

# Good: Secure file handling
def read_user_file(filename: str) -> str:
    """Read file with path validation."""
    # Validate filename
    if ".." in filename or filename.startswith("/"):
        raise ValueError("Invalid filename")

    # Use pathlib for safe path handling
    base_dir = Path(__file__).parent
    file_path = base_dir / "data" / filename

    # Ensure file is within expected directory
    if not str(file_path).startswith(str(base_dir)):
        raise ValueError("Path traversal attempt")

    return file_path.read_text()

# Bad: Direct file access
def unsafe_read(filename):
    with open(filename) as f:  # Vulnerable to path traversal
        return f.read()
```

#### Environment Variables

```python
import os
from typing import Optional

# Good: Secure environment variable handling
def get_database_url() -> str:
    """Get database URL from environment."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    # Validate URL format
    if not db_url.startswith(("postgresql://", "sqlite://")):
        raise ValueError("Invalid database URL format")

    return db_url

# Good: Default values for non-sensitive config
def get_debug_mode() -> bool:
    """Get debug mode setting."""
    return os.getenv("DEBUG", "false").lower() == "true"

# Bad: Hard-coded secrets
```

### 2. Dependency Management

#### Pin Dependency Versions

```toml
# pyproject.toml - Good: Specify version constraints
[project]
dependencies = [
    "requests>=2.31.0,<3.0.0",  # Secure version range
    "cryptography>=41.0.0",     # Latest security patches
]

[dependency-groups]
dev = [
    "pytest>=7.4.0,<8.0.0",
    "safety>=3.0.0",           # Security scanning tool
]
```

#### Regular Updates

```bash
# Check for outdated dependencies
uv pip list --outdated

# Update dependencies (review changes first)
uv lock --upgrade

# Scan for vulnerabilities after updates
task security
```

### 3. Secret Management

#### Environment Variables (Recommended)

```python
# Good: Use environment variables for secrets
import os

def get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable required")
    return api_key
```

#### GitHub Secrets

For CI/CD, use GitHub repository secrets:

```yaml
# .github/workflows/deploy.yml
- name: Deploy with secret
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    echo "Deploying with API key"
```

#### What NOT to do

- never commit secrets to code
- never add secrets to log messages
- never add secrets to error messages.

## Security Scanning Workflow

### Local Development

```bash
# Run all security scans
task security

# Individual scans
uv run safety scan                    # Dependency vulnerabilities
uv run zizmor .github/workflows/     # Workflow security
task deps-check                      # Dependency analysis

# Before committing
task ci-local                        # Full quality + security check
```

### CI/CD Integration

Security scans run automatically:

1. **On Every Push/PR**: Safety dependency scanning
2. **On PR to Main**: CodeQL security analysis
3. **Weekly**: Dependabot dependency updates
4. **On Workflow Changes**: Zizmor workflow auditing

### Security Report Review

```bash
# Generate detailed security reports
uv run safety scan --output json > security-report.json
uv run zizmor --format json .github/workflows/ > workflow-security.json

# Review reports for:
# - Critical/High severity vulnerabilities
# - Outdated packages with known issues
# - Workflow permission issues
# - Excessive GitHub Actions permissions
```

## Security Incident Response

### If Vulnerability Found

1. **Assess Impact**: Determine severity and affected components
2. **Create Issue**: Document the vulnerability privately
3. **Fix Immediately**: Update dependencies or patch code
4. **Test Fix**: Ensure fix doesn't break functionality
5. **Deploy**: Release security update
6. **Notify**: Inform users if necessary

### Example Response Workflow

```bash
# 1. Update vulnerable dependency
uv add "requests>=2.31.0"  # Fix for CVE-XXXX-XXXX

# 2. Verify fix
task security  # Should show no vulnerabilities

# 3. Test functionality
task test

# 4. Commit and deploy
git add .
git commit -m "security: update requests to fix CVE-XXXX-XXXX"
git push origin main
```

## Security Configuration

### Safety Configuration

```ini
# .safety-project.ini
[safety]
# Full report with details
full-report = true

# Scopes to ignore (use carefully)
ignore_scopes = []

# Specific vulnerabilities to ignore (document reasons!)
ignore_vulnerabilities = [
    # "12345",  # Example: False positive in test dependency
]

# Output format
output = "json"
```

### CodeQL Configuration

```yaml
# .github/workflows/scan-codeql.yml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: python
    queries: security-extended  # Use extended security queries
```

### Pre-commit Security Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: zizmor
        name: Zizmor workflow security scan
        entry: uv run zizmor
        language: system
        files: ^\.github/workflows/.*\.ya?ml$
        pass_filenames: false
        args: ['.github/workflows/']
```

## Monitoring and Alerts

### GitHub Security Features

Enable in repository settings:
- **Dependabot alerts**: Automatic vulnerability notifications
- **Secret scanning**: Detect committed secrets
- **Code scanning**: CodeQL integration
- **Security advisories**: Publish security updates

### Regular Security Reviews

Schedule regular reviews:
- **Weekly**: Review Dependabot PRs
- **Monthly**: Full security audit with all tools
- **Quarterly**: Review and update security policies
- **On Release**: Complete security scan before deployment

## Security Resources

### Documentation
- [OWASP Python Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)
- [Python Security Best Practices](https://python.org/dev/security/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

### Tools Documentation
- [Safety Documentation](https://pyup.io/safety/)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Zizmor Documentation](https://docs.zizmor.sh/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

---

**Next Steps**: Learn about [Pre-commit Hooks](pre-commit.md) to automate security and quality checks.
