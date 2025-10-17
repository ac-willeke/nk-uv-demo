# Naturkart uv demo - Python DevOps practices


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TestPyPI](https://img.shields.io/badge/TestPyPI-latest-blue)](https://test.pypi.org/project/nk-uv-demo/)
[![Coverage](https://codecov.io/gh/ac-willeke/nk-uv-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/ac-willeke/nk-uv-demo)
[![Safety](https://img.shields.io/badge/Safety-Dashboard-blue)](https://platform.safetycli.com/codebases/nk-uv-demo/findings)

A demonstration of Python DevOps practices using automated tools and workflows. This repository shows Python project structure, code quality enforcement, security scanning, and CI/CD pipelines.


## Workflow Statuses

| Job | Status | Description |
|---|---|---|
| **CI Python** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/ci-python.yml?branch=main&label=&style=flat) | • Pre-commit hooks (ruff, mypy etc.)<br>• Test coverage with pytest and codecov<br>• Python dependency analysis<br>• Build and test package |
| **CD Python** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/cd-python.yml?label=&style=flat) | • Build Python package (wheel + sdist)<br>• Publish to Test PyPI<br>• Released by git tags or manually in GitHub |
| **Safety Scan** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-safety.yml?branch=main&label=&style=flat) | • Python dependency scan<br>• Results in GitHub Actions log and on the [Safety](https://platform.safetycli.com/codebases/nk-uv-demo/findings) dashboard |
| **CodeQL Analysis** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-codeql.yml?branch=main&label=&style=flat) | • Python and GitHub Actions security analysis<br>• Results in [Security](https://github.com/ac-willeke/nk-uv-demo/security/code-scanning) tab |
| **Zizmor Security** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-zizmor.yml?branch=main&label=&style=flat) | • GitHub Actions security scan<br>• Results in [Security](https://github.com/ac-willeke/nk-uv-demo/security/code-scanning) tab |

In this demo Python packaging and containerization workflows are included. These workflows can be customized or removed based on your specific project requirements. As a minimum we recommend including the CI Python workflow for code quality and testing as well as the Security workflows, CodeQL, Safety, and Zizmor.

## Features

- **Python Tooling** - uv for dependency management
- **Code Quality** - Ruff, mypy, pytest with testing
- **Security** - Security scanning and monitoring
- **CI/CD Pipeline** - Automated testing, building, and deployment
- **Developer Tools** - Pre-commit hooks, VS Code integration, Taskfile automation
- **Documentation** - Guides and implementation details

## Quick Start

### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager
- [Task](https://taskfile.dev/installation/) - Task runner (optional)
- [Git](https://git-scm.com/) and [GitHub](https://github.com/) account

### Setup

```bash
# Clone the repository
gh repo clone ac-willeke/nk-uv-demo
cd nk-uv-demo

# Development setup (installs dependencies, hooks, runs checks)
task dev-setup

# Test the application
task run
# → "Hello from nk-uv-demo!"

# See all available commands
task --list
```

### Key Commands

```bash
task check            # Run all quality checks
task test-html        # Run tests with coverage
task build            # Build Python package
```

For complete command reference, see [Command Cheatsheet](docs/command-cheatsheet.md).

## Tools Included

- **Code Quality:** Ruff (linting/formatting), mypy (type checking), pytest (testing)
- **Security:** Safety, CodeQL, Dependabot, Zizmor
- **CI/CD:** GitHub Actions workflows, automated Test PyPI publishing
- **Developer Tools:** Pre-commit hooks, VS Code integration, Taskfile automation

## Documentation

Documentation is available in the [`docs/`](docs/) directory:

### Getting Started
- **[Requirements](docs/getting-started/requirements.md)** - System requirements and tool installation
- **[Installation](docs/getting-started/installation.md)** - Step-by-step setup guide
- **[Quick Start](docs/getting-started/quickstart.md)** - Get running quickly with Taskfile

### Development
- **[Development Guide](docs/development.md)** - Complete development workflow and tools

### CI/CD
- **[Workflows](docs/ci-cd/workflows.md)** - GitHub Actions CI/CD pipelines
- **[Deployment](docs/ci-cd/deployment.md)** - Package building and publishing

### Reference
- **[Command Cheatsheet](docs/command-cheatsheet.md)** - All commands organized by tool
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## Use Cases

This repository serves as:

- **Project Template** - Starting point for new Python projects
- **Learning Resource** - Study Python DevOps practices
- **Reference Implementation** - See how tools integrate in practice
- **Best Practices Guide** - Follow established patterns and workflows

## Contributing

To contribute:

1. **Setup**: Follow the [Installation Guide](docs/getting-started/installation.md)
2. **Develop**: Read the [Development Overview](docs/development/README.md)
3. **Quality**: Ensure code meets our [quality standards](docs/development/code-quality.md)
4. **Test**: Run tests following our [testing guidelines](docs/development/testing.md)
5. **Submit**: Create a pull request with clear description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Getting started:** [Installation Guide](docs/getting-started/installation.md)
**Commands:** [Command Cheatsheet](docs/command-cheatsheet.md)
**Need help:** [Troubleshooting](docs/troubleshooting.md)
**Contributing:** [Development Guide](docs/development.md)
