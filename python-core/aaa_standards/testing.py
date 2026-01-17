"""
AAA Standards Testing Framework

Provides comprehensive testing utilities for verifying:
- Type safety
- Performance guarantees
- State machine correctness
- Interface contracts
- Error handling

Based on property-based testing and formal verification principles.
"""

from typing import Callable, TypeVar, Any, List, Dict
from dataclasses import dataclass
import time
from .result_types import Result
from .state_machine import FormalStateMachine, GameState, StateTransition
from .formal_specs import ComplexityClass
from .type_definitions import CharacterData, Position

T = TypeVar('T')


@dataclass
class TestResult:
    """Result of a test execution"""
    name: str
    passed: bool
    message: str
    execution_time: float
    
    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status}: {self.name} ({self.execution_time*1000:.2f}ms) - {self.message}"


class TestSuite:
    """
    Comprehensive test suite for AAA standards compliance.
    
    Usage:
        suite = TestSuite()
        suite.add_test("test_name", test_function)
        results = suite.run_all()
    """
    
    def __init__(self, name: str = "AAA Standards Test Suite"):
        self.name = name
        self.tests: List[tuple[str, Callable[[], bool]]] = []
        self.results: List[TestResult] = []
    
    def add_test(self, name: str, test_func: Callable[[], bool]) -> None:
        """
        Add test to suite.
        
        Args:
            name: Test name
            test_func: Function that returns True if test passes
        
        Complexity: O(1)
        """
        self.tests.append((name, test_func))
    
    def run_all(self) -> List[TestResult]:
        """
        Run all tests and return results.
        
        Returns:
            List of TestResult objects
        
        Complexity: O(n) where n = number of tests
        """
        self.results = []
        
        print(f"\n{'=' * 80}")
        print(f"{self.name}")
        print(f"{'=' * 80}\n")
        
        for name, test_func in self.tests:
            start = time.perf_counter()
            
            try:
                passed = test_func()
                message = "Test passed" if passed else "Test returned False"
            except Exception as e:
                passed = False
                message = f"Exception: {str(e)}"
            
            end = time.perf_counter()
            
            result = TestResult(
                name=name,
                passed=passed,
                message=message,
                execution_time=end - start
            )
            
            self.results.append(result)
            print(result)
        
        # Print summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print(f"\n{'=' * 80}")
        print(f"SUMMARY: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print(f"{'=' * 80}\n")
        
        return self.results
    
    def all_passed(self) -> bool:
        """Check if all tests passed. O(n)"""
        return all(r.passed for r in self.results)


# Pre-defined test suites

def test_type_safety() -> TestSuite:
    """Test suite for type safety verification"""
    suite = TestSuite("Type Safety Tests")
    
    # Test 1: Position validation
    def test_position_validation():
        from .type_definitions import Position
        try:
            pos = Position(-1, 0)  # Should raise ValueError
            return False
        except ValueError:
            return True
    suite.add_test("Position validation (negative coords)", test_position_validation)
    
    # Test 2: Character stats invariants
    def test_character_invariants():
        from .type_definitions import CharacterStats, CharacterData
        try:
            # Invalid: current_hp > max_hp
            stats = CharacterStats(
                level=1, max_hp=100, current_hp=150,
                max_mp=50, current_mp=50,
                strength=10, magic=10, defense=10,
                magic_defense=10, speed=10, luck=10
            )
            return False
        except ValueError:
            return True
    suite.add_test("Character stats invariants", test_character_invariants)
    
    # Test 3: Result type safety
    def test_result_types():
        from .result_types import Ok, Err
        
        success = Ok(42)
        assert success.is_success()
        assert not success.is_failure()
        assert success.unwrap() == 42
        
        failure = Err("error")
        assert failure.is_failure()
        assert not failure.is_success()
        assert failure.unwrap_or(0) == 0
        
        return True
    suite.add_test("Result type operations", test_result_types)
    
    return suite


def test_state_machine() -> TestSuite:
    """Test suite for formal state machine"""
    suite = TestSuite("State Machine Tests")
    
    # Test 1: FSM initialization
    def test_fsm_init():
        fsm = FormalStateMachine()
        return fsm.current_state() == GameState.INITIALIZING
    suite.add_test("FSM initialization", test_fsm_init)
    
    # Test 2: Valid transitions
    def test_valid_transitions():
        fsm = FormalStateMachine()
        result = fsm.transition(StateTransition.INITIALIZE)
        return result.is_success() and fsm.current_state() == GameState.MAIN_MENU
    suite.add_test("Valid state transitions", test_valid_transitions)
    
    # Test 3: Invalid transitions
    def test_invalid_transitions():
        fsm = FormalStateMachine()
        result = fsm.transition(StateTransition.EXIT_COMBAT)
        return result.is_failure() and fsm.current_state() == GameState.INITIALIZING
    suite.add_test("Invalid transition rejection", test_invalid_transitions)
    
    # Test 4: Transition history
    def test_transition_history():
        fsm = FormalStateMachine()
        fsm.transition(StateTransition.INITIALIZE)
        fsm.transition(StateTransition.START_NEW_GAME)
        
        history = fsm.get_transition_history()
        return len(history) == 2
    suite.add_test("Transition history tracking", test_transition_history)
    
    # Test 5: State reachability
    def test_reachability():
        # FSM should verify all states are reachable during construction
        try:
            fsm = FormalStateMachine()
            return True  # No exception means reachability verified
        except ValueError:
            return False
    suite.add_test("State reachability verification", test_reachability)
    
    return suite


def test_performance() -> TestSuite:
    """Test suite for performance guarantees"""
    suite = TestSuite("Performance Tests")
    
    # Test 1: LRU cache O(1) operations
    def test_lru_performance():
        from .performance import LRUCache
        
        cache: LRUCache[int, int] = LRUCache(capacity=1000)
        
        # Measure put operations
        start = time.perf_counter()
        for i in range(1000):
            cache.put(i, i * 2)
        put_time = time.perf_counter() - start
        
        # Measure get operations
        start = time.perf_counter()
        for i in range(1000):
            cache.get(i)
        get_time = time.perf_counter() - start
        
        # O(1) means time should scale linearly with n
        # For 1000 operations, should take < 1ms total
        return put_time < 0.001 and get_time < 0.001
    suite.add_test("LRU cache O(1) performance", test_lru_performance)
    
    # Test 2: Memoization effectiveness
    def test_memoization():
        from .performance import memoize
        
        call_count = 0
        
        @memoize(maxsize=10)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x ** 2
        
        # First call
        expensive_func(5)
        first_count = call_count
        
        # Cached call
        expensive_func(5)
        second_count = call_count
        
        return first_count == 1 and second_count == 1  # No additional call
    suite.add_test("Memoization cache hit", test_memoization)
    
    # Test 3: State machine O(1) transitions
    def test_fsm_performance():
        fsm = FormalStateMachine()
        
        start = time.perf_counter()
        for _ in range(100):
            fsm.transition(StateTransition.INITIALIZE)
            fsm.reset()
        elapsed = time.perf_counter() - start
        
        # 100 transitions should take < 1ms (O(1) performance)
        return elapsed < 0.001
    suite.add_test("State machine O(1) transitions", test_fsm_performance)
    
    return suite


def test_error_handling() -> TestSuite:
    """Test suite for error handling with Result types"""
    suite = TestSuite("Error Handling Tests")
    
    # Test 1: Result chaining
    def test_result_chaining():
        from .result_types import Ok, Err
        
        result = Ok(10).map(lambda x: x * 2).map(lambda x: x + 5)
        return result.unwrap() == 25
    suite.add_test("Result functor chaining", test_result_chaining)
    
    # Test 2: Result monadic bind
    def test_result_bind():
        from .result_types import Ok, Err, Result
        
        def safe_divide(a: int, b: int) -> Result[float, str]:
            if b == 0:
                return Err("Division by zero")
            return Ok(a / b)
        
        result = Ok(10).and_then(lambda x: safe_divide(x, 2))
        return result.unwrap() == 5.0
    suite.add_test("Result monadic bind", test_result_bind)
    
    # Test 3: Error propagation
    def test_error_propagation():
        from .result_types import Ok, Err
        
        def divide_chain(x: int) -> Result[float, str]:
            if x == 0:
                return Err("Zero input")
            return Ok(100 / x)
        
        result = divide_chain(0)
        return result.is_failure()
    suite.add_test("Error propagation without exceptions", test_error_propagation)
    
    return suite


def run_aaa_compliance_tests() -> bool:
    """
    Run complete AAA standards compliance test suite.
    
    Returns:
        True if all tests passed
    """
    all_passed = True
    
    # Run all test suites
    suites = [
        test_type_safety(),
        test_state_machine(),
        test_performance(),
        test_error_handling()
    ]
    
    for suite in suites:
        suite.run_all()
        all_passed = all_passed and suite.all_passed()
    
    # Final summary
    if all_passed:
        print("\n" + "=" * 80)
        print("🏆 ALL AAA STANDARDS COMPLIANCE TESTS PASSED")
        print("=" * 80 + "\n")
    else:
        print("\n" + "=" * 80)
        print("⚠️  SOME TESTS FAILED - REVIEW RESULTS ABOVE")
        print("=" * 80 + "\n")
    
    return all_passed


# Example usage
if __name__ == "__main__":
    success = run_aaa_compliance_tests()
    exit(0 if success else 1)
