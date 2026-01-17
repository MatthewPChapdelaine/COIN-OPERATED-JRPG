#!/usr/bin/env python3
"""
COIN:OPERATED JRPG - Cross-Platform Automated Installer
Works on Linux, macOS, and Windows with zero technical knowledge required
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil

# Colors for terminal output
class Colors:
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    """Print installation banner"""
    clear_screen()
    print(f"{Colors.PURPLE}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.PURPLE}║{Colors.NC}                                                          {Colors.PURPLE}║{Colors.NC}")
    print(f"{Colors.PURPLE}║{Colors.NC}              {Colors.YELLOW}🪙 COIN:OPERATED JRPG 🪙{Colors.NC}                    {Colors.PURPLE}║{Colors.NC}")
    print(f"{Colors.PURPLE}║{Colors.NC}                                                          {Colors.PURPLE}║{Colors.NC}")
    print(f"{Colors.PURPLE}║{Colors.NC}            {Colors.CYAN}Automated Installation Wizard{Colors.NC}            {Colors.PURPLE}║{Colors.NC}")
    print(f"{Colors.PURPLE}║{Colors.NC}                                                          {Colors.PURPLE}║{Colors.NC}")
    print(f"{Colors.PURPLE}╚══════════════════════════════════════════════════════════╝{Colors.NC}")
    print()
    print(f"{Colors.BOLD}This installer will:{Colors.NC}")
    print("  ✓ Check system requirements")
    print("  ✓ Install dependencies automatically")
    print("  ✓ Set up desktop integration")
    print("  ✓ Create shortcuts")
    print("  ✓ Configure everything for you")
    print()

def print_success(message):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {message}")

def print_error(message):
    print(f"{Colors.RED}[✗]{Colors.NC} {message}")

def print_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[!]{Colors.NC} {message}")

def check_python():
    """Check Python version"""
    print_info("Checking Python installation...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, but you have {version.major}.{version.minor}")
        print("\nPlease install Python 3.8 or higher from: https://www.python.org/downloads/")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_info("Installing Python dependencies (this may take a minute)...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL)
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        print("\nTry manually: pip install -r requirements.txt")
        return False

def verify_pygame():
    """Verify pygame installation"""
    print_info("Verifying pygame installation...")
    
    try:
        import pygame
        print_success("Pygame is working")
        return True
    except ImportError:
        print_error("Pygame installation failed")
        return False

def verify_pillow():
    """Verify Pillow installation"""
    print_info("Verifying Pillow installation...")
    
    try:
        from PIL import Image
        print_success("Pillow is working")
        return True
    except ImportError:
        print_error("Pillow installation failed")
        return False

def create_linux_desktop_file(project_dir):
    """Create Linux desktop file"""
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=COIN:OPERATED
Comment=A 16-bit Retro JRPG - Journey from Coin to Time Goddess
Exec=/usr/bin/python3 "{project_dir}/coin_operated.py"
Path={project_dir}
Icon={project_dir}/assets/icon.png
Terminal=false
Categories=Game;RolePlaying;
Keywords=jrpg;rpg;game;retro;16bit;coin;
StartupNotify=true
StartupWMClass=coin_operated"""
    
    # Create applications directory
    apps_dir = Path.home() / ".local" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    
    # Write desktop file
    desktop_file = apps_dir / "COIN-OPERATED-JRPG.desktop"
    desktop_file.write_text(desktop_content)
    desktop_file.chmod(0o755)
    
    print_success("Application menu shortcut created")
    
    # Offer desktop shortcut
    response = input(f"\n{Colors.YELLOW}Create desktop shortcut? (y/n): {Colors.NC}").strip().lower()
    if response == 'y':
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            shutil.copy(desktop_file, desktop_dir / "COIN-OPERATED-JRPG.desktop")
            (desktop_dir / "COIN-OPERATED-JRPG.desktop").chmod(0o755)
            print_success("Desktop shortcut created")
        else:
            print_warning("Desktop directory not found")

def create_macos_app():
    """Create macOS application bundle"""
    print_info("Creating macOS application bundle...")
    # TODO: Implement macOS .app bundle creation
    print_warning("macOS app bundle creation not yet implemented")
    print("You can launch with: python3 coin_operated.py")

def create_windows_shortcut(project_dir):
    """Create Windows shortcut"""
    print_info("Creating Windows shortcuts...")
    
    # Create play.bat
    play_bat = project_dir / "play.bat"
    play_bat.write_text(f'@echo off\ncd /d "%~dp0"\npython coin_operated.py\n')
    
    print_success("Quick launch script created (play.bat)")
    
    response = input(f"\n{Colors.YELLOW}Create desktop shortcut? (y/n): {Colors.NC}").strip().lower()
    if response == 'y':
        try:
            # Use PowerShell to create shortcut
            desktop = Path.home() / "Desktop"
            ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{desktop}\\COIN-OPERATED.lnk")
$Shortcut.TargetPath = "{play_bat}"
$Shortcut.WorkingDirectory = "{project_dir}"
$Shortcut.Description = "COIN:OPERATED JRPG - 16-bit Retro RPG"
$Shortcut.Save()
"""
            subprocess.run(["powershell", "-Command", ps_script], check=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success("Desktop shortcut created")
        except:
            print_warning("Could not create desktop shortcut automatically")
            print("You can manually create a shortcut to play.bat")

def setup_desktop_integration():
    """Set up platform-specific desktop integration"""
    print_info("Setting up desktop integration...")
    
    project_dir = Path(__file__).parent.absolute()
    system = platform.system()
    
    if system == "Linux":
        create_linux_desktop_file(project_dir)
    elif system == "Darwin":  # macOS
        create_macos_app()
    elif system == "Windows":
        create_windows_shortcut(project_dir)
    else:
        print_warning(f"Unknown platform: {system}")

def create_launch_script():
    """Create simple launch script"""
    print_info("Creating quick launch script...")
    
    project_dir = Path(__file__).parent.absolute()
    
    if platform.system() != "Windows":
        # Unix-like systems
        launch_script = project_dir / "play.sh"
        launch_script.write_text(f"""#!/bin/bash
cd "$(dirname "$0")"
python3 coin_operated.py
""")
        launch_script.chmod(0o755)
        print_success("Quick launch script created (play.sh)")
    else:
        # Windows
        launch_script = project_dir / "play.bat"
        launch_script.write_text(f"""@echo off
cd /d "%~dp0"
python coin_operated.py
""")
        print_success("Quick launch script created (play.bat)")

def print_completion_message():
    """Print installation complete message"""
    print()
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.GREEN}║{Colors.NC}                                                          {Colors.GREEN}║{Colors.NC}")
    print(f"{Colors.GREEN}║{Colors.NC}              {Colors.BOLD}✨ Installation Complete! ✨{Colors.NC}              {Colors.GREEN}║{Colors.NC}")
    print(f"{Colors.GREEN}║{Colors.NC}                                                          {Colors.GREEN}║{Colors.NC}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════╝{Colors.NC}")
    print()
    print(f"{Colors.BOLD}🎮 You can now launch COIN:OPERATED by:{Colors.NC}")
    print()
    
    system = platform.system()
    if system == "Linux":
        print(f"  {Colors.CYAN}1.{Colors.NC} Opening your {Colors.BOLD}Applications Menu{Colors.NC} and searching for {Colors.YELLOW}COIN:OPERATED{Colors.NC}")
        print(f"  {Colors.CYAN}2.{Colors.NC} Clicking the {Colors.BOLD}Desktop Icon{Colors.NC} (if you created one)")
        print(f"  {Colors.CYAN}3.{Colors.NC} Running: {Colors.YELLOW}./play.sh{Colors.NC}")
    elif system == "Windows":
        print(f"  {Colors.CYAN}1.{Colors.NC} Double-clicking the {Colors.BOLD}Desktop Shortcut{Colors.NC} (if you created one)")
        print(f"  {Colors.CYAN}2.{Colors.NC} Double-clicking {Colors.YELLOW}play.bat{Colors.NC} in this folder")
    else:  # macOS
        print(f"  {Colors.CYAN}1.{Colors.NC} Running: {Colors.YELLOW}./play.sh{Colors.NC}")
    
    print(f"  {Colors.CYAN}4.{Colors.NC} Running: {Colors.YELLOW}python3 coin_operated.py{Colors.NC}")
    print()
    print(f"{Colors.BOLD}🪙 What to expect:{Colors.NC}")
    print("  • Beautiful splash screen with golden Coin logo")
    print("  • 16-bit retro JRPG graphics")
    print("  • Play as Coin - a mystical being made of enchanted coins")
    print("  • No terminal window (pure GUI experience!)")
    print()

def offer_launch():
    """Offer to launch the game"""
    response = input(f"{Colors.YELLOW}Would you like to launch the game now? (y/n): {Colors.NC}").strip().lower()
    
    if response == 'y':
        print()
        print_info("Launching COIN:OPERATED...")
        
        project_dir = Path(__file__).parent.absolute()
        launcher = project_dir / "coin_operated.py"
        
        try:
            if platform.system() == "Windows":
                subprocess.Popen([sys.executable, str(launcher)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, str(launcher)])
            
            print_success("Game launched! Enjoy your journey from coin to goddess!")
        except Exception as e:
            print_error(f"Failed to launch game: {e}")
            print(f"Try running: python3 {launcher}")
    
    print()
    print(f"{Colors.PURPLE}═══════════════════════════════════════════════════════════{Colors.NC}")
    print(f"  {Colors.BOLD}From coin to goddess, from tool to deity{Colors.NC}")
    print(f"  A Universe Beyond the Universe")
    print(f"{Colors.PURPLE}═══════════════════════════════════════════════════════════{Colors.NC}")
    print()

def main():
    """Main installation process"""
    print_banner()
    
    input(f"{Colors.YELLOW}Press Enter to begin installation, or Ctrl+C to cancel{Colors.NC}\n")
    
    # Step 1: Check Python
    if not check_python():
        return 1
    
    # Step 2: Install dependencies
    print()
    if not install_dependencies():
        return 1
    
    # Step 3: Verify installations
    print()
    if not verify_pygame():
        return 1
    
    if not verify_pillow():
        return 1
    
    # Step 4: Create launch scripts
    print()
    create_launch_script()
    
    # Step 5: Setup desktop integration
    print()
    setup_desktop_integration()
    
    # Step 6: Make launcher executable
    print()
    print_info("Making launcher executable...")
    launcher = Path(__file__).parent / "coin_operated.py"
    if launcher.exists() and platform.system() != "Windows":
        launcher.chmod(0o755)
    print_success("Launcher is executable")
    
    # Success!
    print_completion_message()
    offer_launch()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Installation cancelled by user{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
