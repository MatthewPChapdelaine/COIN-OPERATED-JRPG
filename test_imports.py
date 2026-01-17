#!/usr/bin/env python3
"""Test imports and basic functionality of AAA standards module."""

import sys
import os

# Add python-core to path
sys.path.insert(0, '/workspaces/COIN-OPERATED-JRPG/python-core')

print("Testing AAA Standards Module...")
print("=" * 60)

try:
    # Test 1: Basic imports
    print("\n1. Testing basic imports...")
    from aaa_standards import Result, Ok, Err
    print("   ✓ Result types imported")
    
    from aaa_standards import Position, Location
    print("   ✓ Type definitions imported")
    
    from aaa_standards import FormalStateMachine, GameState
    print("   ✓ State machine imported")
    
    # Test 2: Result type functionality
    print("\n2. Testing Result types...")
    success = Ok(42)
    assert success.is_success()
    assert success.unwrap() == 42
    print("   ✓ Success case works")
    
    failure = Err("error")
    assert failure.is_failure()
    print("   ✓ Failure case works")
    
    # Test 3: Position
    print("\n3. Testing Position...")
    pos = Position(10, 20)
    assert pos.x == 10 and pos.y == 20
    print("   ✓ Position works")
    
    # Test 4: State machine
    print("\n4. Testing FormalStateMachine...")
    fsm = FormalStateMachine()
    assert fsm.current_state == GameState.MAIN_MENU
    print("   ✓ State machine initializes")
    
    # Test 5: Import from interfaces.py
    print("\n5. Testing interfaces.py imports...")
    sys.path.insert(0, '/workspaces/COIN-OPERATED-JRPG/python-core')
    from interfaces import GameStateInterface
    print("   ✓ interfaces.py imports successfully")
    
    # Test 6: Import from game_engine.py
    print("\n6. Testing game_engine.py imports...")
    from core.game_engine import GameEngine
    print("   ✓ game_engine.py imports successfully")
    
    # Test 7: Import from character.py
    print("\n7. Testing character.py imports...")
    from core.character import Character, CharacterRole
    print("   ✓ character.py imports successfully")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n✗ IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n✗ TEST ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
