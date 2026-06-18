"""Test the mypy plugin."""

from pathlib import Path

from mypy import api

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"
MYPY_CONFIG_FILE = SAMPLES_DIR / "mypy.ini"
OK_SAMPLE_FILE = SAMPLES_DIR / "shapes_ok.py"
FAILURE_SAMPLE_FILE = SAMPLES_DIR / "shapes_failure.py"


def test_mypy_analyze_ok() -> None:
    """Test that mypy reports no diagnostic when analyzing the OK file."""
    stdout, stderr, status = api.run([str(OK_SAMPLE_FILE), "--config-file", str(MYPY_CONFIG_FILE)])
    assert "Success: no issues found in 1 source file" in stdout
    assert status == 0
    assert stderr == ""


def test_mypy_analyze_failure() -> None:
    """Test that mypy reports a diagnostic when analyzing the failure file."""
    stdout, stderr, status = api.run([str(FAILURE_SAMPLE_FILE), "--config-file", str(MYPY_CONFIG_FILE)])
    assert (
        """shapes_failure.py:33: error: Union member "Circle" does not implement protocol "ShapeProperties"  [misc]"""
        in stdout
    )
    assert "error: Missing member: area  [misc]" in stdout
    assert "Found 2 errors in 1 file (checked 1 source file)" in stdout
    assert status == 1
    assert stderr == ""
