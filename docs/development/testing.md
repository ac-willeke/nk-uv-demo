# Testing

This document covers the testing framework, coverage requirements, and best practices used in nk-uv-demo.

## Overview

Testing ensures code reliability and maintainability through:

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **Coverage Analysis**: Ensure comprehensive test coverage
- **Continuous Testing**: Automated testing in CI/CD

## Testing Framework

### pytest - Python Testing Framework

We use [pytest](https://docs.pytest.org/) as our primary testing framework.

**Configuration**: `pyproject.toml` → `[tool.pytest.ini_options]`

#### Key Features
- **Simple Syntax**: Natural assert statements
- **Fixtures**: Reusable test data and setup
- **Parametrized Tests**: Run tests with multiple inputs
- **Plugin Ecosystem**: Extensive plugin support
- **Coverage Integration**: Built-in coverage reporting

### pytest-cov - Coverage Analysis

[pytest-cov](https://pytest-cov.readthedocs.io/) provides code coverage analysis.

#### Coverage Configuration
```toml
[tool.pytest.ini_options]
addopts = [
  "--cov=src",                    # Cover source code
  "--cov-report=term",            # Terminal coverage report
  "--cov-report=xml:coverage.xml" # XML report for CI
]
```

## Running Tests

### Using Taskfile (Recommended)

```bash
# Run all tests
task test

# Run tests with HTML coverage report
task test-html

# Run specific test file
uv run pytest tests/test_main.py

# Run with coverage details
uv run pytest --cov --cov-report=html
```

### Direct pytest Commands

```bash
# Basic test run
uv run pytest

# Verbose output
uv run pytest -v

# Run specific tests
uv run pytest tests/test_main.py::test_main_function

# Run tests matching pattern
uv run pytest -k "test_main"

# Show coverage report
uv run pytest --cov=src --cov-report=term-missing
```

### Coverage Reports

```bash
# Generate HTML coverage report
task test-html
open htmlcov/index.html  # View in browser

# Terminal coverage report
uv run pytest --cov --cov-report=term

# Generate XML report (for CI)
uv run pytest --cov --cov-report=xml
```

## Test Structure

### Directory Layout

```
tests/
├── __init__.py              # Test package marker
├── conftest.py             # Shared test configuration and fixtures
├── nk_uv_demo/            # Test modules mirroring src structure
│   ├── __init__.py
│   └── test_main.py       # Tests for main module
└── integration/           # Integration tests (if needed)
    └── test_workflows.py
```

### Test File Naming

- **Test Files**: `test_*.py` or `*_test.py`
- **Test Functions**: `test_*`
- **Test Classes**: `Test*`
- **Test Methods**: `test_*`

### Example Test Structure

```python
# tests/nk_uv_demo/test_main.py
"""Tests for the main module."""

import pytest
from nk_uv_demo.main import hello_world, calculate_something


class TestHelloWorld:
    """Test cases for hello_world function."""

    def test_hello_world_returns_string(self):
        """Test that hello_world returns a string."""
        result = hello_world()
        assert isinstance(result, str)
        assert result == "Hello from nk-uv-demo!"

    def test_hello_world_with_name(self):
        """Test hello_world with custom name."""
        result = hello_world("Alice")
        assert result == "Hello, Alice!"


class TestCalculateSomething:
    """Test cases for calculate_something function."""

    @pytest.mark.parametrize("input_val,expected", [
        (0, 0),
        (1, 2),
        (5, 10),
        (-3, -6),
    ])
    def test_calculate_something_parametrized(self, input_val, expected):
        """Test calculate_something with various inputs."""
        result = calculate_something(input_val)
        assert result == expected

    def test_calculate_something_invalid_input(self):
        """Test calculate_something with invalid input."""
        with pytest.raises(TypeError):
            calculate_something("invalid")
```

## Testing Best Practices

### 1. Test Organization

```python
# Good: Organized test class
class TestUserManager:
    """Test cases for UserManager class."""

    def test_create_user_success(self):
        """Test successful user creation."""
        pass

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        pass

    def test_delete_user_success(self):
        """Test successful user deletion."""
        pass
```

### 2. Fixtures for Reusable Test Data

```python
# conftest.py
import pytest
from nk_uv_demo.models import User

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(name="Test User", email="test@example.com")

@pytest.fixture
def user_manager():
    """Create a user manager instance."""
    return UserManager(database_url="sqlite:///:memory:")

# test_user.py
def test_user_creation(sample_user):
    """Test user creation with fixture."""
    assert sample_user.name == "Test User"
    assert sample_user.email == "test@example.com"
```

### 3. Parametrized Tests

```python
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("invalid.email", False),
    ("", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    """Test email validation with multiple inputs."""
    result = validate_email(email)
    assert result == is_valid
```

### 4. Exception Testing

```python
def test_division_by_zero():
    """Test that division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_input_message():
    """Test specific exception message."""
    with pytest.raises(ValueError, match="Input must be positive"):
        process_positive_number(-5)
```

### 5. Mocking External Dependencies

```python
from unittest.mock import patch, Mock

@patch('nk_uv_demo.external_api.requests.get')
def test_api_call_success(mock_get):
    """Test successful API call."""
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_get.return_value = mock_response

    # Test
    result = fetch_data_from_api()

    # Assertions
    assert result["status"] == "success"
    mock_get.assert_called_once()
```

## Coverage Requirements

### Coverage Targets

- **Minimum Coverage**: 80%
- **Target Coverage**: 90%+
- **Critical Code**: 100% (error handling, security functions)

### Coverage Configuration

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=src",                 # Cover source directory
    "--cov-report=term",         # Terminal report
    "--cov-report=xml",          # XML for CI
    "--cov-fail-under=80"        # Fail if coverage < 80%
]
```

### Analyzing Coverage

```bash
# Detailed coverage report
uv run pytest --cov --cov-report=term-missing

# HTML report for visual analysis
task test-html
open htmlcov/index.html

# Focus on specific modules
uv run pytest --cov=src/nk_uv_demo --cov-report=term
```

### Coverage Exclusions

Mark code that shouldn't be covered:

```python
def debug_function():  # pragma: no cover
    """Development-only function."""
    print("Debug information")

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional
```

## Test Markers

### Custom Markers

Define custom markers in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "ci_exclude: Tests excluded from CI/CD pipeline",
    "integration: Integration tests",
    "slow: Slow-running tests"
]
```

### Using Markers

```python
@pytest.mark.ci_exclude
def test_local_only():
    """Test that only runs locally."""
    pass

@pytest.mark.slow
def test_performance():
    """Performance test that takes time."""
    pass

# Run tests excluding certain markers
# uv run pytest -m "not slow"
# uv run pytest -m "not ci_exclude"
```

## Integration with CI/CD

### GitHub Actions Integration

Tests run automatically in CI/CD:

```yaml
# .github/workflows/ci-pytest.yml
- name: Run tests with coverage
  run: |
    uv run pytest --cov --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: coverage.xml
```

### Local CI Simulation

```bash
# Run full CI test suite locally
task ci-local

# This includes:
# - Code formatting check
# - Linting
# - Type checking
# - Test suite with coverage
# - Dependency analysis
```

## Testing Jupyter Notebooks

For testing notebook functionality:

```python
# tests/test_notebooks.py
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def test_notebook_execution():
    """Test that demo notebook runs without errors."""
    with open("notebooks/demo.ipynb") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})
```

## Troubleshooting

### Common Issues

**Tests not discovered:**
```bash
# Check test discovery
uv run pytest --collect-only

# Ensure proper naming (test_*.py or *_test.py)
# Ensure __init__.py files exist
```

**Import errors:**
```bash
# Install package in development mode
uv pip install -e .

# Check PYTHONPATH
uv run python -c "import sys; print(sys.path)"
```

**Coverage issues:**
```bash
# Clear coverage data
rm .coverage coverage.xml
rm -rf htmlcov/

# Run fresh coverage
task test-html
```

**Slow tests:**
```bash
# Run only fast tests
uv run pytest -m "not slow"

# Profile slow tests
uv run pytest --durations=10
```

### Debugging Tests

```python
# Add print statements for debugging
def test_debug_example():
    result = some_function()
    print(f"Debug: result = {result}")  # Will show in pytest -s
    assert result == expected

# Run with output
uv run pytest -s  # Show print statements
uv run pytest -v  # Verbose test names
uv run pytest --pdb  # Drop into debugger on failure
```

## Performance Testing

For performance-sensitive code:

```python
import time
import pytest

@pytest.mark.slow
def test_performance():
    """Test that function completes within time limit."""
    start_time = time.time()

    # Run the function
    result = expensive_function()

    end_time = time.time()
    execution_time = end_time - start_time

    assert execution_time < 5.0  # Should complete in < 5 seconds
    assert result is not None
```

---

**Next Steps**: Learn about [Security](security.md) practices to keep your code safe from vulnerabilities.
