#!/usr/bin/env python3
"""
Simple launcher for the Professional GitHub PR Analytics Platform GUI
"""

import os
import sys
import subprocess

def main():
    """Launch the professional GUI"""
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gui_launcher = os.path.join(script_dir, "run_gui.py")
    
    print("🚀 Launching GitHub PR Analytics Platform...")
    
    try:
        subprocess.run([sys.executable, gui_launcher])
    except KeyboardInterrupt:
        print("\n👋 GUI launcher stopped")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")

if __name__ == "__main__":
    main() 