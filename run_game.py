#!/usr/bin/env python3
"""
NEXUS AI REASONING WAR - Primary Terminal Game Launcher
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from UI.terminal_game import TerminalGameEngine


def main():
    engine = TerminalGameEngine()
    engine.run_interactive_loop()


if __name__ == "__main__":
    main()
