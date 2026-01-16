#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: System Diagnostic Tool
Helps troubleshoot installation and runtime issues.
"""

import sys
import platform
from pathlib import Path


def print_header(text):
    """Print section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def check_python_version():
    """Check Python version."""
    print_header("Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Version: {version_str}")
    print(f"Full: {sys.version}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False


def check_dependencies():
    """Check all dependencies."""
    print_header("Dependencies")
    
    all_good = True
    
    # Check pygame
    try:
        import pygame
        print(f"✅ pygame {pygame.version.ver} - Installed")
    except ImportError:
        print("❌ pygame - Not installed")
        print("   Install: pip install pygame")
        all_good = False
    
    # Check Pillow
    try:
        import PIL
        print(f"✅ Pillow {PIL.__version__} - Installed")
    except ImportError:
        print("❌ Pillow - Not installed")
        print("   Install: pip install Pillow")
        all_good = False
    
    return all_good


def check_file_structure():
    """Check project file structure."""
    print_header("File Structure")
    
    root = Path(__file__).parent
    required_files = [
        'python-core/interfaces.py',
        'python-core/graphics/adapter.py',
        'python-core/graphics/pygame_renderer.py',
        'python-core/graphics/snes_pygame_renderer.py',
        'python-core/config.py',
        'python-core/utils.py',
        'launch_game.py',
        'requirements.txt'
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_good = False
    
    return all_good


def check_import_paths():
    """Check if imports work."""
    print_header("Import Checks")
    
    all_good = True
    
    # Add python-core to path
    sys.path.insert(0, str(Path(__file__).parent / 'python-core'))
    
    # Try interfaces
    try:
        from interfaces import GameStateInterface
        print("✅ interfaces.py - Can import")
    except Exception as e:
        print(f"❌ interfaces.py - Import error: {e}")
        all_good = False
    
    # Try adapter
    try:
        from graphics.adapter import GraphicsAdapter
        print("✅ graphics.adapter - Can import")
    except Exception as e:
        print(f"❌ graphics.adapter - Import error: {e}")
        all_good = False
    
    # Try pygame renderer
    try:
        from graphics.pygame_renderer import PygameRenderer
        print("✅ graphics.pygame_renderer - Can import")
    except Exception as e:
        print(f"❌ graphics.pygame_renderer - Import error: {e}")
        all_good = False
    
    # Try SNES renderer
    try:
        from graphics.snes_pygame_renderer import SNESPygameRenderer
        print("✅ graphics.snes_pygame_renderer - Can import")
    except Exception as e:
        print(f"❌ graphics.snes_pygame_renderer - Import error: {e}")
        all_good = False
    
    # Try config
    try:
        from config import ConfigManager
        print("✅ config.py - Can import")
    except Exception as e:
        print(f"❌ config.py - Import error: {e}")
        all_good = False
    
    # Try utils
    try:
        from utils import clamp
        print("✅ utils.py - Can import")
    except Exception as e:
        print(f"❌ utils.py - Import error: {e}")
        all_good = False
    
    return all_good


def check_pygame_display():
    """Check if pygame can create a display."""
    print_header("Pygame Display Test")
    
    try:
        import pygame
        pygame.init()
        
        # Try to create a small test window
        screen = pygame.display.set_mode((320, 240))
        print("✅ Pygame display initialized")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"❌ Pygame display error: {e}")
        print("   This may be normal in headless environments")
        return False


def check_system_info():
    """Display system information."""
    print_header("System Information")
    
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Implementation: {platform.python_implementation()}")


def check_configuration():
    """Check configuration file."""
    print_header("Configuration")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'python-core'))
        from config import ConfigManager
        
        config = ConfigManager()
        print(f"✅ Configuration loaded")
        print(f"   Graphics Mode: {config.get('graphics.mode')}")
        print(f"   Resolution: {config.get_resolution()}")
        print(f"   FPS: {config.get('graphics.fps')}")
        print(f"   Scale: {config.get('graphics.scale')}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def check_validation_scripts():
    """Check if validation scripts exist."""
    print_header("Validation Scripts")
    
    root = Path(__file__).parent
    scripts = [
        'automation/validate_interfaces.py',
        'automation/validate_no_redundancy.py',
        'automation/validate_save_files.py',
        'automation/validate_feature_parity.py'
    ]
    
    all_good = True
    for script in scripts:
        path = root / script
        if path.exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - Missing")
            all_good = False
    
    return all_good


def run_quick_test():
    """Run a quick functional test."""
    print_header("Quick Functional Test")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'python-core'))
        
        # Test adapter creation
        from graphics.adapter import GraphicsAdapter
        from unittest.mock import Mock
        
        engine = Mock()
        engine.state = 'in_game'
        engine.player = Mock()
        engine.player.name = "Test"
        engine.player.stats = Mock()
        engine.player.stats.current_hp = 100
        engine.player.stats.max_hp = 100
        engine.party = []
        engine.current_location = Mock()
        engine.current_location.name = "Test"
        engine.current_location.description = "Test area"
        engine.current_location.npcs = []
        
        adapter = GraphicsAdapter(engine)
        
        # Test interface methods
        location = adapter.get_player_location()
        party = adapter.get_party_members()
        actions = adapter.get_available_actions()
        
        print("✅ Adapter functional test passed")
        print(f"   Location: {location.get('name')}")
        print(f"   Party size: {len(party)}")
        print(f"   Available actions: {len(actions)}")
        return True
    except Exception as e:
        print(f"❌ Functional test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_recommendations(results):
    """Print recommendations based on test results."""
    print_header("Recommendations")
    
    if all(results.values()):
        print("✅ All checks passed! System is ready.")
        print("\nYou can now run:")
        print("  python3 launch_game.py")
    else:
        print("⚠️  Some checks failed. Here's what to do:\n")
        
        if not results['python']:
            print("1. Upgrade Python to 3.8 or higher")
            print("   Visit: https://www.python.org/downloads/\n")
        
        if not results['dependencies']:
            print("2. Install missing dependencies:")
            print("   pip install -r requirements.txt\n")
        
        if not results['file_structure']:
            print("3. Re-download the project or check for file corruption\n")
        
        if not results['imports']:
            print("4. Check Python path and working directory")
            print("   Run from project root directory\n")
        
        if not results['pygame_display']:
            print("5. Pygame display issue detected")
            print("   - On Linux: May need X11/Wayland display")
            print("   - Try text mode: python3 launch_game.py --mode text\n")


def main():
    """Run diagnostic tool."""
    print("\n" + "=" * 60)
    print("COIN-OPERATED JRPG - System Diagnostic Tool".center(60))
    print("=" * 60)
    
    results = {}
    
    # Run all checks
    results['python'] = check_python_version()
    results['dependencies'] = check_dependencies()
    results['file_structure'] = check_file_structure()
    results['imports'] = check_import_paths()
    results['pygame_display'] = check_pygame_display()
    results['configuration'] = check_configuration()
    results['validation'] = check_validation_scripts()
    results['functional'] = run_quick_test()
    
    # System info
    check_system_info()
    
    # Print recommendations
    print_recommendations(results)
    
    # Summary
    print_header("Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Checks Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 System is fully operational!")
        return 0
    elif passed >= total * 0.7:
        print("\n⚠️  System is mostly operational with minor issues")
        return 0
    else:
        print("\n❌ System has significant issues - please fix errors above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
