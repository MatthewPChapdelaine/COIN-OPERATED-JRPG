#!/bin/bash
# Git push script for COIN:OPERATED JRPG

echo "Adding all changes to git..."
git add .

echo ""
echo "Committing changes..."
git commit -m "Add Linux and Steam deployment support

- Added automated Linux setup (setup_linux.sh, launch.sh)
- Added comprehensive verification system (verify.sh, test_system.py)
- Added Steam deployment files (build_steam.sh, Steam VDF configs)
- Added icon generation system (generate_icon.py)
- Added deployment documentation (docs/DEPLOYMENT.md)
- Updated .gitignore for Python artifacts
- Fixed play.py to use python-core directory
- Added MIT License
- Updated README with Linux/Steam instructions

All systems verified and ready for Linux testing and Steam publishing."

echo ""
echo "Pushing to remote..."
git push origin main

echo ""
echo "✓ Push complete!"
