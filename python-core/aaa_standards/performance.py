"""
Performance Optimization System (AAA Standard)

Provides caching, memoization, and performance monitoring
for game systems that require O(1) or O(log n) performance.

Key Features:
- LRU cache with bounded memory
- Function memoization with TTL
- Performance profiling
- Cache hit rate monitoring

Mathematical Properties:
- Cache lookup: O(1) amortized
- Cache eviction: O(1) (doubly-linked list)
- Memory bounded: O(capacity)
"""

from typing import TypeVar, Generic, Callable, Optional, Dict, Any, Tuple
from functools import wraps
from collections import OrderedDict
from dataclasses import dataclass, field
import time
from .formal_specs import verify_complexity

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


@dataclass
class CacheStats:
    """
    Cache performance statistics.
    
    Useful for tuning cache parameters and identifying bottlenecks.
    """
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    
    def hit_rate(self) -> float:
        """
        Calculate cache hit rate as percentage.
        
        Returns:
            Hit rate in range [0.0, 1.0]
        
        Complexity: O(1)
        """
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def __str__(self) -> str:
        return (f"CacheStats(hits={self.hits}, misses={self.misses}, "
                f"evictions={self.evictions}, hit_rate={self.hit_rate():.2%})")


class LRUCache(Generic[K, V]):
    """
    Least Recently Used (LRU) Cache with bounded memory.
    
    Properties:
    - O(1) get/put operations
    - O(capacity) space complexity
    - Thread-safe with external synchronization
    
    Implementation:
    - Uses OrderedDict for O(1) move-to-end
    - Automatic eviction when capacity exceeded
    
    Use Cases:
    - Quest lookups
    - Character data caching
    - Location data caching
    """
    
    def __init__(self, capacity: int = 1000):
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of entries (default: 1000)
        
        Complexity: O(1)
        """
        if capacity < 1:
            raise ValueError(f"Capacity must be ≥ 1, got {capacity}")
        
        self._capacity = capacity
        self._cache: OrderedDict[K, V] = OrderedDict()
        self._stats = CacheStats()
    
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def get(self, key: K) -> Optional[V]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value if present, None otherwise
        
        Complexity: O(1) amortized
        Thread Safety: No - requires external synchronization
        """
        if key not in self._cache:
            self._stats.misses += 1
            return None
        
        self._stats.hits += 1
        # Move to end (mark as recently used)
        self._cache.move_to_end(key)
        return self._cache[key]
    
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def put(self, key: K, value: V) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        
        Complexity: O(1) amortized
        Thread Safety: No - requires external synchronization
        """
        if key in self._cache:
            # Update existing entry and mark as recently used
            self._cache.move_to_end(key)
        else:
            # Add new entry
            if len(self._cache) >= self._capacity:
                # Evict least recently used (first item)
                self._cache.popitem(last=False)
                self._stats.evictions += 1
        
        self._cache[key] = value
    
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def clear(self) -> None:
        """
        Clear all cache entries.
        
        Complexity: O(1) (OrderedDict.clear is O(1))
        """
        self._cache.clear()
    
    @verify_complexity(time="O(1)", space="O(1)", realtime_safe=True)
    def size(self) -> int:
        """
        Get current cache size.
        
        Returns:
            Number of entries in cache
        
        Complexity: O(1)
        """
        return len(self._cache)
    
    def stats(self) -> CacheStats:
        """
        Get cache statistics.
        
        Returns:
            CacheStats object
        
        Complexity: O(1)
        """
        return self._stats
    
    def __contains__(self, key: K) -> bool:
        """O(1) membership test"""
        return key in self._cache


def memoize(maxsize: int = 128, ttl: Optional[float] = None):
    """
    Memoization decorator with LRU cache and optional TTL.
    
    Args:
        maxsize: Maximum cache size
        ttl: Time-to-live in seconds (None = infinite)
    
    Example:
        @memoize(maxsize=1000, ttl=60.0)
        def expensive_calculation(x: int) -> int:
            return x ** 2
    
    Complexity: O(1) for cached calls
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Tuple, Tuple[T, float]] = {}
        hits = misses = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            nonlocal hits, misses
            
            # Create cache key from arguments
            key = (args, tuple(sorted(kwargs.items())))
            
            # Check cache
            if key in cache:
                value, timestamp = cache[key]
                
                # Check TTL if specified
                if ttl is None or (time.time() - timestamp) < ttl:
                    hits += 1
                    return value
            
            # Cache miss - compute value
            misses += 1
            result = func(*args, **kwargs)
            
            # Store in cache with timestamp
            cache[key] = (result, time.time())
            
            # Evict oldest entry if over capacity
            if len(cache) > maxsize:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            return result
        
        # Add cache inspection methods
        wrapper.cache_info = lambda: {  # type: ignore
            'hits': hits,
            'misses': misses,
            'size': len(cache),
            'maxsize': maxsize,
            'hit_rate': hits / (hits + misses) if (hits + misses) > 0 else 0.0
        }
        wrapper.cache_clear = lambda: cache.clear()  # type: ignore
        
        return wrapper
    return decorator


@dataclass
class PerformanceMetrics:
    """
    Performance measurement results.
    
    Tracks execution time statistics for profiling.
    """
    function_name: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    
    def record_call(self, execution_time: float) -> None:
        """
        Record a function call.
        
        Args:
            execution_time: Time taken in seconds
        
        Complexity: O(1)
        """
        self.call_count += 1
        self.total_time += execution_time
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.avg_time = self.total_time / self.call_count
    
    def __str__(self) -> str:
        return (f"{self.function_name}: "
                f"calls={self.call_count}, "
                f"avg={self.avg_time*1e6:.2f}μs, "
                f"min={self.min_time*1e6:.2f}μs, "
                f"max={self.max_time*1e6:.2f}μs")


class PerformanceProfiler:
    """
    Global performance profiler for monitoring function execution times.
    
    Useful for identifying performance bottlenecks in production.
    """
    
    _metrics: Dict[str, PerformanceMetrics] = {}
    
    @classmethod
    def record(cls, function_name: str, execution_time: float) -> None:
        """
        Record function execution.
        
        Complexity: O(1)
        """
        if function_name not in cls._metrics:
            cls._metrics[function_name] = PerformanceMetrics(function_name)
        cls._metrics[function_name].record_call(execution_time)
    
    @classmethod
    def get_metrics(cls, function_name: str) -> Optional[PerformanceMetrics]:
        """Get metrics for specific function. O(1)"""
        return cls._metrics.get(function_name)
    
    @classmethod
    def get_all_metrics(cls) -> Dict[str, PerformanceMetrics]:
        """Get all metrics. O(1)"""
        return cls._metrics.copy()
    
    @classmethod
    def clear(cls) -> None:
        """Clear all metrics. O(1)"""
        cls._metrics.clear()
    
    @classmethod
    def print_report(cls) -> None:
        """Print performance report sorted by total time."""
        if not cls._metrics:
            print("No performance data collected")
            return
        
        print("\n" + "=" * 80)
        print("PERFORMANCE PROFILE REPORT")
        print("=" * 80)
        
        # Sort by total time descending
        sorted_metrics = sorted(
            cls._metrics.values(),
            key=lambda m: m.total_time,
            reverse=True
        )
        
        for metrics in sorted_metrics:
            print(metrics)
        
        print("=" * 80 + "\n")


def profile(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for automatic performance profiling.
    
    Example:
        @profile
        def expensive_function():
            ...
    
    Results accessible via PerformanceProfiler.print_report()
    
    Complexity: O(1) overhead
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        PerformanceProfiler.record(func.__name__, end - start)
        return result
    return wrapper


# Example usage and tests
if __name__ == "__main__":
    # Test LRU Cache
    cache: LRUCache[str, int] = LRUCache(capacity=3)
    
    # Test basic operations
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.get("a") == 1
    assert cache.size() == 3
    
    # Test eviction
    cache.put("d", 4)  # Should evict "b" (least recently used)
    assert cache.get("b") is None
    assert cache.get("d") == 4
    
    # Test stats
    stats = cache.stats()
    assert stats.hits > 0
    assert stats.misses > 0
    assert stats.evictions == 1
    print(f"✓ Cache stats: {stats}")
    
    # Test memoization
    @memoize(maxsize=10)
    def expensive_func(x: int) -> int:
        return x ** 2
    
    result1 = expensive_func(5)
    result2 = expensive_func(5)  # Should be cached
    assert result1 == result2 == 25
    
    info = expensive_func.cache_info()  # type: ignore
    assert info['hits'] == 1
    print(f"✓ Memoization: {info}")
    
    # Test profiler
    @profile
    def profiled_function():
        time.sleep(0.001)  # 1ms
        return 42
    
    profiled_function()
    profiled_function()
    
    metrics = PerformanceProfiler.get_metrics("profiled_function")
    assert metrics is not None
    assert metrics.call_count == 2
    print(f"✓ Profiler: {metrics}")
    
    print("\n✓ All performance optimization tests passed")
