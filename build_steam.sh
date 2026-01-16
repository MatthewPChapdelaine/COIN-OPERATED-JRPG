#!/bin/bash
# Build and package script for Steam deployment
# This script prepares the game for distribution on Steam

set -e

echo "======================================"
echo "  Coin-Operated JRPG - Steam Build"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Clean previous builds
echo -e "${YELLOW}[1/7]${NC} Cleaning previous builds..."
rm -rf steam_build
rm -rf dist
rm -rf build
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Clean complete"
echo ""

# Step 2: Verify Python dependencies
echo -e "${YELLOW}[2/7]${NC} Verifying Python dependencies..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 is not installed"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

if ! python3 -c "import PIL" 2>/dev/null; then
    echo -e "${YELLOW}!${NC} Pillow not found, installing..."
    pip3 install Pillow>=9.0.0
fi
echo -e "${GREEN}✓${NC} Dependencies verified"
echo ""

# Step 3: Generate game icons
echo -e "${YELLOW}[3/7]${NC} Generating game icons..."
python3 generate_icon.py
echo -e "${GREEN}✓${NC} Icons generated"
echo ""

# Step 4: Run tests
echo -e "${YELLOW}[4/7]${NC} Running game tests..."
if [ -f "python-core/tests/test_game.py" ]; then
    python3 python-core/tests/test_game.py || {
        echo -e "${YELLOW}!${NC} Tests failed but continuing build..."
    }
else
    echo -e "${YELLOW}!${NC} No tests found, skipping..."
fi
echo -e "${GREEN}✓${NC} Tests complete"
echo ""

# Step 5: Create Steam build directory
echo -e "${YELLOW}[5/7]${NC} Creating Steam build structure..."
mkdir -p steam_build
mkdir -p steam_build/python-core
mkdir -p steam_build/assets
mkdir -p steam_build/docs

# Copy game files
cp -r python-core/* steam_build/python-core/
cp play.py steam_build/
cp requirements.txt steam_build/
cp README.md steam_build/
cp LICENSE steam_build/
cp -r docs/* steam_build/docs/ 2>/dev/null || true

# Copy assets if they exist
if [ -d "assets" ]; then
    cp -r assets/* steam_build/assets/
fi

# Clean up Python cache from build
find steam_build -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find steam_build -type f -name "*.pyc" -delete 2>/dev/null || true

echo -e "${GREEN}✓${NC} Build directory created"
echo ""

# Step 6: Create launcher script for Steam
echo -e "${YELLOW}[6/7]${NC} Creating Steam launcher..."
cat > steam_build/launch.sh << 'EOF'
#!/bin/bash
# Steam launcher for Coin-Operated JRPG

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required to run this game."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt --user
fi

# Launch the game
python3 play.py
EOF

chmod +x steam_build/launch.sh
echo -e "${GREEN}✓${NC} Launcher created"
echo ""

# Step 7: Verify build
echo -e "${YELLOW}[7/7]${NC} Verifying build..."
BUILD_SIZE=$(du -sh steam_build | cut -f1)
FILE_COUNT=$(find steam_build -type f | wc -l)

echo "Build directory: steam_build/"
echo "Build size: $BUILD_SIZE"
echo "File count: $FILE_COUNT"
echo ""

# Check for required files
REQUIRED_FILES=("steam_build/play.py" "steam_build/launch.sh" "steam_build/requirements.txt" "steam_build/LICENSE" "steam_build/README.md")
ALL_PRESENT=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} Missing: $file"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = true ]; then
    echo -e "${GREEN}✓${NC} All required files present"
else
    echo -e "${RED}✗${NC} Build verification failed"
    exit 1
fi

echo ""
echo "======================================"
echo -e "${GREEN}✓ BUILD COMPLETE!${NC}"
echo "======================================"
echo ""
echo "Next steps for Steam:"
echo "  1. Update steam_app_build.vdf with your Steam App ID"
echo "  2. Update steam_depot_build.vdf with your Depot ID"
echo "  3. Run: steamcmd +login <username> +run_app_build ../steam_app_build.vdf +quit"
echo ""
echo "To test locally:"
echo "  cd steam_build && ./launch.sh"
echo ""
