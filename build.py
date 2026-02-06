#!/usr/bin/env python3
"""
Setup script for creating a standalone executable
Uses PyInstaller to bundle all files into one executable
"""

import os
import subprocess
import sys


def install_pyinstaller():
    """Install PyInstaller if not present"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--name=guitar_tuner",          # Name of the executable
        "--hidden-import=RPi.GPIO",     # Include hidden imports
        "--hidden-import=numpy",
        "--hidden-import=pyaudio",
        "--hidden-import=RPLCD",
        "--hidden-import=flask",
        "--add-data=config.py:.",       # Include all Python modules
        "--add-data=hardware.py:.",
        "--add-data=audio.py:.",
        "--add-data=tuning.py:.",
        "--add-data=state.py:.",
        "--add-data=web_interface.py:.",
        "main.py"                       # Main entry point
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build successful!")
        print("Executable location: dist/guitar_tuner")
        print("="*60)
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)


def main():
    print("Guitar Tuner - Executable Builder")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    build_executable()


if __name__ == "__main__":
    main()
