#!/bin/bash
# COIN:OPERATED JRPG - Linux Setup Script

echo "=========================================="
echo "  COIN:OPERATED JRPG - Linux Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[1/4] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Install with: sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   ✓ Found Python $PYTHON_VERSION"

if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "❌ Error: Python 3.8 or higher required (found $PYTHON_VERSION)"
    exit 1
fi

# Check pip
echo ""
echo "[2/4] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "   Install with: sudo apt install python3-pip"
    exit 1
fi
echo "   ✓ pip3 is installed"

# Install dependencies
echo ""
echo "[3/4] Installing dependencies..."
pip3 install -r requirements.txt --user
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi
echo "   ✓ Dependencies installed"

# Make scripts executable
echo ""
echo "[4/4] Making scripts executable..."
chmod +x play.py
chmod +x graphics_demo.py
chmod +x snes_demo.py
chmod +x test_graphics.py
chmod +x verify.sh
echo "   ✓ Scripts are executable"

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "To play the game:"
echo "  ./play.py"
echo ""
echo "To test graphics system:"
echo "  ./graphics_demo.py      # Modern graphics"
echo "  ./snes_demo.py          # SNES-style graphics"
echo ""
echo "To run tests:"
echo "  ./verify.sh"
echo ""
