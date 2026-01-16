"""
COIN-OPERATED JRPG: Utilities
Helper functions and utilities for the graphics system.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional


def check_dependencies() -> Tuple[bool, List[str]]:
    """Check if all required dependencies are installed.
    
    Returns:
        (all_installed, missing_packages) tuple
    """
    missing = []
    
    # Check pygame
    try:
        import pygame
    except ImportError:
        missing.append('pygame')
    
    # Check Pillow
    try:
        import PIL
    except ImportError:
        missing.append('Pillow')
    
    return (len(missing) == 0, missing)


def check_graphics_dependencies(mode: str) -> Tuple[bool, List[str]]:
    """Check dependencies for specific graphics mode.
    
    Args:
        mode: 'text', 'graphics', or 'retro16'
        
    Returns:
        (all_installed, missing_packages) tuple
    """
    missing = []
    
    if mode == 'text':
        return (True, [])
    
    # Graphics and Retro16 modes need pygame
    try:
        import pygame
    except ImportError:
        missing.append('pygame')
    
    # Retro16 mode also needs Pillow
    if mode == 'retro16':
        try:
            import PIL
        except ImportError:
            missing.append('Pillow')
    
    return (len(missing) == 0, missing)


def print_dependency_error(missing: List[str]):
    """Print helpful dependency error message.
    
    Args:
        missing: List of missing package names
    """
    print("\n⚠️  ERROR: Missing dependencies")
    print("\nRequired packages not installed:")
    for package in missing:
        print(f"  • {package}")
    
    print("\n📦 Install with:")
    if len(missing) == 1:
        print(f"  pip install {missing[0]}")
    else:
        print(f"  pip install {' '.join(missing)}")
    
    print("\nOr install all dependencies:")
    print("  pip install -r requirements.txt")


def get_project_root() -> Path:
    """Get project root directory.
    
    Returns:
        Path to project root
    """
    # Assuming this file is in python-core/
    return Path(__file__).parent.parent


def setup_python_path():
    """Add python-core to sys.path if not already there."""
    root = get_project_root()
    python_core = root / 'python-core'
    
    if str(python_core) not in sys.path:
        sys.path.insert(0, str(python_core))


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {secs}s"
    
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m {secs}s"


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between two values.
    
    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    return start + (end - start) * clamp(t, 0.0, 1.0)


def ease_in_out(t: float) -> float:
    """Smooth easing function (cubic).
    
    Args:
        t: Input value (0.0 to 1.0)
        
    Returns:
        Eased value (0.0 to 1.0)
    """
    t = clamp(t, 0.0, 1.0)
    if t < 0.5:
        return 4 * t * t * t
    else:
        p = 2 * t - 2
        return 1 + p * p * p / 2


def color_lerp(color1: Tuple[int, int, int], 
               color2: Tuple[int, int, int], 
               t: float) -> Tuple[int, int, int]:
    """Interpolate between two RGB colors.
    
    Args:
        color1: Start color (R, G, B)
        color2: End color (R, G, B)
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated color (R, G, B)
    """
    return (
        int(lerp(color1[0], color2[0], t)),
        int(lerp(color1[1], color2[1], t)),
        int(lerp(color1[2], color2[2], t))
    )


def print_banner(text: str, width: int = 60, char: str = "="):
    """Print a centered banner.
    
    Args:
        text: Text to display
        width: Banner width
        char: Character to use for border
    """
    print(char * width)
    print(text.center(width))
    print(char * width)


def print_box(lines: List[str], width: int = 60, padding: int = 2):
    """Print text in a box.
    
    Args:
        lines: Lines of text to display
        width: Box width
        padding: Padding inside box
    """
    print("┌" + "─" * (width - 2) + "┐")
    
    for line in lines:
        padded_line = " " * padding + line + " " * (width - len(line) - padding - 2)
        print("│" + padded_line + "│")
    
    print("└" + "─" * (width - 2) + "┘")


def validate_mode(mode: str) -> bool:
    """Validate graphics mode.
    
    Args:
        mode: Mode to validate
        
    Returns:
        True if valid, False otherwise
    """
    return mode in ['text', 'graphics', 'retro16']


def get_mode_description(mode: str) -> str:
    """Get description of graphics mode.
    
    Args:
        mode: Graphics mode
        
    Returns:
        Mode description
    """
    descriptions = {
        'text': 'Text-based interactive fiction',
        'graphics': 'Modern 2D graphics renderer',
        'retro16': 'Authentic 16-bit retro graphics'
    }
    return descriptions.get(mode, 'Unknown mode')


def get_mode_requirements(mode: str) -> List[str]:
    """Get requirements for graphics mode.
    
    Args:
        mode: Graphics mode
        
    Returns:
        List of required packages
    """
    requirements = {
        'text': [],
        'graphics': ['pygame'],
        'retro16': ['pygame', 'Pillow']
    }
    return requirements.get(mode, [])


class PerformanceMonitor:
    """Simple performance monitoring."""
    
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60
    
    def record_frame(self, frame_time: float):
        """Record frame time.
        
        Args:
            frame_time: Frame time in seconds
        """
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
    
    def get_average_fps(self) -> float:
        """Get average FPS.
        
        Returns:
            Average FPS over recorded samples
        """
        if not self.frame_times:
            return 0.0
        
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0.0
    
    def get_min_fps(self) -> float:
        """Get minimum FPS.
        
        Returns:
            Minimum FPS over recorded samples
        """
        if not self.frame_times:
            return 0.0
        
        max_time = max(self.frame_times)
        return 1.0 / max_time if max_time > 0 else 0.0
    
    def get_max_fps(self) -> float:
        """Get maximum FPS.
        
        Returns:
            Maximum FPS over recorded samples
        """
        if not self.frame_times:
            return 0.0
        
        min_time = min(self.frame_times)
        return 1.0 / min_time if min_time > 0 else 0.0


# Convenience functions for common operations

def safe_import(module_name: str, package_name: Optional[str] = None) -> Optional[object]:
    """Safely import a module.
    
    Args:
        module_name: Name of module to import
        package_name: Package name (for pip install message)
        
    Returns:
        Imported module or None if failed
    """
    try:
        return __import__(module_name)
    except ImportError:
        pkg_name = package_name or module_name
        print(f"⚠️  Warning: {module_name} not available")
        print(f"   Install with: pip install {pkg_name}")
        return None
