#!/usr/bin/env python3
"""
Quick verification test for COIN:OPERATED JRPG
Tests core functionality without requiring bash
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Check Python version"""
    print("[1/6] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (3.8+ required)")
        return False

def test_dependencies():
    """Check required dependencies"""
    print("\n[2/6] Checking dependencies...")
    try:
        import PIL
        print(f"✓ Pillow {PIL.__version__}")
        return True
    except ImportError:
        print("✗ Pillow not installed")
        print("  Install with: pip3 install Pillow>=9.0.0")
        return False

def test_file_structure():
    """Check essential files exist"""
    print("\n[3/6] Checking project structure...")
    
    required_files = [
        "python-core/main.py",
        "python-core/core/game_engine.py",
        "python-core/core/character.py",
        "python-core/systems/combat.py",
        "python-core/content/act1_content.py",
        "play.py",
        "README.md",
        "LICENSE",
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ Missing: {file}")
            missing.append(file)
    
    return len(missing) == 0

def test_game_engine():
    """Test game engine imports"""
    print("\n[4/6] Testing game engine...")
    try:
        sys.path.insert(0, 'python-core')
        from core.game_engine import GameEngine
        print("✓ Game engine loads successfully")
        return True
    except Exception as e:
        print(f"✗ Game engine failed to load: {e}")
        return False

def test_graphics_system():
    """Check graphics system files"""
    print("\n[5/6] Checking graphics system...")
    
    graphics_files = [
        "python-core/graphics/snes_palette.py",
        "python-core/graphics/snes_sprite_generator.py",
        "python-core/graphics/snes_renderer.py",
    ]
    
    found = 0
    for file in graphics_files:
        if Path(file).exists():
            found += 1
    
    if found == len(graphics_files):
        print(f"✓ SNES graphics system complete ({found}/{len(graphics_files)} files)")
        return True
    elif found > 0:
        print(f"⚠ Partial SNES graphics system ({found}/{len(graphics_files)} files)")
        return True
    else:
        print("⚠ No graphics system found (optional)")
        return True

def test_steam_files():
    """Check Steam deployment files"""
    print("\n[6/6] Checking Steam files...")
    
    steam_files = [
        "steam_appid.txt",
        "steam_app_build.vdf",
        "build_steam.sh",
        "generate_icon.py",
    ]
    
    missing = []
    for file in steam_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ Missing: {file}")
            missing.append(file)
    
    return len(missing) == 0

def main():
    """Run all tests"""
    print("=" * 50)
    print("COIN:OPERATED JRPG - System Verification")
    print("=" * 50)
    print()
    
    results = []
    results.append(test_python_version())
    results.append(test_dependencies())
    results.append(test_file_structure())
    results.append(test_game_engine())
    results.append(test_graphics_system())
    results.append(test_steam_files())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("✓ ALL CHECKS PASSED!")
        print("=" * 50)
        print()
        print("Your game is ready!")
        print()
        print("To play: python3 play.py")
        print("To build for Steam: bash build_steam.sh")
        print()
        return 0
    else:
        failed = sum(1 for r in results if not r)
        print(f"✗ {failed} CHECK(S) FAILED")
        print("=" * 50)
        print()
        print("Please fix the issues above before deploying.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
