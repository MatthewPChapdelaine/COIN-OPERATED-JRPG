"""
Animation Generator - Creates sprite animations procedurally
"""

from PIL import Image
import math
from .sprite_generator import SpriteGenerator
from .color_palette import ColorPalette


class AnimationGenerator:
    """Generates animated sprite sequences"""
    
    def __init__(self, sprite_gen: SpriteGenerator):
        self.sprite_gen = sprite_gen
        self.palette = ColorPalette
    
    def generate_walk_cycle(self, character_type: str, direction: str = 'down') -> list:
        """Generate 4-frame walk cycle"""
        frames = []
        
        # Frame 1: Left foot forward
        frame1 = self.sprite_gen.create_character_sprite(character_type, direction)
        frame1 = self._apply_walk_offset(frame1, -1, 0, 'left')
        frames.append(frame1)
        
        # Frame 2: Standing
        frame2 = self.sprite_gen.create_character_sprite(character_type, direction)
        frames.append(frame2)
        
        # Frame 3: Right foot forward
        frame3 = self.sprite_gen.create_character_sprite(character_type, direction)
        frame3 = self._apply_walk_offset(frame3, 1, 0, 'right')
        frames.append(frame3)
        
        # Frame 4: Standing
        frame4 = self.sprite_gen.create_character_sprite(character_type, direction)
        frames.append(frame4)
        
        return frames
    
    def _apply_walk_offset(self, img: Image, x_offset: int, y_offset: int, foot: str) -> Image:
        """Apply subtle movement to sprite for walk animation"""
        # Create a slightly modified version for walk cycle
        # This is a simple approach; could be more sophisticated
        new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        new_img.paste(img, (x_offset, y_offset))
        return new_img
    
    def generate_attack_animation(self, character_type: str) -> list:
        """Generate attack animation sequence"""
        frames = []
        
        # Wind-up frame
        frame1 = self.sprite_gen.create_character_sprite(character_type, 'down')
        frames.append(frame1)
        
        # Attack frame (with effect)
        frame2 = self._create_attack_frame(character_type)
        frames.append(frame2)
        
        # Impact frame
        frame3 = self._create_attack_frame(character_type, impact=True)
        frames.append(frame3)
        
        # Recovery frame
        frame4 = self.sprite_gen.create_character_sprite(character_type, 'down')
        frames.append(frame4)
        
        return frames
    
    def _create_attack_frame(self, character_type: str, impact: bool = False) -> Image:
        """Create attack animation frame"""
        base = self.sprite_gen.create_character_sprite(character_type, 'down')
        
        if impact:
            # Add flash effect
            overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
            # Draw impact lines
            from PIL import ImageDraw
            draw = ImageDraw.Draw(overlay)
            center_x, center_y = base.size[0] // 2, base.size[1] // 2
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = center_x + int(math.cos(rad) * 10)
                y1 = center_y + int(math.sin(rad) * 10)
                x2 = center_x + int(math.cos(rad) * 16)
                y2 = center_y + int(math.sin(rad) * 16)
                draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 200), width=2)
            
            base = Image.alpha_composite(base, overlay)
        
        return base
    
    def generate_cast_animation(self, character_type: str, spell_type: str = 'magic') -> list:
        """Generate spell casting animation"""
        frames = []
        
        # Charge up frames (3 frames)
        for i in range(3):
            frame = self._create_cast_frame(character_type, i / 3.0, spell_type)
            frames.append(frame)
        
        # Cast frame
        cast_frame = self._create_cast_frame(character_type, 1.0, spell_type, casting=True)
        frames.append(cast_frame)
        
        # Release frame
        release_frame = self._create_cast_frame(character_type, 0.5, spell_type)
        frames.append(release_frame)
        
        return frames
    
    def _create_cast_frame(self, character_type: str, power: float, spell_type: str, casting: bool = False) -> Image:
        """Create magical casting frame"""
        base = self.sprite_gen.create_character_sprite(character_type, 'down')
        overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(overlay)
        
        # Get spell color
        if spell_type == 'time':
            color = self.palette.get('magic_time')
        elif spell_type == 'fire':
            color = self.palette.get('magic_fire')
        elif spell_type == 'ice':
            color = self.palette.get('magic_ice')
        elif spell_type == 'healing':
            color = self.palette.get('magic_healing')
        else:
            color = self.palette.get('magic_light')
        
        # Draw magical circles around character
        center_x, center_y = base.size[0] // 2, base.size[1] // 2
        num_circles = int(power * 3) + 1
        
        for i in range(num_circles):
            radius = 12 + i * 4 + int(power * 6)
            alpha = int(150 * power) - i * 30
            alpha = max(30, min(200, alpha))
            circle_color = self.palette.with_alpha(color, alpha)
            draw.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        outline=circle_color, width=2)
        
        if casting:
            # Add particles for casting moment
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x = center_x + int(math.cos(rad) * 14)
                y = center_y + int(math.sin(rad) * 14)
                particle_color = self.palette.with_alpha(color, 255)
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=particle_color)
        
        return Image.alpha_composite(base, overlay)
    
    def generate_damage_animation(self, character_type: str) -> list:
        """Generate taking damage animation"""
        frames = []
        
        base_sprite = self.sprite_gen.create_character_sprite(character_type, 'down')
        
        # Flash red frames
        for i in range(3):
            if i % 2 == 0:
                # Red overlay
                frame = self._apply_color_overlay(base_sprite, (255, 0, 0), 0.5)
            else:
                # Normal
                frame = base_sprite
            frames.append(frame)
        
        return frames
    
    def _apply_color_overlay(self, img: Image, color: tuple, alpha: float) -> Image:
        """Apply color overlay to image"""
        overlay = Image.new('RGBA', img.size, color + (int(255 * alpha),))
        return Image.alpha_composite(img, overlay)
    
    def generate_idle_animation(self, character_type: str) -> list:
        """Generate idle breathing/bobbing animation"""
        frames = []
        
        # Create subtle breathing effect (8 frames)
        for i in range(8):
            # Calculate breathing offset (sine wave)
            offset = int(math.sin(i * math.pi / 4) * 1)
            
            base = self.sprite_gen.create_character_sprite(character_type, 'down')
            
            # Apply vertical offset
            new_img = Image.new('RGBA', base.size, (0, 0, 0, 0))
            new_img.paste(base, (0, offset))
            frames.append(new_img)
        
        return frames
    
    def generate_victory_animation(self, character_type: str) -> list:
        """Generate victory/level up animation"""
        frames = []
        
        base = self.sprite_gen.create_character_sprite(character_type, 'down')
        
        # Jump and sparkle effect
        for i in range(12):
            frame = Image.new('RGBA', base.size, (0, 0, 0, 0))
            
            # Calculate jump arc
            t = i / 12.0
            jump_height = int(math.sin(t * math.pi) * 8)
            
            # Paste character at jump position
            frame.paste(base, (0, -jump_height))
            
            # Add sparkles
            overlay = Image.new('RGBA', frame.size, (0, 0, 0, 0))
            from PIL import ImageDraw
            draw = ImageDraw.Draw(overlay)
            
            num_sparkles = 5
            for j in range(num_sparkles):
                angle = (t * 360 + j * 72) % 360
                rad = math.radians(angle)
                radius = 16
                x = frame.size[0] // 2 + int(math.cos(rad) * radius)
                y = frame.size[1] // 2 + int(math.sin(rad) * radius) - jump_height
                
                sparkle_color = self.palette.with_alpha(self.palette.get('yellow'), 255)
                draw.polygon([
                    (x, y - 3),
                    (x + 1, y),
                    (x, y + 3),
                    (x - 1, y)
                ], fill=sparkle_color)
            
            frame = Image.alpha_composite(frame, overlay)
            frames.append(frame)
        
        return frames
    
    def generate_death_animation(self, character_type: str) -> list:
        """Generate defeat/death animation"""
        frames = []
        
        base = self.sprite_gen.create_character_sprite(character_type, 'down')
        
        # Fade and fall animation
        for i in range(8):
            t = i / 8.0
            
            # Create fading sprite
            alpha = int(255 * (1 - t))
            frame = Image.new('RGBA', base.size, (0, 0, 0, 0))
            
            # Apply fade
            faded = Image.new('RGBA', base.size, (0, 0, 0, 0))
            faded.paste(base, (0, int(t * 4)))  # Fall slightly
            
            # Adjust alpha
            for x in range(faded.size[0]):
                for y in range(faded.size[1]):
                    pixel = faded.getpixel((x, y))
                    if pixel[3] > 0:
                        new_alpha = int(pixel[3] * (1 - t))
                        faded.putpixel((x, y), pixel[:3] + (new_alpha,))
            
            frames.append(faded)
        
        return frames
    
    def save_animation(self, frames: list, base_filename: str, directory: str = "generated_animations"):
        """Save animation frames"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        saved_files = []
        for i, frame in enumerate(frames):
            filename = f"{base_filename}_frame_{i:02d}.png"
            filepath = os.path.join(directory, filename)
            frame.save(filepath, 'PNG')
            saved_files.append(filepath)
        
        return saved_files
    
    def create_spritesheet(self, frames: list, columns: int = 4) -> Image:
        """Combine animation frames into a spritesheet"""
        if not frames:
            return None
        
        frame_width, frame_height = frames[0].size
        rows = (len(frames) + columns - 1) // columns
        
        sheet = Image.new('RGBA', 
                         (frame_width * columns, frame_height * rows),
                         (0, 0, 0, 0))
        
        for i, frame in enumerate(frames):
            x = (i % columns) * frame_width
            y = (i // columns) * frame_height
            sheet.paste(frame, (x, y))
        
        return sheet
