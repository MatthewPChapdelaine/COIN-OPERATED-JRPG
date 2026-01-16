"""
COIN-OPERATED JRPG: SNES-Style Pygame Renderer
Integrates existing SNES graphics system with interface pattern.
Authentic 16-bit graphics with interface-based architecture.
"""

import pygame
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from PIL import Image
import io

# Only import from interfaces
sys.path.insert(0, str(Path(__file__).parent.parent))
from interfaces import GameStateInterface, GameCommandInterface, GameEventInterface

# Import SNES graphics modules
from graphics.snes_renderer import SNESGameRenderer
from graphics.snes_battle_screen import SNESBattleScreen
from graphics.snes_ui import SNESUI


class SNESPygameRenderer(GameEventInterface):
    """SNES-style renderer using pygame + PIL.
    
    Combines authentic SNES graphics generation with pygame display.
    Uses interface pattern for clean separation.
    """
    
    # SNES resolution
    SNES_WIDTH = 256
    SNES_HEIGHT = 224
    SCALE_FACTOR = 3  # Scale up for modern displays
    
    def __init__(self, adapter: GameStateInterface, scale: int = 3):
        """Initialize SNES renderer.
        
        Args:
            adapter: Adapter implementing GameStateInterface
            scale: Scaling factor (3 = 768x672 display)
        """
        pygame.init()
        self.scale = scale
        self.display_width = self.SNES_WIDTH * scale
        self.display_height = self.SNES_HEIGHT * scale
        
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("COIN-OPERATED JRPG - SNES Mode")
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Interface to game logic
        self.adapter = adapter
        
        # SNES graphics generator
        self.snes_renderer = SNESGameRenderer()
        self.snes_battle = SNESBattleScreen()
        self.snes_ui = SNESUI()
        
        # Frame rate (60 FPS for SNES accuracy)
        self.fps = 60
        
        # Message log
        self.messages = []
        self.message_display_time = 180  # 3 seconds at 60fps
        self.message_timer = 0
        
        # Animation state
        self.animation_frame = 0
        self.frame_counter = 0
    
    def run(self):
        """Main game loop."""
        self.running = True
        
        while self.running:
            self._handle_events()
            self._render()
            
            self.frame_counter += 1
            if self.frame_counter % 15 == 0:  # Update every 15 frames
                self.animation_frame = (self.animation_frame + 1) % 4
            
            self.clock.tick(self.fps)
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
    
    def _handle_keypress(self, key: int):
        """Convert keyboard input to game commands."""
        available_actions = self.adapter.get_available_actions()
        
        # Movement
        if key == pygame.K_UP and 'move_up' in available_actions:
            self.adapter.player_move('up')
        elif key == pygame.K_DOWN and 'move_down' in available_actions:
            self.adapter.player_move('down')
        elif key == pygame.K_LEFT and 'move_left' in available_actions:
            self.adapter.player_move('left')
        elif key == pygame.K_RIGHT and 'move_right' in available_actions:
            self.adapter.player_move('right')
        
        # Actions
        elif key == pygame.K_SPACE or key == pygame.K_RETURN:
            if 'interact' in available_actions:
                location = self.adapter.get_player_location()
                if 'nearby_npcs' in location and location['nearby_npcs']:
                    self.adapter.interact_with_npc(location['nearby_npcs'][0])
        
        # Combat actions
        elif key == pygame.K_a and 'attack' in available_actions:
            # Attack first enemy
            encounter = self.adapter.get_current_encounter()
            if encounter and encounter.get('enemies'):
                target_id = encounter['enemies'][0].get('id', 'enemy_0')
                self.adapter.execute_combat_action('attack', target_id)
        
        # Menu
        elif key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_s:
            self.adapter.save_game(1)
            self.messages.append("Game saved!")
            self.message_timer = self.message_display_time
    
    def _render(self):
        """Render current game state in SNES style."""
        # Get game state
        encounter = self.adapter.get_current_encounter()
        
        # Generate SNES graphics
        if encounter:
            pil_image = self._render_snes_combat(encounter)
        else:
            pil_image = self._render_snes_overworld()
        
        # Convert PIL to pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        pygame_surface = pygame.image.fromstring(data, size, mode)
        
        # Scale up for modern display
        scaled_surface = pygame.transform.scale(
            pygame_surface,
            (self.display_width, self.display_height)
        )
        
        # Display
        self.screen.blit(scaled_surface, (0, 0))
        
        # Show messages if any
        if self.message_timer > 0:
            self._render_message_overlay()
            self.message_timer -= 1
        
        pygame.display.flip()
    
    def _render_snes_overworld(self) -> Image:
        """Render overworld in SNES style."""
        # Get location data
        location = self.adapter.get_player_location()
        party = self.adapter.get_party_members()
        
        # Create simple map data (for now)
        # In full implementation, this would come from actual map data
        map_width = 16
        map_height = 14
        map_data = []
        for y in range(map_height):
            row = []
            for x in range(map_width):
                # Simple pattern
                if (x + y) % 3 == 0:
                    row.append('grass')
                elif x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1:
                    row.append('tree')
                else:
                    row.append('grass')
            map_data.append(row)
        
        # Player position (center)
        player_x = map_width // 2
        player_y = map_height // 2
        
        # Get player character name
        character_name = 'coin'
        if party and len(party) > 0:
            character_name = party[0].get('name', 'coin').lower()
        
        # Render using SNES renderer
        try:
            scene = self.snes_renderer.render_overworld_scene(
                map_data, player_x, player_y, character_name
            )
        except:
            # Fallback to simple rendering
            scene = Image.new('RGB', (self.SNES_WIDTH, self.SNES_HEIGHT), (20, 80, 20))
        
        return scene
    
    def _render_snes_combat(self, encounter: Dict[str, Any]) -> Image:
        """Render combat in SNES style."""
        party = self.adapter.get_party_members()
        enemies = encounter.get('enemies', [])
        
        # Prepare party data for SNES renderer
        party_data = []
        for member in party[:4]:  # Max 4 party members
            party_data.append({
                'name': member.get('name', 'Unknown'),
                'hp': member.get('current_hp', 100),
                'max_hp': member.get('max_hp', 100),
                'mp': member.get('current_mp', 50),
                'max_mp': member.get('max_mp', 50),
                'level': member.get('level', 1)
            })
        
        # Prepare enemy data
        enemy_data = []
        for enemy in enemies[:4]:  # Max 4 enemies
            enemy_data.append({
                'name': enemy.get('name', 'Enemy'),
                'hp': enemy.get('current_hp', 100),
                'max_hp': enemy.get('max_hp', 100),
                'type': enemy.get('id', 'unknown')
            })
        
        # Render using SNES battle screen
        try:
            battle_img = self.snes_battle.render_battle_scene(
                party_data, enemy_data, 'grassland'
            )
        except:
            # Fallback to simple rendering
            battle_img = Image.new('RGB', (self.SNES_WIDTH, self.SNES_HEIGHT), (40, 60, 100))
            from PIL import ImageDraw
            draw = ImageDraw.Draw(battle_img)
            draw.text((10, 10), "BATTLE", fill=(255, 255, 255))
        
        return battle_img
    
    def _render_message_overlay(self):
        """Render message box overlay in pygame."""
        if not self.messages:
            return
        
        # Semi-transparent message box
        overlay = pygame.Surface((self.display_width, 80))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, self.display_height - 80))
        
        # Message text
        font = pygame.font.Font(None, 24)
        text = font.render(self.messages[-1], True, (255, 255, 255))
        self.screen.blit(text, (20, self.display_height - 60))
    
    # GameEventInterface implementation
    def on_combat_started(self, encounter_data: Dict[str, Any]) -> None:
        self.messages.append("Battle started!")
        self.message_timer = self.message_display_time
    
    def on_enemy_defeated(self, enemy_id: str) -> None:
        self.messages.append("Enemy defeated!")
        self.message_timer = self.message_display_time
    
    def on_damage_dealt(self, amount: int, target_id: str) -> None:
        self.messages.append(f"{amount} damage!")
        self.message_timer = self.message_display_time
    
    def on_dialogue_displayed(self, dialogue_text: str) -> None:
        self.messages.append(dialogue_text[:50])
        self.message_timer = self.message_display_time
    
    def on_inventory_changed(self, inventory: Dict[str, Any]) -> None:
        pass
    
    def on_level_up(self, character_id: str) -> None:
        self.messages.append("Level up!")
        self.message_timer = self.message_display_time
    
    def on_quest_completed(self, quest_id: str) -> None:
        quest_data = self.adapter.get_quest(quest_id)
        quest_name = quest_data.get('title', 'Quest')
        self.messages.append(f"Quest complete: {quest_name}")
        self.message_timer = self.message_display_time
    
    def on_ending_triggered(self, ending_id: str) -> None:
        self.messages.append("Ending reached!")
        self.message_timer = self.message_display_time
