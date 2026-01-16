"""
Effect Generator - Creates visual effects for magic, combat, and UI
"""

from PIL import Image, ImageDraw
import math
from .color_palette import ColorPalette


class EffectGenerator:
    """Generates visual effects procedurally"""
    
    def __init__(self, size: int = 64):
        self.size = size
        self.palette = ColorPalette
    
    def generate_magic_effect(self, effect_type: str, frame: int, total_frames: int = 12) -> Image:
        """Generate magical effect animation frame"""
        if effect_type == 'time_magic':
            return self._generate_time_effect(frame, total_frames)
        elif effect_type == 'fire':
            return self._generate_fire_effect(frame, total_frames)
        elif effect_type == 'ice':
            return self._generate_ice_effect(frame, total_frames)
        elif effect_type == 'lightning':
            return self._generate_lightning_effect(frame, total_frames)
        elif effect_type == 'healing':
            return self._generate_healing_effect(frame, total_frames)
        elif effect_type == 'dark':
            return self._generate_dark_effect(frame, total_frames)
        else:
            return self._generate_generic_magic(frame, total_frames)
    
    def _generate_time_effect(self, frame: int, total: int) -> Image:
        """Generate time magic effect (clock/spiral)"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        # Rotating clock hands
        color = self.palette.get('magic_time')
        
        # Outer circle
        radius = self.size // 3
        alpha = int(255 * (1 - abs(t - 0.5) * 2))
        circle_color = self.palette.with_alpha(color, alpha)
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=circle_color, width=2)
        
        # Clock hands
        num_hands = 4
        for i in range(num_hands):
            angle = (t * 360 + i * 90) % 360
            rad = math.radians(angle)
            x = center_x + int(math.cos(rad) * radius * 0.8)
            y = center_y + int(math.sin(rad) * radius * 0.8)
            hand_color = self.palette.with_alpha(color, 200)
            draw.line([center_x, center_y, x, y], fill=hand_color, width=2)
        
        # Spiral particles
        num_particles = 8
        for i in range(num_particles):
            spiral_t = (t + i / num_particles) % 1.0
            angle = spiral_t * 360 * 2
            rad = math.radians(angle)
            particle_radius = spiral_t * radius
            x = center_x + int(math.cos(rad) * particle_radius)
            y = center_y + int(math.sin(rad) * particle_radius)
            particle_alpha = int(255 * (1 - spiral_t))
            particle_color = self.palette.with_alpha(color, particle_alpha)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=particle_color)
        
        return img
    
    def _generate_fire_effect(self, frame: int, total: int) -> Image:
        """Generate fire effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        # Multiple flame particles rising
        num_flames = 6
        for i in range(num_flames):
            flame_t = (t + i / num_flames) % 1.0
            x = center_x + int(math.sin(i * 1.5) * 8)
            y = center_y - int(flame_t * self.size * 0.6)
            
            # Flame color gradient (yellow to red to transparent)
            if flame_t < 0.3:
                color = self.palette.get('yellow')
            elif flame_t < 0.6:
                color = self.palette.get('orange')
            else:
                color = self.palette.get('red')
            
            alpha = int(255 * (1 - flame_t))
            flame_color = self.palette.with_alpha(color, alpha)
            
            # Flame shape (teardrop)
            size = int(6 * (1 - flame_t * 0.5))
            draw.ellipse([x - size, y - size * 2, x + size, y + size],
                        fill=flame_color, outline=None)
        
        return img
    
    def _generate_ice_effect(self, frame: int, total: int) -> Image:
        """Generate ice effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        color = self.palette.get('magic_ice')
        
        # Expanding ice crystals
        num_crystals = 6
        for i in range(num_crystals):
            angle = i * 60
            rad = math.radians(angle)
            length = int(t * self.size * 0.4)
            
            x = center_x + int(math.cos(rad) * length)
            y = center_y + int(math.sin(rad) * length)
            
            alpha = int(255 * (1 - t * 0.5))
            crystal_color = self.palette.with_alpha(color, alpha)
            
            # Draw crystal spike
            draw.line([center_x, center_y, x, y], fill=crystal_color, width=3)
            
            # Crystal tip
            draw.polygon([
                (x, y),
                (x + int(math.cos(rad + 0.5) * 4), y + int(math.sin(rad + 0.5) * 4)),
                (x + int(math.cos(rad - 0.5) * 4), y + int(math.sin(rad - 0.5) * 4))
            ], fill=crystal_color)
        
        # Central snowflake
        snowflake_alpha = int(255 * (1 - abs(t - 0.5) * 2))
        snowflake_color = self.palette.with_alpha(color, snowflake_alpha)
        draw.ellipse([center_x - 4, center_y - 4, center_x + 4, center_y + 4],
                    fill=snowflake_color, outline=None)
        
        return img
    
    def _generate_lightning_effect(self, frame: int, total: int) -> Image:
        """Generate lightning effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x = self.size // 2
        t = frame / total
        
        color = self.palette.get('magic_lightning')
        
        # Lightning bolt
        if frame % 3 != 2:  # Flash effect
            points = [(center_x, 0)]
            y = 0
            x = center_x
            
            while y < self.size:
                y += self.size // 6
                x += (hash(f"{frame}_{y}") % 20) - 10
                x = max(5, min(self.size - 5, x))
                points.append((x, y))
            
            # Main bolt
            alpha = 255 if frame % 3 == 0 else 180
            bolt_color = self.palette.with_alpha(color, alpha)
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=bolt_color, width=3)
            
            # Glow around bolt
            glow_color = self.palette.with_alpha(color, 100)
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=glow_color, width=7)
        
        return img
    
    def _generate_healing_effect(self, frame: int, total: int) -> Image:
        """Generate healing effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        color = self.palette.get('magic_healing')
        
        # Floating sparkles moving upward
        num_sparkles = 12
        for i in range(num_sparkles):
            sparkle_t = (t + i / num_sparkles) % 1.0
            angle = i * 30
            rad = math.radians(angle)
            radius = 10 + math.sin(sparkle_t * math.pi) * 5
            
            x = center_x + int(math.cos(rad) * radius)
            y = center_y - int(sparkle_t * self.size * 0.5) + self.size // 4
            
            alpha = int(255 * math.sin(sparkle_t * math.pi))
            sparkle_color = self.palette.with_alpha(color, alpha)
            
            # Draw plus sign
            draw.line([x - 3, y, x + 3, y], fill=sparkle_color, width=2)
            draw.line([x, y - 3, x, y + 3], fill=sparkle_color, width=2)
        
        # Pulsing aura
        pulse = math.sin(t * math.pi * 2) * 0.5 + 0.5
        radius = int(self.size * 0.3 * (1 + pulse * 0.2))
        aura_alpha = int(100 * pulse)
        aura_color = self.palette.with_alpha(color, aura_alpha)
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=aura_color, width=2)
        
        return img
    
    def _generate_dark_effect(self, frame: int, total: int) -> Image:
        """Generate dark magic effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        color = self.palette.get('magic_chaos')
        
        # Swirling dark energy
        num_wisps = 5
        for i in range(num_wisps):
            wisp_t = (t + i / num_wisps) % 1.0
            angle = wisp_t * 360 * 2 + i * 72
            rad = math.radians(angle)
            radius = self.size * 0.3 * (1 - wisp_t * 0.5)
            
            x = center_x + int(math.cos(rad) * radius)
            y = center_y + int(math.sin(rad) * radius)
            
            alpha = int(200 * (1 - wisp_t))
            wisp_color = self.palette.with_alpha(color, alpha)
            
            # Wisp trail
            trail_length = 5
            for j in range(trail_length):
                trail_angle = rad - j * 0.1
                trail_x = x + int(math.cos(trail_angle) * j * 2)
                trail_y = y + int(math.sin(trail_angle) * j * 2)
                trail_alpha = int(alpha * (1 - j / trail_length))
                trail_color = self.palette.with_alpha(color, trail_alpha)
                draw.ellipse([trail_x - 2, trail_y - 2, trail_x + 2, trail_y + 2],
                           fill=trail_color)
        
        return img
    
    def _generate_generic_magic(self, frame: int, total: int) -> Image:
        """Generate generic magic effect"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = self.size // 2, self.size // 2
        t = frame / total
        
        color = self.palette.get('magic_light')
        
        # Expanding rings
        num_rings = 3
        for i in range(num_rings):
            ring_t = (t + i / num_rings) % 1.0
            radius = int(ring_t * self.size * 0.5)
            alpha = int(255 * (1 - ring_t))
            ring_color = self.palette.with_alpha(color, alpha)
            draw.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        outline=ring_color, width=2)
        
        return img
    
    def generate_particle_burst(self, color_name: str, num_particles: int = 20) -> list:
        """Generate particle burst animation"""
        frames = []
        color = self.palette.get(color_name)
        total_frames = 15
        
        for frame in range(total_frames):
            img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            center_x, center_y = self.size // 2, self.size // 2
            t = frame / total_frames
            
            for i in range(num_particles):
                angle = (i / num_particles) * 360
                rad = math.radians(angle)
                distance = t * self.size * 0.4
                
                x = center_x + int(math.cos(rad) * distance)
                y = center_y + int(math.sin(rad) * distance)
                
                # Particle fades out
                alpha = int(255 * (1 - t))
                particle_color = self.palette.with_alpha(color, alpha)
                size = int(3 * (1 - t * 0.5))
                draw.ellipse([x - size, y - size, x + size, y + size],
                           fill=particle_color)
            
            frames.append(img)
        
        return frames
    
    def generate_slash_effect(self, angle: int = 45) -> list:
        """Generate slash/cut effect"""
        frames = []
        total_frames = 8
        
        for frame in range(total_frames):
            img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            t = frame / total_frames
            
            # Slash line
            center_x, center_y = self.size // 2, self.size // 2
            rad = math.radians(angle)
            length = self.size * 0.6 * t
            
            x1 = center_x - int(math.cos(rad) * length / 2)
            y1 = center_y - int(math.sin(rad) * length / 2)
            x2 = center_x + int(math.cos(rad) * length / 2)
            y2 = center_y + int(math.sin(rad) * length / 2)
            
            # Slash color (white to transparent)
            alpha = int(255 * (1 - t))
            slash_color = self.palette.with_alpha(self.palette.get('white'), alpha)
            draw.line([x1, y1, x2, y2], fill=slash_color, width=4)
            
            # Glow
            glow_color = self.palette.with_alpha(self.palette.get('white'), alpha // 2)
            draw.line([x1, y1, x2, y2], fill=glow_color, width=8)
            
            frames.append(img)
        
        return frames
    
    def generate_impact_effect(self) -> list:
        """Generate impact/hit effect"""
        frames = []
        total_frames = 6
        
        for frame in range(total_frames):
            img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            center_x, center_y = self.size // 2, self.size // 2
            t = frame / total_frames
            
            # Expanding circle
            radius = int(t * self.size * 0.4)
            alpha = int(255 * (1 - t))
            color = self.palette.with_alpha(self.palette.get('white'), alpha)
            draw.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        outline=color, width=3)
            
            # Impact lines
            num_lines = 8
            for i in range(num_lines):
                angle = i * 45
                rad = math.radians(angle)
                length = t * 15
                x1 = center_x + int(math.cos(rad) * 8)
                y1 = center_y + int(math.sin(rad) * 8)
                x2 = center_x + int(math.cos(rad) * (8 + length))
                y2 = center_y + int(math.sin(rad) * (8 + length))
                draw.line([x1, y1, x2, y2], fill=color, width=2)
            
            frames.append(img)
        
        return frames
    
    def save_effect_animation(self, frames: list, effect_name: str, directory: str = "generated_effects"):
        """Save effect animation frames"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        saved_files = []
        for i, frame in enumerate(frames):
            filename = f"{effect_name}_frame_{i:02d}.png"
            filepath = os.path.join(directory, filename)
            frame.save(filepath, 'PNG')
            saved_files.append(filepath)
        
        return saved_files
