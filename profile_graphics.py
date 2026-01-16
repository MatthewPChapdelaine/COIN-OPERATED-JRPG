#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Graphics Performance Profiler
Analyzes rendering performance and identifies bottlenecks.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import statistics


# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))


class PerformanceProfiler:
    """Profiler for graphics performance."""
    
    def __init__(self):
        """Initialize profiler."""
        self.timings: Dict[str, List[float]] = {}
        self.current_timers: Dict[str, float] = {}
    
    def start(self, name: str):
        """Start timing an operation."""
        self.current_timers[name] = time.perf_counter()
    
    def stop(self, name: str):
        """Stop timing and record result."""
        if name not in self.current_timers:
            return
        
        elapsed = time.perf_counter() - self.current_timers[name]
        
        if name not in self.timings:
            self.timings[name] = []
        
        self.timings[name].append(elapsed * 1000)  # Convert to ms
        del self.current_timers[name]
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for an operation."""
        if name not in self.timings or not self.timings[name]:
            return {}
        
        values = self.timings[name]
        return {
            'min': min(values),
            'max': max(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'count': len(values)
        }
    
    def print_report(self):
        """Print performance report."""
        print("\n" + "=" * 80)
        print("Performance Profile Report".center(80))
        print("=" * 80)
        
        # Sort by mean time
        operations = sorted(
            self.timings.keys(),
            key=lambda k: statistics.mean(self.timings[k]),
            reverse=True
        )
        
        print(f"\n{'Operation':<30} {'Mean':<10} {'Min':<10} {'Max':<10} {'StdDev':<10}")
        print("-" * 80)
        
        for op in operations:
            stats = self.get_stats(op)
            print(f"{op:<30} {stats['mean']:>8.2f}ms {stats['min']:>8.2f}ms "
                  f"{stats['max']:>8.2f}ms {stats['stdev']:>8.2f}ms")
        
        print("\n" + "=" * 80)


def profile_pygame_renderer(profiler: PerformanceProfiler, frames: int = 100):
    """Profile pygame renderer."""
    print("\nProfiling Pygame Renderer...")
    
    try:
        import pygame
        from graphics.pygame_renderer import PygameRenderer
        from graphics.adapter import GraphicsAdapter
        from unittest.mock import Mock
        
        # Create mock engine
        engine = Mock()
        engine.state = 'in_game'
        engine.player = Mock()
        engine.player.name = "Hero"
        engine.player.stats = Mock()
        engine.player.stats.current_hp = 100
        engine.player.stats.max_hp = 100
        engine.player.stats.level = 5
        engine.party = []
        engine.current_location = Mock()
        engine.current_location.name = "Test Area"
        engine.current_location.description = "A test area"
        engine.current_location.npcs = []
        
        adapter = GraphicsAdapter(engine)
        
        # Initialize pygame
        pygame.init()
        renderer = PygameRenderer(adapter, width=800, height=600)
        
        # Profile rendering
        for i in range(frames):
            profiler.start('pygame_render_frame')
            
            profiler.start('pygame_clear')
            renderer.screen.fill((0, 0, 0))
            profiler.stop('pygame_clear')
            
            profiler.start('pygame_draw_text')
            location = adapter.get_player_location()
            renderer._draw_text(
                location.get('name', 'Unknown'),
                (400, 50),
                renderer.fonts['large'],
                (255, 255, 255)
            )
            profiler.stop('pygame_draw_text')
            
            profiler.start('pygame_display_update')
            pygame.display.flip()
            profiler.stop('pygame_display_update')
            
            profiler.stop('pygame_render_frame')
            
            # Process events to keep window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
        
        pygame.quit()
        print(f"✅ Profiled {frames} frames")
        return True
        
    except Exception as e:
        print(f"❌ Error profiling pygame: {e}")
        return False


def profile_snes_renderer(profiler: PerformanceProfiler, frames: int = 100):
    """Profile Retro16 renderer."""
    print("\nProfiling Retro16 Renderer...")
    
    try:
        import pygame
        from graphics.snes_pygame_renderer import Retro16PygameRenderer
        from graphics.adapter import GraphicsAdapter
        from unittest.mock import Mock
        
        # Create mock engine
        engine = Mock()
        engine.state = 'in_game'
        engine.player = Mock()
        engine.player.name = "Hero"
        engine.player.stats = Mock()
        engine.player.stats.current_hp = 100
        engine.player.stats.max_hp = 100
        engine.player.stats.level = 5
        engine.party = []
        engine.current_location = Mock()
        engine.current_location.name = "Test Area"
        engine.current_location.description = "A test area"
        engine.current_location.npcs = []
        
        adapter = GraphicsAdapter(engine)
        
        # Initialize pygame
        pygame.init()
        renderer = Retro16PygameRenderer(adapter, scale=2)
        
        # Profile rendering
        for i in range(frames):
            profiler.start('retro16_render_frame')
            
            profiler.start('retro16_render')
            renderer._render()
            profiler.stop('retro16_render')
            
            profiler.start('retro16_display_update')
            pygame.display.flip()
            profiler.stop('retro16_display_update')
            
            profiler.stop('retro16_render_frame')
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
        
        pygame.quit()
        print(f"✅ Profiled {frames} frames")
        return True
        
    except Exception as e:
        print(f"❌ Error profiling Retro16: {e}")
        return False


def profile_adapter(profiler: PerformanceProfiler, iterations: int = 1000):
    """Profile adapter operations."""
    print("\nProfiling Graphics Adapter...")
    
    try:
        from graphics.adapter import GraphicsAdapter
        from unittest.mock import Mock
        
        # Create mock engine
        engine = Mock()
        engine.state = 'in_game'
        engine.player = Mock()
        engine.player.name = "Hero"
        engine.player.stats = Mock()
        engine.player.stats.current_hp = 100
        engine.player.stats.max_hp = 100
        engine.party = []
        engine.current_location = Mock()
        engine.current_location.name = "Test Area"
        engine.current_location.description = "A test area"
        engine.current_location.npcs = []
        
        adapter = GraphicsAdapter(engine)
        
        # Profile various operations
        for i in range(iterations):
            profiler.start('adapter_get_location')
            adapter.get_player_location()
            profiler.stop('adapter_get_location')
            
            profiler.start('adapter_get_party')
            adapter.get_party_members()
            profiler.stop('adapter_get_party')
            
            profiler.start('adapter_get_actions')
            adapter.get_available_actions()
            profiler.stop('adapter_get_actions')
            
            profiler.start('adapter_get_state')
            adapter.get_game_state()
            profiler.stop('adapter_get_state')
        
        print(f"✅ Profiled {iterations} iterations")
        return True
        
    except Exception as e:
        print(f"❌ Error profiling adapter: {e}")
        return False


def profile_configuration(profiler: PerformanceProfiler, iterations: int = 1000):
    """Profile configuration operations."""
    print("\nProfiling Configuration System...")
    
    try:
        from config import ConfigManager
        import tempfile
        import shutil
        
        # Create temporary config directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            config = ConfigManager(config_path=Path(temp_dir) / "config.json")
            
            # Profile get operations
            for i in range(iterations):
                profiler.start('config_get')
                config.get('graphics.mode')
                profiler.stop('config_get')
                
                profiler.start('config_get_resolution')
                config.get_resolution()
                profiler.stop('config_get_resolution')
            
            # Profile set operations
            for i in range(iterations // 10):  # Fewer iterations for writes
                profiler.start('config_set')
                config.set('graphics.fps', 60)
                profiler.stop('config_set')
            
            # Profile save operations
            for i in range(10):
                profiler.start('config_save')
                config.save()
                profiler.stop('config_save')
            
            print(f"✅ Profiled configuration system")
            return True
            
        finally:
            shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"❌ Error profiling config: {e}")
        return False


def profile_utils(profiler: PerformanceProfiler, iterations: int = 10000):
    """Profile utility functions."""
    print("\nProfiling Utility Functions...")
    
    try:
        from utils import clamp, lerp, color_lerp, ease_in_out
        
        # Profile clamp
        for i in range(iterations):
            profiler.start('utils_clamp')
            clamp(i, 0, 100)
            profiler.stop('utils_clamp')
        
        # Profile lerp
        for i in range(iterations):
            profiler.start('utils_lerp')
            lerp(0, 100, i / iterations)
            profiler.stop('utils_lerp')
        
        # Profile color_lerp
        for i in range(iterations):
            profiler.start('utils_color_lerp')
            color_lerp((255, 0, 0), (0, 255, 0), i / iterations)
            profiler.stop('utils_color_lerp')
        
        # Profile ease_in_out
        for i in range(iterations):
            profiler.start('utils_ease_in_out')
            ease_in_out(i / iterations)
            profiler.stop('utils_ease_in_out')
        
        print(f"✅ Profiled {iterations} iterations")
        return True
        
    except Exception as e:
        print(f"❌ Error profiling utils: {e}")
        return False


def analyze_bottlenecks(profiler: PerformanceProfiler):
    """Analyze and report bottlenecks."""
    print("\n" + "=" * 80)
    print("Bottleneck Analysis".center(80))
    print("=" * 80)
    
    # Find slowest operations
    slow_ops = []
    for name in profiler.timings:
        stats = profiler.get_stats(name)
        if stats['mean'] > 1.0:  # > 1ms average
            slow_ops.append((name, stats['mean']))
    
    if slow_ops:
        slow_ops.sort(key=lambda x: x[1], reverse=True)
        print("\n⚠️  Operations taking > 1ms on average:")
        for op, mean_time in slow_ops[:5]:  # Top 5
            print(f"   {op}: {mean_time:.2f}ms")
            
            # Provide recommendations
            if 'display_update' in op:
                print("     → Consider VSync or frame limiting")
            elif 'render_frame' in op:
                print("     → Consider reducing draw calls or screen resolution")
            elif 'save' in op:
                print("     → Consider async writes or batching saves")
    else:
        print("\n✅ No significant bottlenecks detected")
    
    # Check for high variance
    high_variance = []
    for name in profiler.timings:
        stats = profiler.get_stats(name)
        if stats.get('stdev', 0) > stats.get('mean', 0):
            high_variance.append((name, stats['stdev'], stats['mean']))
    
    if high_variance:
        print("\n⚠️  Operations with high variance:")
        for op, stdev, mean in high_variance[:5]:
            print(f"   {op}: σ={stdev:.2f}ms, μ={mean:.2f}ms")
            print("     → Inconsistent performance - check for external factors")
    
    print("\n" + "=" * 80)


def main():
    """Run performance profiler."""
    print("\n" + "=" * 80)
    print("COIN-OPERATED JRPG - Graphics Performance Profiler".center(80))
    print("=" * 80)
    
    profiler = PerformanceProfiler()
    
    # Profile each component
    profile_adapter(profiler, iterations=1000)
    profile_configuration(profiler, iterations=1000)
    profile_utils(profiler, iterations=10000)
    
    # Profile renderers (if pygame available)
    try:
        import pygame
        profile_pygame_renderer(profiler, frames=100)
        profile_snes_renderer(profiler, frames=100)
    except ImportError:
        print("\n⚠️  Pygame not available - skipping renderer profiling")
    
    # Print results
    profiler.print_report()
    analyze_bottlenecks(profiler)
    
    print("\n" + "=" * 80)
    print("Profiling Complete".center(80))
    print("=" * 80)


if __name__ == "__main__":
    main()
