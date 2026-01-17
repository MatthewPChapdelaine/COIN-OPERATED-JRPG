#!/usr/bin/env python3
"""
COIN:OPERATED JRPG - Installation Script for Desktop Integration
Installs desktop launcher and makes the game easily accessible
"""

import os
import sys
import shutil
from pathlib import Path

def install_desktop_launcher():
    """Install .desktop file for Linux desktop integration"""
    
    # Get paths
    project_root = Path(__file__).parent.absolute()
    desktop_file = project_root / "COIN-OPERATED-JRPG.desktop"
    
    # Update paths in desktop file to be absolute
    with open(desktop_file, 'r') as f:
        content = f.read()
    
    content = content.replace('/workspaces/COIN-OPERATED-JRPG', str(project_root))
    
    # Write updated desktop file
    temp_desktop = project_root / "COIN-OPERATED-JRPG_updated.desktop"
    with open(temp_desktop, 'w') as f:
        f.write(content)
    
    # Find appropriate desktop directory
    desktop_dirs = [
        Path.home() / ".local" / "share" / "applications",
        Path.home() / "Desktop",
        Path("/usr/share/applications")
    ]
    
    installed = False
    for desktop_dir in desktop_dirs:
        if desktop_dir.exists() and os.access(desktop_dir, os.W_OK):
            try:
                dest = desktop_dir / "COIN-OPERATED-JRPG.desktop"
                shutil.copy2(temp_desktop, dest)
                os.chmod(dest, 0o755)
                print(f"✓ Installed desktop launcher to: {dest}")
                installed = True
                break
            except Exception as e:
                print(f"⚠ Failed to install to {desktop_dir}: {e}")
                continue
    
    # Clean up temp file
    temp_desktop.unlink()
    
    if not installed:
        print("⚠ Could not install desktop launcher automatically")
        print(f"  Manual installation: Copy {desktop_file} to ~/.local/share/applications/")
    
    return installed

def make_executable():
    """Make main game launcher executable"""
    project_root = Path(__file__).parent.absolute()
    launcher = project_root / "coin_operated.py"
    
    if launcher.exists():
        os.chmod(launcher, 0o755)
        print(f"✓ Made executable: {launcher}")
        return True
    else:
        print(f"⚠ Launcher not found: {launcher}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n Checking dependencies...")
    
    missing = []
    
    try:
        import pygame
        print("✓ pygame installed")
    except ImportError:
        print("✗ pygame NOT installed")
        missing.append("pygame")
    
    try:
        from PIL import Image
        print("✓ PIL/Pillow installed")
    except ImportError:
        print("✗ PIL/Pillow NOT installed")
        missing.append("Pillow")
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("\nTo install:")
        print(f"  pip install {' '.join(missing)}")
        print("OR")
        print(f"  pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed!")
    return True

def main():
    print("=" * 60)
    print(" COIN:OPERATED JRPG - Installation")
    print("=" * 60)
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n⚠ Please install dependencies before continuing")
        sys.exit(1)
    
    print("\n🔧 Installing desktop integration...")
    
    # Make launcher executable
    make_executable()
    
    # Install desktop launcher
    install_desktop_launcher()
    
    print("\n" + "=" * 60)
    print(" Installation Complete!")
    print("=" * 60)
    print("\n🎮 You can now launch COIN:OPERATED from:")
    print("  1. Your applications menu")
    print("  2. Desktop icon (if installed to Desktop)")
    print("  3. Command line: python3 coin_operated.py")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
