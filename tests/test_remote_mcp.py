"""Regression coverage for external MCP discovery failures."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXAMPLES = ROOT / "examples"


def load_lesson():
    sys.path.insert(0, str(EXAMPLES))
    spec = importlib.util.spec_from_file_location(
        "remote_mcp", EXAMPLES / "33_remote_mcp.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_mcp_discovery_failure_is_explained() -> None:
    lesson = load_lesson()
    assert "HTTP 424" in lesson.describe_mcp_failure(424)
    assert "could not reach" in lesson.describe_mcp_failure(None)
