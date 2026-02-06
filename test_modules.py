#!/usr/bin/env python3
"""
Test script to verify all modules can be imported
Run this before building to ensure everything is working
"""

import sys


def test_imports():
    """Test that all modules can be imported"""
    
    print("Testing module imports...")
    print("-" * 60)
    
    tests = [
        ("config", "Configuration"),
        ("hardware", "Hardware Controller"),
        ("audio", "Audio Processor"),
        ("tuning", "Tuning Manager"),
        ("state", "Application State"),
        ("web_interface", "Web Interface"),
        ("main", "Main Application"),
    ]
    
    failed = []
    
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✓ {description:25s} ({module_name}.py)")
        except ImportError as e:
            print(f"✗ {description:25s} ({module_name}.py) - FAILED")
            print(f"  Error: {e}")
            failed.append(module_name)
        except Exception as e:
            print(f"⚠ {description:25s} ({module_name}.py) - WARNING")
            print(f"  Error: {e}")
    
    print("-" * 60)
    
    if failed:
        print(f"\n❌ {len(failed)} module(s) failed to import:")
        for mod in failed:
            print(f"   - {mod}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        print("\nYou can now:")
        print("   1. Run directly: python3 main.py")
        print("   2. Build executable: python3 build.py")
        return True


def test_dependencies():
    """Test that required dependencies are installed"""
    
    print("\nTesting dependencies...")
    print("-" * 60)
    
    deps = [
        ("RPi.GPIO", "Raspberry Pi GPIO"),
        ("numpy", "NumPy"),
        ("pyaudio", "PyAudio"),
        ("RPLCD", "RPLCD"),
        ("flask", "Flask"),
    ]
    
    missing = []
    
    for module, name in deps:
        try:
            __import__(module)
            print(f"✓ {name:25s}")
        except ImportError:
            print(f"✗ {name:25s} - NOT INSTALLED")
            missing.append(name)
    
    print("-" * 60)
    
    if missing:
        print(f"\n  {len(missing)} dependency/dependencies missing:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nNote: RPi.GPIO will only work on Raspberry Pi hardware")
        print("      Other systems can still test the build process")
    else:
        print("\n All dependencies installed!")
    
    print()


def main():
    """Main test runner"""
    print("="*60)
    print("Guitar Tuner - Module Test")
    print("="*60)
    print()
    
    # Test dependencies first
    test_dependencies()
    
    # Test module imports
    success = test_imports()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
