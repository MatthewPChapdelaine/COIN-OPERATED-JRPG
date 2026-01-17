#!/bin/bash
# COIN:OPERATED JRPG - One-Click Installer
# Fully automated setup - no technical knowledge required

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Fancy banner
clear
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}                                                          ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}              ${YELLOW}🪙 COIN:OPERATED JRPG 🪙${NC}                    ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                          ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}            ${CYAN}Automated Installation Wizard${NC}            ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                          ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}This installer will:${NC}"
echo "  ✓ Check system requirements"
echo "  ✓ Install dependencies automatically"
echo "  ✓ Set up desktop integration"
echo "  ✓ Create application menu shortcut"
echo "  ✓ Optionally create desktop icon"
echo ""
echo -e "${YELLOW}Press Enter to begin installation, or Ctrl+C to cancel${NC}"
read -r

# Function to print status
print_status() {
    echo -e "\n${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Step 1: Check Python
print_status "Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check Python version
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]; }; then
    print_error "Python 3.8+ required, but you have $PYTHON_VERSION"
    exit 1
fi

# Step 2: Check pip
print_status "Checking pip installation..."

if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
elif command -v pip &> /dev/null; then
    print_success "pip found"
    alias pip3=pip
else
    print_warning "pip not found, attempting to install..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pip
    else
        print_error "Could not install pip automatically"
        echo "Please install pip3 manually for your distribution"
        exit 1
    fi
fi

# Step 3: Install Python dependencies
print_status "Installing Python dependencies (this may take a minute)..."

if [ -f "requirements.txt" ]; then
    # Try to install without sudo first (user install)
    if pip3 install --user -r requirements.txt > /tmp/coin_install.log 2>&1; then
        print_success "Dependencies installed successfully"
    elif pip3 install -r requirements.txt > /tmp/coin_install.log 2>&1; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        echo "Check /tmp/coin_install.log for details"
        exit 1
    fi
else
    print_error "requirements.txt not found!"
    echo "Please run this script from the COIN-OPERATED-JRPG directory"
    exit 1
fi

# Step 4: Verify pygame installation
print_status "Verifying pygame installation..."

if python3 -c "import pygame" 2>/dev/null; then
    print_success "Pygame is working"
else
    print_warning "Pygame import failed, trying system package..."
    if command -v apt &> /dev/null; then
        sudo apt install -y python3-pygame
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pygame
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pygame
    fi
    
    if python3 -c "import pygame" 2>/dev/null; then
        print_success "Pygame installed via system package"
    else
        print_error "Could not install pygame"
        echo "Try manually: pip3 install pygame"
        exit 1
    fi
fi

# Step 5: Verify Pillow installation
print_status "Verifying Pillow installation..."

if python3 -c "from PIL import Image" 2>/dev/null; then
    print_success "Pillow is working"
else
    print_error "Pillow installation failed"
    echo "Try manually: pip3 install Pillow"
    exit 1
fi

# Step 6: Create desktop file
print_status "Setting up desktop integration..."

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE_CONTENT="[Desktop Entry]
Version=1.0
Type=Application
Name=COIN:OPERATED
Comment=A 16-bit Retro JRPG - Journey from Coin to Time Goddess
Exec=/usr/bin/python3 \"$PROJECT_DIR/coin_operated.py\"
Path=$PROJECT_DIR
Icon=$PROJECT_DIR/assets/icon.png
Terminal=false
Categories=Game;RolePlaying;
Keywords=jrpg;rpg;game;retro;16bit;coin;
StartupNotify=true
StartupWMClass=coin_operated"

# Create applications directory if it doesn't exist
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Write desktop file
echo "$DESKTOP_FILE_CONTENT" > "$APPS_DIR/COIN-OPERATED-JRPG.desktop"
chmod +x "$APPS_DIR/COIN-OPERATED-JRPG.desktop"

print_success "Application menu shortcut created"

# Step 7: Offer to create desktop shortcut
echo ""
echo -e "${YELLOW}Would you like a desktop shortcut? (y/n)${NC}"
read -r CREATE_DESKTOP

if [[ "$CREATE_DESKTOP" =~ ^[Yy]$ ]]; then
    DESKTOP_DIR="$HOME/Desktop"
    if [ -d "$DESKTOP_DIR" ]; then
        cp "$APPS_DIR/COIN-OPERATED-JRPG.desktop" "$DESKTOP_DIR/"
        chmod +x "$DESKTOP_DIR/COIN-OPERATED-JRPG.desktop"
        
        # Try to mark as trusted (varies by desktop environment)
        if command -v gio &> /dev/null; then
            gio set "$DESKTOP_DIR/COIN-OPERATED-JRPG.desktop" "metadata::trusted" yes 2>/dev/null || true
        fi
        
        print_success "Desktop shortcut created"
    else
        print_warning "Desktop directory not found, skipping desktop shortcut"
    fi
fi

# Step 8: Make launcher executable
print_status "Making launcher executable..."
chmod +x "$PROJECT_DIR/coin_operated.py"
print_success "Launcher is executable"

# Step 9: Create quick launch script
print_status "Creating quick launch script..."

cat > "$PROJECT_DIR/play.sh" << 'EOFSCRIPT'
#!/bin/bash
# Quick launch script for COIN:OPERATED
cd "$(dirname "$0")"
python3 coin_operated.py
EOFSCRIPT

chmod +x "$PROJECT_DIR/play.sh"
print_success "Quick launch script created (play.sh)"

# Step 10: Update desktop database
print_status "Updating desktop database..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR" 2>/dev/null || true
    print_success "Desktop database updated"
fi

# Success message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}                                                          ${GREEN}║${NC}"
echo -e "${GREEN}║${NC}              ${BOLD}✨ Installation Complete! ✨${NC}              ${GREEN}║${NC}"
echo -e "${GREEN}║${NC}                                                          ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}🎮 You can now launch COIN:OPERATED by:${NC}"
echo ""
echo -e "  ${CYAN}1.${NC} Opening your ${BOLD}Applications Menu${NC} and searching for ${YELLOW}COIN:OPERATED${NC}"
echo -e "  ${CYAN}2.${NC} Clicking the ${BOLD}Desktop Icon${NC} (if you created one)"
echo -e "  ${CYAN}3.${NC} Running: ${YELLOW}./play.sh${NC}"
echo -e "  ${CYAN}4.${NC} Running: ${YELLOW}python3 coin_operated.py${NC}"
echo ""
echo -e "${BOLD}🪙 What to expect:${NC}"
echo "  • Beautiful splash screen with golden Coin logo"
echo "  • 16-bit retro JRPG graphics"
echo "  • Play as Coin - a mystical being made of enchanted coins"
echo "  • No terminal window (pure GUI experience!)"
echo ""
echo -e "${YELLOW}Would you like to launch the game now? (y/n)${NC}"
read -r LAUNCH_NOW

if [[ "$LAUNCH_NOW" =~ ^[Yy]$ ]]; then
    echo ""
    print_status "Launching COIN:OPERATED..."
    sleep 1
    python3 "$PROJECT_DIR/coin_operated.py" &
    echo ""
    print_success "Game launched! Enjoy your journey from coin to goddess!"
    echo ""
else
    echo ""
    echo -e "${CYAN}Thank you! Launch the game whenever you're ready.${NC}"
    echo ""
fi

echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
echo -e "  ${BOLD}From coin to goddess, from tool to deity${NC}"
echo -e "  ${ITALIC}A Universe Beyond the Universe${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
echo ""
