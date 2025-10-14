# Naturkart uv demo - Python DevOps practices

[![CI](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-quality.yml/badge.svg)](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-quality.yml)
[![Tests](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-test-build.yml/badge.svg)](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-test-build.yml)
[![Security](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/scan-safety.yml/badge.svg)](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/scan-safety.yml)

A demonstration of Python DevOps practices using automated tools and workflows. This repository shows Python project structure, code quality enforcement, security scanning, and CI/CD pipelines.

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

## Project Status

| Check | Status |
|-------|--------|
| **Build** | ![CI](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-quality.yml/badge.svg) |
| **Tests** | ![Tests](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/ci-test-build.yml/badge.svg) |
| **Security** | ![Security](https://github.com/ac-willeke/nk-uv-demo/actions/workflows/scan-safety.yml/badge.svg) |
| **Package** | [Test PyPI](https://test.pypi.org/project/nk-uv-demo/) |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Getting started:** [Installation Guide](docs/getting-started/installation.md)
**Commands:** [Command Cheatsheet](docs/command-cheatsheet.md)
**Need help:** [Troubleshooting](docs/troubleshooting.md)
**Contributing:** [Development Guide](docs/development.md)
