#!/usr/bin/env python3
"""
NEXUS AI REASONING WAR - Desktop Graphical 2D Window Launcher (Tkinter Canvas)
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from UI.desktop_gui import DesktopGUIEngine, TK_AVAILABLE


def main():
    if not TK_AVAILABLE:
        print("[!] Tkinter not available in this Python environment. Launching interactive terminal engine...")
        from UI.terminal_game import TerminalGameEngine
        TerminalGameEngine().run_interactive_loop()
        return

    gui = DesktopGUIEngine()
    gui.run()


if __name__ == "__main__":
    main()
