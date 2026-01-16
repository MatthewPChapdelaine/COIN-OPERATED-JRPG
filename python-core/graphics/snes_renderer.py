"""
SNES Game Renderer - Main rendering engine for SNES-style JRPG
Combines all SNES graphics systems into unified game renderer
"""

from PIL import Image, ImageDraw
from .snes_palette import SNESPalette
from .snes_sprite_generator import SNESSpriteGenerator
from .snes_tilemap import SNESTileGenerator, SNESMapRenderer
from .snes_battle_screen import SNESBattleScreen
from .snes_ui import SNESUI


class SNESGameRenderer:
    """
    Main game renderer for SNES-style JRPG
    Handles all visual rendering at SNES resolution (256x224)
    """
    
    # SNES hardware specs
    SCREEN_WIDTH = 256
    SCREEN_HEIGHT = 224
    TILE_SIZE = 16
    SPRITE_SIZE = 16
    
    def __init__(self):
        self.palette = SNESPalette
        self.sprite_gen = SNESSpriteGenerator(self.SPRITE_SIZE)
        self.map_renderer = SNESMapRenderer(self.TILE_SIZE)
        self.battle_screen = SNESBattleScreen()
        self.ui = SNESUI()
        
        # Cache for commonly used assets
        self.sprite_cache = {}
        self.ui_cache = {}
    
    def get_character_sprite(self, character_name: str) -> Image:
        """Get or generate character sprite"""
        if character_name not in self.sprite_cache:
            if character_name.lower() == 'coin':
                self.sprite_cache[character_name] = self.sprite_gen.generate_coin_sprite()
            elif character_name.lower() == 'jinn_lir':
                self.sprite_cache[character_name] = self.sprite_gen.generate_jinn_lir_sprite()
            elif character_name.lower() == 'coireena':
                self.sprite_cache[character_name] = self.sprite_gen.generate_warrior_sprite()
            elif character_name.lower() in ['orbius', 'selene']:
                color = 'white' if character_name.lower() == 'orbius' else 'purple'
                self.sprite_cache[character_name] = self.sprite_gen.generate_mage_sprite(color)
            else:
                # Default NPC
                self.sprite_cache[character_name] = self.sprite_gen.generate_npc_sprite()
        
        return self.sprite_cache[character_name]
    
    def render_overworld_scene(self, map_data: list, player_x: int, player_y: int,
                               character_name: str = 'coin') -> Image:
        """
        Render overworld scene with player character
        
        map_data: 2D array of tile types
        player_x, player_y: Player position in tiles
        """
        # Calculate viewport (show area around player)
        viewport_width = self.SCREEN_WIDTH // self.TILE_SIZE
        viewport_height = (self.SCREEN_HEIGHT - 64) // self.TILE_SIZE  # Reserve space for UI
        
        # Center camera on player
        camera_x = max(0, min(player_x - viewport_width // 2, len(map_data[0]) - viewport_width))
        camera_y = max(0, min(player_y - viewport_height // 2, len(map_data) - viewport_height))
        
        # Extract visible map section
        visible_map = []
        for y in range(camera_y, min(camera_y + viewport_height, len(map_data))):
            if y < len(map_data):
                row = map_data[y][camera_x:camera_x + viewport_width]
                visible_map.append(row)
        
        # Render map
        map_img = self.map_renderer.render_map(visible_map, viewport_width, len(visible_map))
        
        # Create full screen
        screen = Image.new('RGB', (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (0, 0, 0))
        screen.paste(map_img, (0, 0))
        
        # Draw player sprite
        player_sprite = self.get_character_sprite(character_name)
        player_screen_x = (player_x - camera_x) * self.TILE_SIZE
        player_screen_y = (player_y - camera_y) * self.TILE_SIZE
        
        # Scale sprite 2x for overworld visibility
        scaled_sprite = player_sprite.resize((player_sprite.width * 2, player_sprite.height * 2), Image.NEAREST)
        
        if scaled_sprite.mode == 'RGBA':
            screen.paste(scaled_sprite, (player_screen_x, player_screen_y), scaled_sprite)
        else:
            screen.paste(scaled_sprite, (player_screen_x, player_screen_y))
        
        # Add UI at bottom
        self._add_overworld_ui(screen)
        
        return screen
    
    def _add_overworld_ui(self, screen: Image):
        """Add UI elements to overworld screen"""
        # Status bar at bottom (simple)
        ui_window = self.ui.create_text_window(self.SCREEN_WIDTH, 64, 'simple')
        screen.paste(ui_window, (0, self.SCREEN_HEIGHT - 64), ui_window)
    
    def render_battle(self, party_data: list, enemy_data: list,
                     background: str = 'grassland') -> Image:
        """
        Render battle scene
        
        party_data: List of (character_name, hp, max_hp, mp, max_mp) tuples
        enemy_data: List of (enemy_type, name) tuples
        """
        # Generate sprites
        party_sprites = []
        for char_name, hp, max_hp, mp, max_mp in party_data:
            sprite = self.get_character_sprite(char_name)
            party_sprites.append((sprite, char_name))
        
        enemy_sprites = []
        for enemy_type, name in enemy_data:
            enemy_sprite_gen = SNESSpriteGenerator(24)  # Larger sprites for battle
            sprite = enemy_sprite_gen.generate_enemy_sprite(enemy_type)
            enemy_sprites.append((sprite, name))
        
        # Render battle screen
        battle_img = self.battle_screen.render_battle_screen(
            party_sprites, enemy_sprites, background
        )
        
        return battle_img
    
    def render_menu_screen(self, menu_type: str = 'main', **kwargs) -> Image:
        """
        Render menu screen
        
        menu_type: 'main', 'status', 'item', 'save'
        """
        screen = Image.new('RGB', (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (0, 0, 0))
        
        # Dark background
        draw = ImageDraw.Draw(screen)
        bg_color = self.palette.get('shadow')
        draw.rectangle([0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT], fill=bg_color)
        
        if menu_type == 'main':
            # Main menu
            main_menu = self.ui.create_main_menu(120, 140)
            screen.paste(main_menu, (20, 40), main_menu)
            
            # Status windows for party
            if 'party' in kwargs:
                y_offset = 20
                for i, member in enumerate(kwargs['party'][:3]):
                    status = self.ui.create_status_window(
                        member.get('name', 'Unknown'),
                        member.get('level', 1),
                        member.get('hp', 100),
                        member.get('max_hp', 100),
                        member.get('mp', 50),
                        member.get('max_mp', 50)
                    )
                    screen.paste(status, (self.SCREEN_WIDTH - status.width - 20, y_offset), status)
                    y_offset += status.height + 10
        
        elif menu_type == 'title':
            # Title screen
            title = self.ui.create_title_screen(kwargs.get('title', 'COIN:OPERATED'))
            return title
        
        elif menu_type == 'dialogue':
            # Render scene with dialogue box
            if 'background' in kwargs:
                screen = kwargs['background']
            
            dialogue_box = self.ui.create_dialogue_box(
                self.SCREEN_WIDTH - 32,
                72,
                kwargs.get('speaker', '')
            )
            screen.paste(dialogue_box, (16, self.SCREEN_HEIGHT - 88), dialogue_box)
        
        return screen
    
    def render_transition(self, from_scene: Image, to_scene: Image,
                         transition_type: str = 'fade', progress: float = 0.5) -> Image:
        """
        Render transition between scenes
        
        transition_type: 'fade', 'wipe', 'battle_swirl'
        progress: 0.0 to 1.0
        """
        if transition_type == 'fade':
            # Simple cross-fade
            result = Image.new('RGB', (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (0, 0, 0))
            
            # Blend images
            from_array = from_scene.convert('RGB')
            to_array = to_scene.convert('RGB')
            
            result = Image.blend(from_array, to_array, progress)
            
            return result
        
        elif transition_type == 'wipe':
            # Horizontal wipe
            result = from_scene.copy()
            wipe_x = int(self.SCREEN_WIDTH * progress)
            
            if wipe_x > 0:
                to_crop = to_scene.crop((0, 0, wipe_x, self.SCREEN_HEIGHT))
                result.paste(to_crop, (0, 0))
            
            return result
        
        elif transition_type == 'battle_swirl':
            # Classic battle transition effect (simplified)
            result = from_scene.copy()
            draw = ImageDraw.Draw(result)
            
            # Spiral pattern overlay
            import math
            center_x = self.SCREEN_WIDTH // 2
            center_y = self.SCREEN_HEIGHT // 2
            max_radius = int(min(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) * progress)
            
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                for r in range(0, max_radius, 4):
                    x = int(center_x + r * math.cos(rad))
                    y = int(center_y + r * math.sin(rad))
                    if 0 <= x < self.SCREEN_WIDTH and 0 <= y < self.SCREEN_HEIGHT:
                        # Sample from destination
                        pixel = to_scene.getpixel((x, y))
                        draw.point((x, y), fill=pixel)
            
            return result
        
        return from_scene
    
    def save_scene(self, scene: Image, filename: str, directory: str = "snes_scenes", scale: int = 2):
        """Save rendered scene to file"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        
        # Scale up for better visibility (2x or 3x)
        if scale > 1:
            scaled = scene.resize((scene.width * scale, scene.height * scale), Image.NEAREST)
            scaled.save(filepath, 'PNG')
        else:
            scene.save(filepath, 'PNG')
        
        return filepath
    
    def create_demo_scenes(self, output_dir: str = "snes_demo"):
        """Create demo scenes showcasing all rendering capabilities"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating SNES-style demo scenes...")
        
        # 1. Title screen
        print("  - Title screen")
        title = self.render_menu_screen('title', title='COIN:OPERATED')
        self.save_scene(title, 'title_screen.png', output_dir)
        
        # 2. Overworld scene
        print("  - Overworld scene")
        simple_map = self.map_renderer.create_simple_overworld(20, 20)
        overworld = self.render_overworld_scene(
            [['grass'] * 20 for _ in range(20)],
            10, 10,
            'coin'
        )
        self.save_scene(overworld, 'overworld.png', output_dir)
        
        # 3. Battle scene
        print("  - Battle scene")
        party = [
            ('coin', 85, 100, 30, 50),
            ('jinn_lir', 120, 150, 45, 80)
        ]
        enemies = [
            ('shadow', 'Shadow'),
            ('slime', 'Slime')
        ]
        battle = self.render_battle(party, enemies, 'grassland')
        self.save_scene(battle, 'battle_scene.png', output_dir)
        
        # 4. Menu screen
        print("  - Menu screen")
        menu_party = [
            {'name': 'Coin', 'level': 12, 'hp': 85, 'max_hp': 100, 'mp': 30, 'max_mp': 50},
            {'name': 'Jinn-Lir', 'level': 15, 'hp': 120, 'max_hp': 150, 'mp': 45, 'max_mp': 80},
        ]
        menu = self.render_menu_screen('main', party=menu_party)
        self.save_scene(menu, 'menu_screen.png', output_dir)
        
        print(f"✓ Demo scenes saved to {output_dir}")
        
        return output_dir
