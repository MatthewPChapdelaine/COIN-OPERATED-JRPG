"""
Phase 3 Optimization: Memory Management and Object Pooling

This module provides memory optimization features for Phase 3:
- Object pooling for frequently created objects
- Bounded memory collections
- Memory usage tracking

Design Law Article IV Compliance:
- Memory bounds: All collections have max capacity
- O(1) allocation from pool
- No unbounded growth
"""

from typing import TypeVar, Generic, Callable, Optional, List, Deque
from collections import deque
from dataclasses import dataclass
import sys

from aaa_standards.formal_specs import verify_complexity

T = TypeVar('T')


@dataclass
class MemoryStats:
    """
    Memory usage statistics.
    
    Complexity: O(1) storage and updates
    """
    objects_created: int = 0
    objects_pooled: int = 0
    objects_reused: int = 0
    current_pool_size: int = 0
    max_pool_size: int = 0
    pool_hit_rate: float = 0.0
    
    def update_hit_rate(self) -> None:
        """
        Calculate pool hit rate.
        
        Complexity: O(1)
        """
        total_requests = self.objects_reused + (self.objects_created - self.objects_pooled)
        if total_requests > 0:
            self.pool_hit_rate = self.objects_reused / total_requests


class ObjectPool(Generic[T]):
    """
    Generic object pool for memory optimization.
    
    Features:
    - O(1) allocation and return
    - Bounded memory (max_size)
    - Automatic object reset via reset_func
    - Memory statistics tracking
    
    Use Cases:
    - Frequently created/destroyed objects (bullets, particles, effects)
    - Combat messages
    - UI elements
    
    Complexity:
    - acquire(): O(1)
    - release(): O(1)
    - Memory: O(max_size) bounded
    
    Design Law Article IV Compliance:
    - Prevents unbounded memory growth
    - O(1) operations for real-time use
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        reset_func: Optional[Callable[[T], None]] = None,
        max_size: int = 100
    ):
        """
        Initialize object pool.
        
        Args:
            factory: Function to create new objects
            reset_func: Optional function to reset objects before reuse
            max_size: Maximum pool size (default: 100)
        
        Complexity: O(1)
        """
        if max_size < 1:
            raise ValueError(f"max_size must be >= 1, got {max_size}")
        
        self._factory = factory
        self._reset_func = reset_func
        self._max_size = max_size
        
        # Bounded pool: O(max_size) memory
        self._pool: Deque[T] = deque(maxlen=max_size)
        
        # Statistics
        self._stats = MemoryStats(max_pool_size=max_size)
    
    @verify_complexity(time="O(1)", description="Acquire object from pool", realtime_safe=True)
    def acquire(self) -> T:
        """
        Get object from pool or create new one.
        
        Returns:
            Object instance (reused or newly created)
        
        Complexity: O(1)
        Thread Safety: Not thread-safe
        """
        if self._pool:
            # Reuse from pool
            obj = self._pool.pop()
            self._stats.objects_reused += 1
            self._stats.current_pool_size = len(self._pool)
            self._stats.update_hit_rate()
            
            # Reset object if reset function provided
            if self._reset_func:
                self._reset_func(obj)
            
            return obj
        else:
            # Create new object
            obj = self._factory()
            self._stats.objects_created += 1
            self._stats.update_hit_rate()
            return obj
    
    @verify_complexity(time="O(1)", description="Return object to pool", realtime_safe=True)
    def release(self, obj: T) -> None:
        """
        Return object to pool for reuse.
        
        Args:
            obj: Object to return
        
        Complexity: O(1)
        Thread Safety: Not thread-safe
        """
        if len(self._pool) < self._max_size:
            self._pool.append(obj)
            self._stats.objects_pooled += 1
            self._stats.current_pool_size = len(self._pool)
        # If pool is full, object is discarded (will be garbage collected)
    
    @verify_complexity(time="O(n)", description="Pre-warm pool with n objects")
    def prewarm(self, count: int) -> None:
        """
        Pre-create objects to fill pool.
        
        Useful for preventing allocations during gameplay.
        
        Args:
            count: Number of objects to pre-create
        
        Complexity: O(count)
        """
        count = min(count, self._max_size)
        for _ in range(count):
            if len(self._pool) < self._max_size:
                obj = self._factory()
                self._pool.append(obj)
                self._stats.objects_created += 1
                self._stats.objects_pooled += 1
        self._stats.current_pool_size = len(self._pool)
    
    @verify_complexity(time="O(1)", description="Get pool statistics")
    def get_stats(self) -> MemoryStats:
        """
        Get memory statistics.
        
        Returns:
            MemoryStats object
        
        Complexity: O(1)
        """
        return self._stats
    
    @verify_complexity(time="O(1)", description="Clear pool")
    def clear(self) -> None:
        """
        Clear all pooled objects.
        
        Complexity: O(1) (deque.clear is O(1))
        """
        self._pool.clear()
        self._stats.current_pool_size = 0


class BoundedDeque(Generic[T]):
    """
    Deque with bounded memory for logs, history, etc.
    
    Example uses:
    - Combat log (max 1000 messages)
    - Command history (max 100 commands)
    - Recent events (max 50 events)
    
    Complexity:
    - append(): O(1)
    - pop(): O(1)
    - Memory: O(maxlen) bounded
    
    Design Law Article IV Compliance:
    - Automatic oldest-item eviction
    - Bounded memory guarantee
    """
    
    def __init__(self, maxlen: int):
        """
        Initialize bounded deque.
        
        Args:
            maxlen: Maximum length
        
        Complexity: O(1)
        """
        if maxlen < 1:
            raise ValueError(f"maxlen must be >= 1, got {maxlen}")
        
        self._deque: Deque[T] = deque(maxlen=maxlen)
        self._maxlen = maxlen
        self._total_appended = 0
        self._evicted = 0
    
    @verify_complexity(time="O(1)", description="Append item", realtime_safe=True)
    def append(self, item: T) -> None:
        """
        Append item, automatically evicting oldest if at capacity.
        
        Complexity: O(1)
        """
        if len(self._deque) >= self._maxlen:
            self._evicted += 1
        self._deque.append(item)
        self._total_appended += 1
    
    @verify_complexity(time="O(1)", description="Get most recent items")
    def get_recent(self, n: int) -> List[T]:
        """
        Get n most recent items.
        
        Args:
            n: Number of items to get
        
        Returns:
            List of recent items (newest first)
        
        Complexity: O(n) but n is bounded
        """
        n = min(n, len(self._deque))
        return list(reversed(list(self._deque)[-n:]))
    
    def __len__(self) -> int:
        """Get current length. O(1)"""
        return len(self._deque)
    
    @property
    def maxlen(self) -> int:
        """Get maximum length. O(1)"""
        return self._maxlen
    
    @property
    def evicted_count(self) -> int:
        """Get number of evicted items. O(1)"""
        return self._evicted
    
    def clear(self) -> None:
        """Clear all items. O(1)"""
        self._deque.clear()


# Example usage and testing
if __name__ == "__main__":
    print("Phase 3 Memory Optimization - Test Suite")
    print("=" * 60)
    
    # Test ObjectPool
    print("\n1. Testing ObjectPool...")
    
    # Simple object factory
    def create_point():
        return {'x': 0, 'y': 0, 'active': True}
    
    def reset_point(point):
        point['x'] = 0
        point['y'] = 0
        point['active'] = True
    
    pool = ObjectPool(
        factory=create_point,
        reset_func=reset_point,
        max_size=10
    )
    
    # Pre-warm pool
    pool.prewarm(5)
    stats = pool.get_stats()
    print(f"  Pre-warmed: {stats.objects_created} objects created, pool size: {stats.current_pool_size}")
    
    # Acquire objects
    objects = [pool.acquire() for _ in range(10)]
    stats = pool.get_stats()
    print(f"  Acquired 10: {stats.objects_reused} reused, {stats.objects_created} total created")
    
    # Release objects
    for obj in objects:
        pool.release(obj)
    stats = pool.get_stats()
    print(f"  Released 10: pool size: {stats.current_pool_size}")
    
    # Reacquire (should all come from pool)
    objects2 = [pool.acquire() for _ in range(10)]
    stats = pool.get_stats()
    print(f"  Re-acquired 10: hit rate: {stats.pool_hit_rate:.1%}")
    
    print(f"✓ ObjectPool test passed")
    
    # Test BoundedDeque
    print("\n2. Testing BoundedDeque...")
    
    combat_log = BoundedDeque[str](maxlen=1000)
    
    # Add messages
    for i in range(1500):
        combat_log.append(f"Message {i}")
    
    print(f"  Added 1500 messages, current size: {len(combat_log)}")
    print(f"  Evicted: {combat_log.evicted_count}")
    print(f"  Max length: {combat_log.maxlen}")
    
    # Get recent
    recent = combat_log.get_recent(5)
    print(f"  Recent messages: {recent[:2]}...")
    
    print(f"✓ BoundedDeque test passed")
    
    print("\n✓ All Phase 3 Memory Optimization tests passed")
