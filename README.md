# Naturkart uv demo - Python DevOps best practices

This repository demonstrates best practices for Python project development and packaging. It showcases how to structure a Python project, manage dependencies with uv, implement CI/CD pipelines using GitHub Actions, and containerize code with Docker.

## Checklist

- [ ] Open-source **license** (e.g. MIT)
- [x] Repo **naming convention** (`nk-<name>`, `nkf-<name>`, etc.)
- [ ] GitHub Action workflow for **code security** (Dependabot, CodeQL)

## Requirements

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [GitHub](https://github.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/engine/install/) (optional)
- [VS Code](https://code.visualstudio.com/) (optional)

## Demo walk-through

To follow this walk-through you must  **clone** the repository to your local machine.

```bash
# clone from github and navigate to folder
gh repo clone naturkart-miljodir/nk-uv-demo
cd ~/git/nk-uv-demo
```

### **Test** the uv python package from CLI

```bash
# Run the entrypoint
uv run nk-uv-demo
# > Hello from nk-uv-demo!
```

For more uv commands check: [CLI Reference](https://docs.astral.sh/uv/reference/cli/)

### **Connect** to the Python environment `.venv`

In Visual Studio Code, the Python extension and Jupyter Notebooks extension detect the `.venv` created by `uv` package manager as the default environment. If not, set the enviroment manually. 

#### 1. Connect in Python Scripts

- Open a Python script in VS Code.
- Click on the Python version in the bottom left corner of the VS Code window.
- Click on "Enter interpreter path..." > enter path to python.exe in the .venv environment: `./.venv/Scripts/python.exe` or `./.venv/bin/python.exe`

#### 2. Connect from the terminal

```bash
# connect .venv environment
source .venv/bin/activate
```

#### 3. Connect in Jupyter Notebooks

- Open the notebook [notebooks/demo.ipynb](./notebooks/demo.ipynb)
- Select `.venv` as Kernel
    - Right-upper corner > "Select Kernel" > "add path to Kernel"
- Run the notebook cells to test whether you can use the local package inside the notebook. 

**Note:** To use the *.venv* inside notebooks the `ipykernel` must be installed in the *.venv*. You can install it as development dependency using: 

```bash
# add specific version of ipykernel to dev
uv add --group dev "ipykernel>=6.29.5,<7"
```
  