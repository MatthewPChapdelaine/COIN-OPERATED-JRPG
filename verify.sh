#!/bin/bash
# COIN:OPERATED JRPG - Verification Script
# Run this to verify all systems are working

echo "========================================"
echo "COIN:OPERATED JRPG - System Verification"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -eq 0 ]; then
    echo "✅ Python 3 installed"
else
    echo "❌ Python 3 not found"
    exit 1
fi
echo ""

# Check file structure
echo "Checking project structure..."
files=(
    "src/main.py"
    "src/core/game_engine.py"
    "src/core/character.py"
    "src/systems/combat.py"
    "src/systems/progression.py"
    "src/systems/quest.py"
    "src/systems/dialogue.py"
    "src/systems/save_system.py"
    "src/content/act1_content.py"
    "src/content/act2_content.py"
    "src/content/act3_content.py"
    "src/content/act4_content.py"
    "src/content/enemies.py"
    "src/tests/test_game.py"
    "play.py"
    "README.md"
    "docs/DEVELOPMENT.md"
)

missing=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
        missing=$((missing + 1))
    fi
done

if [ $missing -eq 0 ]; then
    echo ""
    echo "✅ All files present!"
else
    echo ""
    echo "❌ $missing files missing"
    exit 1
fi
echo ""

# Run tests
echo "Running automated tests..."
python3 src/tests/test_game.py
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "⚠️ Some tests failed"
fi
echo ""

# Final summary
echo "========================================"
echo "Verification Complete!"
echo "========================================"
echo ""
echo "To play the game, run:"
echo "  python3 play.py"
echo ""
echo "For more information:"
echo "  README.md - Player guide"
echo "  docs/DEVELOPMENT.md - Developer guide"
echo "  COMPLETION_REPORT.md - Project summary"
echo ""
