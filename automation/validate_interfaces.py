#!/usr/bin/env python3
"""Verify graphics only uses interface."""

import sys
import re
from pathlib import Path

def validate_interfaces():
    """Check graphics layer uses only interfaces."""
    graphics_dir = Path("python-core/graphics")
    
    if not graphics_dir.exists():
        print("✅ Graphics layer not yet created")
        sys.exit(0)
    
    violations = []
    forbidden = [
        'from core import',
        'from systems import',
        'from content import',
    ]
    
    for py_file in graphics_dir.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        for forbidden_import in forbidden:
            if forbidden_import in content:
                violations.append(f"{py_file}: {forbidden_import}")
    
    if violations:
        print("❌ Interface violations:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("✅ All imports compliant")
        sys.exit(0)

if __name__ == "__main__":
    validate_interfaces()
