#!/bin/bash
# COIN:OPERATED JRPG - Universal Package Builder
# Creates distribution packages for multiple formats

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}              ${YELLOW}🪙 COIN:OPERATED JRPG 🪙${NC}                    ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}           Universal Package Builder                  ${CYAN}║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

VERSION="1.0.0"
PACKAGE_NAME="coin-operated-jrpg"

echo "Select package format to build:"
echo ""
echo "  1) .deb (Debian/Ubuntu)"
echo "  2) .rpm (Fedora/RedHat/SUSE)"
echo "  3) .tar.gz (Universal Linux)"
echo "  4) .zip (Windows/Universal)"
echo "  5) .AppImage (Universal Linux)"
echo "  6) All formats"
echo ""
read -p "Enter choice (1-6): " choice

build_deb() {
    echo -e "\n${GREEN}Building Debian package (.deb)...${NC}"
    bash build_deb.sh
}

build_rpm() {
    echo -e "\n${GREEN}Building RPM package (.rpm)...${NC}"
    
    if ! command -v rpmbuild &> /dev/null; then
        echo -e "${RED}Error: rpmbuild not found${NC}"
        echo "Install with: sudo apt install rpm (Debian) or sudo dnf install rpm-build (Fedora)"
        return 1
    fi
    
    # Create RPM build structure
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    
    # Create tarball for sources
    tar czf ~/rpmbuild/SOURCES/${PACKAGE_NAME}-${VERSION}.tar.gz \
        --exclude='.git' \
        --exclude='build' \
        --exclude='*.pyc' \
        --exclude='__pycache__' \
        --transform "s,^,${PACKAGE_NAME}-${VERSION}/," \
        .
    
    # Create spec file
    cat > ~/rpmbuild/SPECS/${PACKAGE_NAME}.spec << EOF
Name:           ${PACKAGE_NAME}
Version:        ${VERSION}
Release:        1%{?dist}
Summary:        16-bit Retro JRPG - Journey from coin to goddess

License:        MIT
URL:            https://github.com/MatthewPChapdelaine/COIN-OPERATED-JRPG
Source0:        %{name}-%{version}.tar.gz

Requires:       python3 >= 3.8
Requires:       python3-pygame
Requires:       python3-pillow

%description
Play as Coin, a sentient being made from mystical Domminnian coins.
Journey from magical artifact to Time Goddess in this authentic 16-bit JRPG.

%prep
%setup -q

%build
# Nothing to build - Python game

%install
rm -rf \$RPM_BUILD_ROOT
mkdir -p \$RPM_BUILD_ROOT/opt/coin-operated
mkdir -p \$RPM_BUILD_ROOT/usr/bin
mkdir -p \$RPM_BUILD_ROOT/usr/share/applications
mkdir -p \$RPM_BUILD_ROOT/usr/share/pixmaps

cp -r * \$RPM_BUILD_ROOT/opt/coin-operated/

cat > \$RPM_BUILD_ROOT/usr/bin/coin-operated << 'EOFSCRIPT'
#!/bin/bash
cd /opt/coin-operated
python3 coin_operated.py "\$@"
EOFSCRIPT
chmod +x \$RPM_BUILD_ROOT/usr/bin/coin-operated

cat > \$RPM_BUILD_ROOT/usr/share/applications/coin-operated.desktop << 'EOFDESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=COIN:OPERATED
Comment=16-bit Retro JRPG
Exec=coin-operated
Icon=coin-operated
Terminal=false
Categories=Game;RolePlaying;
EOFDESKTOP

%files
/opt/coin-operated
/usr/bin/coin-operated
/usr/share/applications/coin-operated.desktop

%changelog
* $(date +'%a %b %d %Y') Builder <coin-operated@example.com> - ${VERSION}-1
- Initial RPM release

EOF
    
    # Build RPM
    rpmbuild -ba ~/rpmbuild/SPECS/${PACKAGE_NAME}.spec
    
    # Copy to current directory
    cp ~/rpmbuild/RPMS/noarch/${PACKAGE_NAME}-${VERSION}-*.rpm .
    echo -e "${GREEN}RPM package created!${NC}"
}

build_tarball() {
    echo -e "\n${GREEN}Building tarball (.tar.gz)...${NC}"
    
    BUILD_DIR="build/tarball"
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}"
    
    # Copy all necessary files
    cp -r python-core "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp coin_operated.py "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp requirements.txt "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp -r assets "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    cp README.md "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp LICENSE "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    cp setup.sh "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp auto_setup.py "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    
    # Create install script
    cat > "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/INSTALL.txt" << 'EOF'
COIN:OPERATED JRPG - Installation Instructions

1. Ensure Python 3.8+ is installed:
   python3 --version

2. Run the automated installer:
   bash setup.sh
   
   Or manual installation:
   pip3 install -r requirements.txt
   python3 coin_operated.py

3. Enjoy the game!

For more information, see README.md
EOF
    
    # Create tarball
    cd "$BUILD_DIR"
    tar czf "${PACKAGE_NAME}-${VERSION}.tar.gz" "${PACKAGE_NAME}-${VERSION}"
    cd - > /dev/null
    
    mv "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}.tar.gz" .
    echo -e "${GREEN}Tarball created: ${PACKAGE_NAME}-${VERSION}.tar.gz${NC}"
}

build_zip() {
    echo -e "\n${GREEN}Building ZIP archive (.zip)...${NC}"
    
    BUILD_DIR="build/zip"
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}"
    
    # Copy all files
    cp -r python-core "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp coin_operated.py "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp requirements.txt "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp -r assets "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    cp README.md "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp LICENSE "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    cp setup.bat "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    cp auto_setup.py "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/"
    
    # Create Windows README
    cat > "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}/INSTALL.txt" << 'EOF'
COIN:OPERATED JRPG - Windows Installation

1. Install Python 3.8+ from: https://www.python.org/downloads/
   (Make sure to check "Add Python to PATH"!)

2. Double-click setup.bat
   OR run: python auto_setup.py

3. Play the game!

Launch by:
  - Desktop shortcut (if created)
  - Double-clicking play.bat
  - Running: python coin_operated.py

For more info, see README.md
EOF
    
    # Create ZIP
    cd "$BUILD_DIR"
    zip -r "${PACKAGE_NAME}-${VERSION}.zip" "${PACKAGE_NAME}-${VERSION}" -q
    cd - > /dev/null
    
    mv "$BUILD_DIR/${PACKAGE_NAME}-${VERSION}.zip" .
    echo -e "${GREEN}ZIP archive created: ${PACKAGE_NAME}-${VERSION}.zip${NC}"
}

build_appimage() {
    echo -e "\n${GREEN}Building AppImage...${NC}"
    echo -e "${YELLOW}Note: AppImage build requires additional tools${NC}"
    
    if ! command -v appimagetool &> /dev/null; then
        echo -e "${RED}Error: appimagetool not found${NC}"
        echo "Download from: https://appimage.github.io/appimagetool/"
        return 1
    fi
    
    BUILD_DIR="build/appimage"
    APP_DIR="${BUILD_DIR}/CoinOperated.AppDir"
    
    rm -rf "$BUILD_DIR"
    mkdir -p "$APP_DIR/usr/bin"
    mkdir -p "$APP_DIR/usr/share/applications"
    mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"
    mkdir -p "$APP_DIR/opt/coin-operated"
    
    # Copy game files
    cp -r python-core "$APP_DIR/opt/coin-operated/"
    cp coin_operated.py "$APP_DIR/opt/coin-operated/"
    cp requirements.txt "$APP_DIR/opt/coin-operated/"
    
    # Create AppRun script
    cat > "$APP_DIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
cd "${HERE}/opt/coin-operated"
exec python3 coin_operated.py "$@"
EOF
    chmod +x "$APP_DIR/AppRun"
    
    # Create desktop file
    cp "${PACKAGE_DIR}/usr/share/applications/coin-operated.desktop" "$APP_DIR/" 2>/dev/null || \
    cat > "$APP_DIR/coin-operated.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=COIN:OPERATED
Exec=coin-operated
Icon=coin-operated
Categories=Game;
EOF
    
    # Create icon
    cp assets/icon.png "$APP_DIR/coin-operated.png" 2>/dev/null || \
    echo "Icon" > "$APP_DIR/coin-operated.png"
    
    # Build AppImage
    appimagetool "$APP_DIR" "${PACKAGE_NAME}-${VERSION}-x86_64.AppImage"
    
    echo -e "${GREEN}AppImage created: ${PACKAGE_NAME}-${VERSION}-x86_64.AppImage${NC}"
}

# Execute based on choice
case $choice in
    1)
        build_deb
        ;;
    2)
        build_rpm
        ;;
    3)
        build_tarball
        ;;
    4)
        build_zip
        ;;
    5)
        build_appimage
        ;;
    6)
        echo -e "${YELLOW}Building all package formats...${NC}"
        build_deb || true
        build_rpm || true
        build_tarball || true
        build_zip || true
        build_appimage || true
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}              Package Build Complete!                  ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Available packages:"
ls -lh ${PACKAGE_NAME}* 2>/dev/null || echo "See build/ directory"
echo ""
