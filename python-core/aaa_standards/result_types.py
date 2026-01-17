"""
Result Types - Monadic Error Handling (AAA Standard)

Replaces exception-based error handling with explicit Result types.
Based on Rust's Result<T, E> pattern.

Complexity: O(1) for all operations
Thread Safety: Immutable, thread-safe
"""

from typing import TypeVar, Generic, Callable, Union
from dataclasses import dataclass
from enum import Enum

T = TypeVar('T')  # Success type
E = TypeVar('E')  # Error type
U = TypeVar('U')  # Mapped type


class ResultType(Enum):
    """Result discriminator"""
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass(frozen=True)
class Success(Generic[T]):
    """
    Success variant of Result type.
    
    Complexity: O(1) construction and access
    Immutable: Yes (frozen dataclass)
    """
    value: T
    result_type: ResultType = ResultType.SUCCESS
    
    def is_success(self) -> bool:
        """O(1) check"""
        return True
    
    def is_failure(self) -> bool:
        """O(1) check"""
        return False
    
    def unwrap(self) -> T:
        """
        Extract value from Success.
        O(1) operation.
        """
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        """O(1) - Returns value, ignores default"""
        return self.value
    
    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        """
        Functor map operation.
        Complexity: O(1) + O(f)
        """
        return Success(f(self.value))
    
    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """
        Monadic bind (>>=) operation.
        Complexity: O(1) + O(f)
        """
        return f(self.value)


@dataclass(frozen=True)
class Failure(Generic[E]):
    """
    Failure variant of Result type.
    
    Complexity: O(1) construction and access
    Immutable: Yes (frozen dataclass)
    """
    error: E
    result_type: ResultType = ResultType.FAILURE
    
    def is_success(self) -> bool:
        """O(1) check"""
        return False
    
    def is_failure(self) -> bool:
        """O(1) check"""
        return True
    
    def unwrap(self) -> T:
        """
        Raises RuntimeError - use is_success() first.
        O(1) operation.
        """
        raise RuntimeError(f"Called unwrap() on Failure: {self.error}")
    
    def unwrap_or(self, default: T) -> T:
        """O(1) - Returns default"""
        return default
    
    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        """
        Functor map - no-op for Failure.
        O(1) operation.
        """
        return self  # type: ignore
    
    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """
        Monadic bind - no-op for Failure.
        O(1) operation.
        """
        return self  # type: ignore


# Type alias for cleaner syntax
Result = Union[Success[T], Failure[E]]


def Ok(value: T) -> Success[T]:
    """
    Convenience constructor for Success.
    O(1) operation.
    """
    return Success(value)


def Err(error: E) -> Failure[E]:
    """
    Convenience constructor for Failure.
    O(1) operation.
    """
    return Failure(error)


# Example usage and tests
if __name__ == "__main__":
    # Example: Division with error handling
    def safe_divide(a: int, b: int) -> Result[float, str]:
        """
        Division with explicit error handling.
        Complexity: O(1)
        """
        if b == 0:
            return Err("Division by zero")
        return Ok(a / b)
    
    # Test cases
    result1 = safe_divide(10, 2)
    assert result1.is_success()
    assert result1.unwrap() == 5.0
    
    result2 = safe_divide(10, 0)
    assert result2.is_failure()
    assert result2.unwrap_or(0.0) == 0.0
    
    # Chaining operations
    result3 = safe_divide(10, 2).map(lambda x: x * 2)
    assert result3.unwrap() == 10.0
    
    print("✓ All Result type tests passed")
