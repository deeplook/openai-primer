"""Each lesson must be safe to run without credentials or network access."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_every_numbered_example_runs_offline() -> None:
    examples = sorted((ROOT / "examples").glob("[0-9][0-9]_*.py"))
    assert len(examples) == 34
    environment = os.environ | {"OPENAI_API_KEY": ""}
    for example in examples:
        result = subprocess.run(
            [sys.executable, str(example)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        assert result.returncode == 0, f"{example.name}: {result.stderr}"
        assert "OK:" in result.stdout or "SKIP:" in result.stdout
