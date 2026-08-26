#!/usr/bin/env python3
"""
NEXUS AI REASONING WAR - Interactive Web Canvas Launcher
"""

import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main():
    app_path = os.path.join(os.path.dirname(__file__), "UI", "web_game.py")
    print(f"[*] Starting Streamlit Web Game Canvas: {app_path}")
    try:
        subprocess.run(["streamlit", "run", app_path, "--server.port", "8503"], check=True)
    except FileNotFoundError:
        print("[!] Streamlit binary not found. Falling back to Native Terminal Engine...")
        from UI.terminal_game import TerminalGameEngine
        TerminalGameEngine().run_interactive_loop()


if __name__ == "__main__":
    main()
