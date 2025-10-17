# UV demo - Python DevOps practices

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![TestPyPI](https://img.shields.io/badge/TestPyPI-latest-blue)](https://test.pypi.org/project/nk-uv-demo/) [![Coverage](https://codecov.io/gh/ac-willeke/nk-uv-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/ac-willeke/nk-uv-demo) [![Safety](https://img.shields.io/badge/Safety-Dashboard-blue)](https://platform.safetycli.com/codebases/nk-uv-demo/findings)

This repository demonstrates best practices for Python project development and packaging. It showcases how to structure a Python project, manage dependencies with uv, setup security scanning and CI/CD pipelines using GitHub Actions and containerize code with Docker.

### Features

- **Python Tools**: uv for dependency management, setuptools-scm for dynamic versioning.
- **GitHub Action** workflows for **CI/CD**:
    - **Code Quality** with pre-commit, ruff, mypy and pytest.
    - **Security scanning** with Safety, CodeQL, Dependabot and Zizmor.
    - **Python** deployment to Test PyPI
    - **Container** deployment to GitHub Container Registry (ghcr.io).
- **Developer Tools**: Pre-commit hooks, Development containers, VS Code integration, Taskfile automation

## Workflow Statuses

| Job | Status | Description |
|---|---|---|
| **CI Python** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/ci-python.yml?branch=main&label=&style=flat) | • Pre-commit hooks (ruff, mypy etc.)<br>• Test coverage with pytest and codecov<br>• Python dependency analysis<br>• Build and test package |
| **CD Python** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/cd-python.yml?label=&style=flat) | • Build Python package (wheel + sdist)<br>• Publish to Test PyPI<br>• Released by git tags or manually in GitHub |
| **Safety Scan** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-safety.yml?branch=main&label=&style=flat) | • Python dependency scan<br>• Results in GitHub Actions log and on the [Safety](https://platform.safetycli.com/codebases/nk-uv-demo/findings) dashboard |
| **CodeQL Analysis** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-codeql.yml?branch=main&label=&style=flat) | • Python and GitHub Actions security analysis<br>• Results in [Security](https://github.com/ac-willeke/nk-uv-demo/security/code-scanning) tab |
| **Zizmor Security** | ![Status](https://img.shields.io/github/actions/workflow/status/ac-willeke/nk-uv-demo/scan-zizmor.yml?branch=main&label=&style=flat) | • GitHub Actions security scan<br>• Results in [Security](https://github.com/ac-willeke/nk-uv-demo/security/code-scanning) tab |

In this demo Python packaging and containerization workflows are included. These workflows can be customized or removed based on your specific project requirements. As a minimum we recommend including the CI Python workflow for code quality and testing as well as the Security workflows, CodeQL, Safety, and Zizmor.

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Git](https://git-scm.com/), [GitHub](https://github.com/) account, and [GitHub CLI](https://cli.github.com/)
- [Task](https://taskfile.dev/installation/)
- [Docker](https://docs.docker.com/engine/install/) (optional)
- [VS Code](https://code.visualstudio.com/) (optional)

### Setup

Task is used to automate common development tasks *(see [Taskfile.yml](Taskfile.yml))*. To setup the project without Task you can follow the instructions in the [Installation Guide](docs/getting-started/installation.md).

```bash
# Clone the repository
gh repo clone ac-willeke/nk-uv-demo
cd nk-uv-demo

# Development setup (installs dependencies, hooks, runs checks)
task dev-setup

# Test the application
task run
# → "Hello from nk-uv-demo!"
# → "Version: xxxx"

# See all available commands
task --list
```

### Contributing

To contribute:

1. **Setup**: Follow the Setup instructions above
2. **Develop**:
    - Create a branch for your feature or bugfix
    - Make your changes
    - Ensure code meets the quality standards by running `task check`
3. **Integrate**:
    - Check that all ci-tests pass locally with `task ci-local`
    - Push your branch to GitHub
    - Create a pull request against the `develop` branch
    - Await review and merge, your branch will be automatically deleted after merging.
4. **Deploy**:
    - Create a git tag for releases (e.g., `v0.1.0`) using `task tag`
    - Create a PR from `develop` to `main` to deploy the new release
    - Once merged to `main`, the CD workflows are triggered.
        - CD Python automatically builds and publishes the package to Test PyPI
        - CD Docker builds and pushes the container image to GitHub Container Registry
    - **NOTE**: ensure to merge back `main` into `develop` after releases to keep branches in sync.





### Key Commands

```bash
task check            # Run all quality checks (ruff, mypy, pytest, deptry)
task format lint-fix  # Format and lint code with ruff
task security         # Run security scans (safety, zizmor)
task build            # Build Python package
task tag              # Prepare a new release (create git tag)
```

For complete command reference, see [Command Cheatsheet](docs/command-cheatsheet.md).

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

## Acknowledgements

This demo project leverages the following tools and best practices from the Python and DevOps communities:

- **Development practices** inspired by Eric Riddochs course [Taking Python to Production](https://www.udemy.com/course/setting-up-the-linux-terminal-for-software-development/) and Marvelous MLOps course [MLOps with Databricks: Free Edition](https://www.youtube.com/results?search_query=marvelous+mlops).
- **Docker setup** based on astral-sh Docker example [astral-sh/uv-docker-example](https://github.com/astral-sh/uv-docker-example)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
