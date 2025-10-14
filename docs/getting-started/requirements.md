# Requirements

This document outlines the system requirements and tools needed to work with the nk-uv-demo project.

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.12 or higher (managed by uv)

## Required Tools

### Essential Tools

- **[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)**: Version control system
- **[GitHub](https://github.com/)**: Repository hosting and collaboration
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**: Fast Python package manager and resolver

### Recommended Tools

- **[Task](https://taskfile.dev/installation/)**: Task runner for simplified development workflow
- **[VS Code](https://code.visualstudio.com/)**: Code editor with excellent Python support
- **[Docker](https://docs.docker.com/engine/install/)**: Containerization platform (for containerization features)

## Tool Installation

### Install uv (Required)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Task (Recommended)

**Linux/macOS:**
```bash
# Using Homebrew
brew install go-task

# Using curl
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
```

**Windows:**
```powershell
# Using Chocolatey
choco install go-task

# Using Scoop
scoop install task
```

### Install Docker (Optional)

Follow the official installation guide for your platform:
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Desktop for macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Engine for Linux](https://docs.docker.com/engine/install/)

## Verification

After installing the required tools, verify they're working:

```bash
# Check tool versions
git --version
uv --version
task --version  # if installed
docker --version  # if installed

# Test uv functionality
uv python list
```

## Next Steps

Once you have the requirements installed, proceed to:
- [Installation Guide](installation.md) - Clone and set up the project
- [Quick Start](quickstart.md) - Get up and running quickly with Taskfile
