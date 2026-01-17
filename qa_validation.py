"""Quick validation of QA fixes"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

print("QA Validation Report")
print("=" * 60)

errors = []

# Test 1: AAA Standards module structure
try:
    from aaa_standards import Result, Ok, Err
    print("✓ Result types import successfully")
except Exception as e:
    errors.append(f"Result types import failed: {e}")
    print(f"✗ Result types: {e}")

try:
    from aaa_standards import Position, Location, CharacterData
    print("✓ Type definitions import successfully")
except Exception as e:
    errors.append(f"Type definitions import failed: {e}")
    print(f"✗ Type definitions: {e}")

try:
    from aaa_standards import FormalStateMachine, GameState
    print("✓ State machine imports successfully")
except Exception as e:
    errors.append(f"State machine import failed: {e}")
    print(f"✗ State machine: {e}")

# Test 2: Core modules
try:
    from interfaces import GameStateInterface
    print("✓ Interfaces module imports successfully")
except Exception as e:
    errors.append(f"Interfaces import failed: {e}")
    print(f"✗ Interfaces: {e}")

try:
    from core.game_engine import GameEngine, GameEngineData
    print("✓ Game engine imports successfully")
except Exception as e:
    errors.append(f"Game engine import failed: {e}")
    print(f"✗ Game engine: {e}")

try:
    from core.character import Character, CharacterRole
    print("✓ Character module imports successfully")
except Exception as e:
    errors.append(f"Character import failed: {e}")
    print(f"✗ Character: {e}")

# Test 3: Functionality tests
try:
    pos = Position(10, 20)
    assert pos.x == 10
    print("✓ Position creation works")
except Exception as e:
    errors.append(f"Position test failed: {e}")
    print(f"✗ Position: {e}")

try:
    result = Ok(42)
    assert result.is_success()
    assert result.unwrap() == 42
    print("✓ Result type functionality works")
except Exception as e:
    errors.append(f"Result functionality failed: {e}")
    print(f"✗ Result functionality: {e}")

try:
    fsm = FormalStateMachine()
    assert fsm.current_state == GameState.MAIN_MENU
    print("✓ State machine initialization works")
except Exception as e:
    errors.append(f"State machine test failed: {e}")
    print(f"✗ State machine: {e}")

print("=" * 60)
if errors:
    print(f"\n❌ {len(errors)} ERRORS FOUND:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    sys.exit(1)
else:
    print("\n✅ ALL QA CHECKS PASSED!")
    sys.exit(0)
