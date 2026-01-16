#!/usr/bin/env python3
"""
COIN:OPERATED JRPG - Quick Start Script
Run this to start the game
"""

import sys
import os

# Add python-core directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

from main import main

if __name__ == "__main__":
    main()
