#!/bin/bash
# Quick start launcher for COIN:OPERATED JRPG
# This script checks dependencies and launches the game

clear

echo "╔══════════════════════════════════════╗"
echo "║     COIN:OPERATED JRPG               ║"
echo "║  A Universe Beyond the Universe      ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required to run this game."
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher is required."
    echo "   Current version: $PYTHON_VERSION"
    echo ""
    echo "Please upgrade Python."
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"

# Check for Pillow
if ! python3 -c "import PIL" 2>/dev/null; then
    echo ""
    echo "⚠️  Pillow (PIL) not found. This is required for graphics."
    echo ""
    echo "Would you like to install it now? (y/n)"
    read -r response
    
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "Installing Pillow..."
        pip3 install Pillow>=9.0.0 --user
        
        if [ $? -eq 0 ]; then
            echo "✓ Pillow installed successfully!"
        else
            echo "❌ Failed to install Pillow."
            echo "   Please run manually: pip3 install Pillow>=9.0.0"
            exit 1
        fi
    else
        echo ""
        echo "⚠️  Warning: Graphics features will not work without Pillow."
        echo "   Install later with: pip3 install Pillow>=9.0.0"
        echo ""
    fi
else
    PIL_VERSION=$(python3 -c "import PIL; print(PIL.__version__)")
    echo "✓ Pillow $PIL_VERSION installed"
fi

echo ""
echo "Starting game..."
echo ""

# Launch the game
python3 play.py

# Exit with the same code as the game
exit $?
