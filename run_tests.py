#!/usr/bin/env python
"""Run all tests"""

import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent

if __name__ == "__main__":
    # Run pytest
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(project_root / "tests"),
            "-v",
            "--tb=short",
        ]
    )
    sys.exit(result.returncode)
