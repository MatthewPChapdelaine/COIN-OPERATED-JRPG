#!/bin/bash
# COIN:OPERATED JRPG - Comprehensive Verification Script
# Run this to verify all systems are working for Linux and Steam deployment

set -e

echo "========================================"
echo "COIN:OPERATED JRPG - System Verification"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# Check Python version
echo -e "${YELLOW}[1/8]${NC} Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION (>= 3.8 required)"
    else
        echo -e "${RED}✗${NC} Python $PYTHON_VERSION (>= 3.8 required)"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}✗${NC} Python 3 not found"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check dependencies
echo -e "${YELLOW}[2/8]${NC} Checking Python dependencies..."
if python3 -c "import PIL" 2>/dev/null; then
    PIL_VERSION=$(python3 -c "import PIL; print(PIL.__version__)")
    echo -e "${GREEN}✓${NC} Pillow $PIL_VERSION installed"
else
    echo -e "${RED}✗${NC} Pillow not installed (required for graphics)"
    echo "  Install with: pip3 install Pillow>=9.0.0"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check project structure
echo -e "${YELLOW}[3/8]${NC} Checking project structure..."
files=(
    "python-core/main.py"
    "python-core/core/game_engine.py"
    "python-core/core/character.py"
    "python-core/systems/combat.py"
    "python-core/systems/progression.py"
    "python-core/systems/quest.py"
    "python-core/systems/dialogue.py"
    "python-core/systems/save_system.py"
    "python-core/content/act1_content.py"
    "python-core/content/act2_content.py"
    "python-core/content/act3_content.py"
    "python-core/content/act4_content.py"
    "python-core/content/enemies.py"
    "play.py"
    "README.md"
    "LICENSE"
    "requirements.txt"
)

missing=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} Missing: $file"
        missing=$((missing + 1))
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check graphics systems
echo -e "${YELLOW}[4/8]${NC} Checking graphics systems..."
graphics_files=(
    "python-core/graphics/snes_palette.py"
    "python-core/graphics/snes_sprite_generator.py"
    "python-core/graphics/snes_tilemap.py"
    "python-core/graphics/snes_battle_screen.py"
    "python-core/graphics/snes_ui.py"
    "python-core/graphics/snes_renderer.py"
)

for file in "${graphics_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${YELLOW}!${NC} Optional: $file (SNES graphics system)"
    fi
done
echo ""

# Check Steam files
echo -e "${YELLOW}[5/8]${NC} Checking Steam deployment files..."
steam_files=(
    "steam_appid.txt"
    "steam_app_build.vdf"
    "steam_depot_build.vdf"
    "build_steam.sh"
    "generate_icon.py"
)

for file in "${steam_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} Missing: $file"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Test Python syntax
echo -e "${YELLOW}[6/8]${NC} Testing Python syntax..."
SYNTAX_ERRORS=0
for pyfile in $(find python-core -name "*.py" 2>/dev/null); do
    if ! python3 -m py_compile "$pyfile" 2>/dev/null; then
        echo -e "${RED}✗${NC} Syntax error in $pyfile"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
        ERRORS=$((ERRORS + 1))
    fi
done

if [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All Python files have valid syntax"
else
    echo -e "${RED}✗${NC} Found $SYNTAX_ERRORS file(s) with syntax errors"
fi
echo ""

# Test game engine import
echo -e "${YELLOW}[7/8]${NC} Testing game engine..."
if python3 -c "import sys; sys.path.insert(0, 'python-core'); from core.game_engine import GameEngine; print('Game engine loaded successfully')" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Game engine loads successfully"
else
    echo -e "${RED}✗${NC} Game engine failed to load"
    echo "  Try running: python3 -c \"import sys; sys.path.insert(0, 'python-core'); from core.game_engine import GameEngine\""
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check disk space
echo -e "${YELLOW}[8/8]${NC} Checking system resources..."
DISK_AVAILABLE=$(df . | tail -1 | awk '{print $4}')
if [ "$DISK_AVAILABLE" -gt 100000 ]; then
    echo -e "${GREEN}✓${NC} Sufficient disk space available"
else
    echo -e "${YELLOW}!${NC} Low disk space: $(df -h . | tail -1 | awk '{print $4}') available"
fi
echo ""

# Final report
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo "========================================"
    echo ""
    echo "Your game is ready for Linux and Steam!"
    echo ""
    echo "To run the game:"
    echo "  ./setup_linux.sh    # Install dependencies (first time)"
    echo "  python3 play.py     # Start the game"
    echo ""
    echo "To build for Steam:"
    echo "  ./build_steam.sh    # Create Steam build"
    echo ""
    exit 0
else
    echo -e "${RED}✗ FOUND $ERRORS ISSUE(S)${NC}"
    echo "========================================"
    echo ""
    echo "Please fix the issues above before deploying."
    echo ""
    exit 1
fi

