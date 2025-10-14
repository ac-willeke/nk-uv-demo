# Development Documentation

Welcome to the development documentation for nk-uv-demo. This section covers everything you need to know about developing, testing, and maintaining high-quality Python code.

## Overview

This project demonstrates Python DevOps best practices including:

- **Code Quality**: Automated formatting, linting, and type checking
- **Testing**: Comprehensive test suite with coverage reporting
- **Security**: Multiple layers of security scanning
- **Documentation**: Well-documented code and processes
- **Automation**: Pre-commit hooks and CI/CD integration

## Quick Navigation

### Essential Guides
- **[Code Quality](code-quality.md)** - Formatting, linting, and type checking
- **[Testing](testing.md)** - Test framework, coverage, and best practices
- **[Security](security.md)** - Security scanning tools and practices
- **[Pre-commit Hooks](pre-commit.md)** - Automated quality checks

### Development Workflow

1. **Start Development**: Follow the [installation guide](../getting-started/installation.md)
2. **Make Changes**: Use the tools described in [Code Quality](code-quality.md)
3. **Test Changes**: Run tests as described in [Testing](testing.md)
4. **Commit**: Let [Pre-commit hooks](pre-commit.md) ensure quality
5. **Deploy**: Use the [CI/CD workflows](../ci-cd/workflows.md)

## Development Tools Stack

| Category | Tool | Purpose | Configuration |
|----------|------|---------|---------------|
| **Formatting** | [Ruff](https://docs.astral.sh/ruff/) | Code formatting and fast linting | `pyproject.toml` |
| **Type Checking** | [Mypy](https://mypy-lang.org/) | Static type analysis | `pyproject.toml` |
| **Testing** | [pytest](https://docs.pytest.org/) | Test framework with coverage | `pyproject.toml` |
| **Dependencies** | [Deptry](https://deptry.com/) | Dependency analysis | `pyproject.toml` |
| **Security** | [Safety](https://pypi.org/project/safety/) | Vulnerability scanning | `.safety-project.ini` |
| **Automation** | [Pre-commit](https://pre-commit.com/) | Git hooks for quality | `.pre-commit-config.yaml` |

## Development Standards

### Code Style

We follow **PEP 8** with these specific configurations:

- **Line Length**: 88 characters (Black-compatible)
- **Indentation**: 4 spaces
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: reStructuredText (reST) format following PEP 257

### Quality Gates

Code must pass these checks before merging:

1. **Formatting**: Ruff format compliance
2. **Linting**: No Ruff lint errors
3. **Type Checking**: Mypy validation
4. **Tests**: All tests pass with >80% coverage
5. **Dependencies**: No unused or missing dependencies
6. **Security**: No known vulnerabilities

### Commit Standards

- **Pre-commit hooks**: Automatically enforce quality standards
- **Commit messages**: Clear, descriptive messages
- **Atomic commits**: One logical change per commit
- **Branch protection**: Main branch requires PR reviews

## Quick Start Commands

### Command Reference

See [Command Cheatsheet](../command-cheatsheet.md) for all development commands organized by tool.

## IDE Integration

### VS Code (Recommended)

The project includes VS Code configuration:

- **Extensions**: Automatic recommendations for Python, Ruff, and testing
- **Settings**: Pre-configured formatting, linting, and type checking
- **Tasks**: Integrated task runner
- **Debugging**: Python debugging configuration

### Other IDEs

For other IDEs, ensure they're configured to:
1. Use the `.venv` Python environment
2. Run Ruff for formatting and linting
3. Use Mypy for type checking
4. Integrate with pytest for testing

## Contributing Guidelines

1. **Fork and Clone**: Create your own fork of the repository
2. **Feature Branch**: Create a branch for your changes
3. **Develop**: Follow the quality standards outlined here
4. **Test**: Ensure all tests pass and add new tests for new features
5. **Submit PR**: Create a pull request with a clear description
6. **Review**: Address feedback and maintain quality standards

## Getting Help

- **Documentation**: Check the relevant guide in this docs/ folder
- **Taskfile**: Run `task help` for workflow information
- **Issues**: Check GitHub Issues for known problems
- **Discussions**: Use GitHub Discussions for questions

---

**Next Steps**: Start with [Code Quality](code-quality.md) to understand the tools and standards used in this project.
