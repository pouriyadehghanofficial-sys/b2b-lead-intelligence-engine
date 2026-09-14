#!/usr/bin/env python
"""Run Streamlit UI"""

import subprocess
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment for Streamlit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_LOGGER_LEVEL'] = 'info'

if __name__ == "__main__":
    # Run Streamlit
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(project_root / "app" / "ui" / "main.py"),
            "--logger.level=info",
        ]
    )
