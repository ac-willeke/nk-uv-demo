"""Tests for the main module."""

import sys
from pathlib import Path
import pytest

# Add the src directory to the Python path if not already added
# sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import project modules after path setup
from nk_uv_demo import main


def test_main_function_output(capsys):
    """Test that the main function prints the expected output."""
    main()
    captured = capsys.readouterr()
    assert "Hello from nk-uv-demo!" in captured.out
