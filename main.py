#!/usr/bin/env python3
"""
NEXUS AI REASONING WAR (2088)
A Real AI Puzzle Adventure Game
Master Entrypoint supporting Terminal Engine, Desktop GUI, Web Canvas, and Automated Test Suite.
"""

import sys
import os
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main():
    parser = argparse.ArgumentParser(
        description="NEXUS AI REASONING WAR — A Real Playable AI Puzzle Adventure Game"
    )
    parser.add_argument("--terminal", action="store_true", help="Launch Cyberpunk Terminal Game Canvas")
    parser.add_argument("--gui", action="store_true", help="Launch Native 2D Desktop Graphical Window")
    parser.add_argument("--web", action="store_true", help="Launch Streamlit Web Game Canvas")
    parser.add_argument("--test", action="store_true", help="Run Complete System Verification Test Suite")

    args = parser.parse_args()

    if args.test:
        from Tests.test_all import run_all_tests
        sys.exit(run_all_tests())
    elif args.gui:
        from UI.desktop_gui import DesktopGUIEngine, TK_AVAILABLE
        if TK_AVAILABLE:
            DesktopGUIEngine().run()
        else:
            print("[!] Tkinter not available in current python runtime. Launching Terminal engine...")
            from UI.terminal_game import TerminalGameEngine
            TerminalGameEngine().run_interactive_loop()
    elif args.web:
        from run_web import main as run_web_main
        run_web_main()
    else:
        # Default: Terminal Interactive Game Canvas
        from UI.terminal_game import TerminalGameEngine
        TerminalGameEngine().run_interactive_loop()


if __name__ == "__main__":
    main()
