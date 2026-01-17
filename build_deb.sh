#!/bin/bash
# COIN:OPERATED JRPG - Debian Package Builder
# Creates a .deb file for easy installation on Ubuntu/Debian systems

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}              ${YELLOW}🪙 COIN:OPERATED JRPG 🪙${NC}                    ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}             Debian Package Builder (.deb)            ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get version from setup or use default
VERSION="1.0.0"
PACKAGE_NAME="coin-operated-jrpg"
ARCH="all"  # Python is architecture-independent

echo -e "${GREEN}[INFO]${NC} Building ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo ""

# Create package structure
BUILD_DIR="build/debian"
PACKAGE_DIR="${BUILD_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}"

echo -e "${GREEN}[1/8]${NC} Creating package directory structure..."
rm -rf "$BUILD_DIR"
mkdir -p "${PACKAGE_DIR}/DEBIAN"
mkdir -p "${PACKAGE_DIR}/opt/coin-operated"
mkdir -p "${PACKAGE_DIR}/usr/share/applications"
mkdir -p "${PACKAGE_DIR}/usr/share/pixmaps"
mkdir -p "${PACKAGE_DIR}/usr/bin"

# Copy game files
echo -e "${GREEN}[2/8]${NC} Copying game files..."
cp -r python-core "${PACKAGE_DIR}/opt/coin-operated/"
cp coin_operated.py "${PACKAGE_DIR}/opt/coin-operated/"
cp requirements.txt "${PACKAGE_DIR}/opt/coin-operated/"
cp -r assets "${PACKAGE_DIR}/opt/coin-operated/" 2>/dev/null || mkdir -p "${PACKAGE_DIR}/opt/coin-operated/assets"
cp README.md "${PACKAGE_DIR}/opt/coin-operated/"
cp LICENSE "${PACKAGE_DIR}/opt/coin-operated/" 2>/dev/null || echo "MIT License" > "${PACKAGE_DIR}/opt/coin-operated/LICENSE"

# Create launcher script
echo -e "${GREEN}[3/8]${NC} Creating launcher script..."
cat > "${PACKAGE_DIR}/usr/bin/coin-operated" << 'EOF'
#!/bin/bash
# COIN:OPERATED launcher script
cd /opt/coin-operated
python3 coin_operated.py "$@"
EOF
chmod +x "${PACKAGE_DIR}/usr/bin/coin-operated"

# Create desktop file
echo -e "${GREEN}[4/8]${NC} Creating desktop entry..."
cat > "${PACKAGE_DIR}/usr/share/applications/coin-operated.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=COIN:OPERATED
GenericName=16-bit Retro JRPG
Comment=Journey from coin to goddess in this authentic 16-bit JRPG
Exec=coin-operated
Icon=coin-operated
Terminal=false
Categories=Game;RolePlaying;AdventureGame;
Keywords=jrpg;rpg;game;retro;16bit;snes;coin;fantasy;
StartupNotify=true
StartupWMClass=coin_operated
EOF

# Create icon (placeholder if assets don't exist)
echo -e "${GREEN}[5/8]${NC} Adding icon..."
if [ -f "assets/icon.png" ]; then
    cp assets/icon.png "${PACKAGE_DIR}/usr/share/pixmaps/coin-operated.png"
else
    # Create a simple placeholder icon
    echo "Placeholder icon" > "${PACKAGE_DIR}/usr/share/pixmaps/coin-operated.png"
fi

# Create control file
echo -e "${GREEN}[6/8]${NC} Creating package metadata..."
cat > "${PACKAGE_DIR}/DEBIAN/control" << EOF
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: games
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.8), python3-pip, python3-pygame, python3-pil
Maintainer: Loporian Industries <coin-operated@example.com>
Description: COIN:OPERATED - 16-bit Retro JRPG
 Play as Coin, a sentient being made from mystical Domminnian coins.
 Journey from magical artifact to Time Goddess in this authentic
 16-bit JRPG inspired by SNES classics like Final Fantasy VI and
 Chrono Trigger.
 .
 Features:
  * Authentic 16-bit graphics (256x224 resolution)
  * Deep spiritual narrative (Gnostic Christianity & Wiccan themes)
  * Strategic turn-based combat
  * Party system with unique characters
  * Multiple story endings
  * Pure GUI desktop experience
Homepage: https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG
EOF

# Create postinst script (runs after installation)
echo -e "${GREEN}[7/8]${NC} Creating installation scripts..."
cat > "${PACKAGE_DIR}/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user pygame Pillow 2>/dev/null || true

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache /usr/share/pixmaps 2>/dev/null || true
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  COIN:OPERATED JRPG installed successfully!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Launch the game by:"
echo "  • Searching for 'COIN:OPERATED' in your applications menu"
echo "  • Running: coin-operated"
echo ""
echo "🪙 From coin to goddess, from tool to deity 🪙"
echo ""

exit 0
EOF
chmod +x "${PACKAGE_DIR}/DEBIAN/postinst"

# Create prerm script (runs before removal)
cat > "${PACKAGE_DIR}/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

echo "Removing COIN:OPERATED JRPG..."

exit 0
EOF
chmod +x "${PACKAGE_DIR}/DEBIAN/prerm"

# Build the .deb package
echo -e "${GREEN}[8/8]${NC} Building .deb package..."
dpkg-deb --build "${PACKAGE_DIR}"

# Move to root directory
mv "${BUILD_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb" .

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}             ✨ Package Built Successfully! ✨           ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Package created:${NC} ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo ""
echo -e "${BLUE}To install:${NC}"
echo "  sudo dpkg -i ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "  sudo apt-get install -f  # Fix any missing dependencies"
echo ""
echo -e "${BLUE}Or double-click the .deb file in your file manager${NC}"
echo ""
echo -e "${BLUE}To uninstall:${NC}"
echo "  sudo apt remove ${PACKAGE_NAME}"
echo ""
echo -e "${YELLOW}Package size:${NC} $(du -h ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb | cut -f1)"
echo ""
