#!/usr/bin/env python3
"""Fix all absolute imports in aaa_standards module to relative imports."""

import os
import re

# Files to fix
files_to_fix = [
    'python-core/aaa_standards/testing.py',
    'python-core/aaa_standards/interfaces_typed.py'
]

for filepath in files_to_fix:
    full_path = os.path.join('/workspaces/COIN-OPERATED-JRPG', filepath)
    if not os.path.exists(full_path):
        print(f"Skipping {filepath} - not found")
        continue
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    # Replace all absolute imports with relative imports
    # Pattern: from aaa_standards.X import Y -> from .X import Y
    original = content
    content = re.sub(r'from aaa_standards\.(\w+)', r'from .\1', content)
    
    if content != original:
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✓ Fixed imports in {filepath}")
    else:
        print(f"  No changes needed in {filepath}")

print("\n✓ Import fixes complete!")
