"""
Phase 3 Optimization Module

This module contains all Phase 3 optimization implementations:
- Performance monitoring and FPS tracking
- Memory optimization and object pooling
- Profiling utilities
- Bottleneck detection

Design Law Article IV Compliance.
"""

from .performance_monitor import (
    PerformanceMonitor,
    FrameMetrics,
    timed_operation
)

from .memory_optimization import (
    ObjectPool,
    BoundedDeque,
    MemoryStats
)

__all__ = [
    # Performance monitoring
    'PerformanceMonitor',
    'FrameMetrics',
    'timed_operation',
    # Memory optimization
    'ObjectPool',
    'BoundedDeque',
    'MemoryStats',
]
