"""
COIN-OPERATED JRPG: Pygame Graphics Renderer
Main graphics renderer implementing interface pattern.
NO direct imports from game logic - only through interfaces.
"""

import pygame
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

# Only import from interfaces - NEVER from core/systems/content
sys.path.insert(0, str(Path(__file__).parent.parent))
from interfaces import GameStateInterface, GameCommandInterface, GameEventInterface


class PygameRenderer(GameEventInterface):
    """Main pygame renderer - receives game state via interface."""
    
    def __init__(self, adapter: GameStateInterface, width: int = 800, height: int = 600):
        """Initialize pygame renderer.
        
        Args:
            adapter: Adapter implementing GameStateInterface
            width: Screen width
            height: Screen height
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("COIN-OPERATED JRPG")
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Interface to game logic
        self.adapter = adapter
        
        # Visual settings
        self.width = width
        self.height = height
        self.fps = 60
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.YELLOW = (255, 255, 0)
        
        # Font
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Current display state
        self.messages = []
        self.current_menu = None
        
    def run(self):
        """Main game loop."""
        self.running = True
        
        while self.running:
            # Handle events
            self._handle_events()
            
            # Render current state
            self._render()
            
            # Control frame rate
            self.clock.tick(self.fps)
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events and convert to game commands."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
    
    def _handle_keypress(self, key: int):
        """Convert keyboard input to game commands.
        
        Args:
            key: Pygame key constant
        """
        # Get current game state to determine valid actions
        available_actions = self.adapter.get_available_actions()
        
        # Movement commands
        if key == pygame.K_UP and 'move_up' in available_actions:
            self.adapter.player_move('up')
        elif key == pygame.K_DOWN and 'move_down' in available_actions:
            self.adapter.player_move('down')
        elif key == pygame.K_LEFT and 'move_left' in available_actions:
            self.adapter.player_move('left')
        elif key == pygame.K_RIGHT and 'move_right' in available_actions:
            self.adapter.player_move('right')
        
        # Interaction
        elif key == pygame.K_SPACE and 'interact' in available_actions:
            # Get nearby NPCs from game state
            location = self.adapter.get_player_location()
            if 'nearby_npcs' in location and location['nearby_npcs']:
                npc_id = location['nearby_npcs'][0]
                self.adapter.interact_with_npc(npc_id)
        
        # Menu
        elif key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_i and 'inventory' in available_actions:
            # Toggle inventory view
            pass
        elif key == pygame.K_s and 'save' in available_actions:
            self.adapter.save_game(1)
    
    def _render(self):
        """Render current game state."""
        self.screen.fill(self.BLACK)
        
        # Get current game state via interface
        encounter = self.adapter.get_current_encounter()
        
        if encounter:
            self._render_combat(encounter)
        else:
            self._render_overworld()
        
        # Render UI elements
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_overworld(self):
        """Render overworld/exploration view."""
        # Get location data from game logic
        location = self.adapter.get_player_location()
        party = self.adapter.get_party_members()
        
        # Render location name
        if location and 'name' in location:
            location_text = self.font_medium.render(
                location['name'], True, self.WHITE
            )
            self.screen.blit(location_text, (20, 20))
        
        # Render player sprite (center of screen)
        if party and len(party) > 0:
            player = party[0]
            player_rect = pygame.Rect(
                self.width // 2 - 16,
                self.height // 2 - 16,
                32, 32
            )
            pygame.draw.rect(self.screen, self.BLUE, player_rect)
            
            # Player name
            name_text = self.font_small.render(
                player.get('name', 'Player'), True, self.WHITE
            )
            self.screen.blit(name_text, (player_rect.x - 20, player_rect.y - 25))
        
        # Render location description
        if location and 'description' in location:
            desc_text = self.font_small.render(
                location['description'][:60], True, self.GRAY
            )
            self.screen.blit(desc_text, (20, self.height - 100))
    
    def _render_combat(self, encounter: Dict[str, Any]):
        """Render combat screen.
        
        Args:
            encounter: Combat encounter data from game logic
        """
        # Title
        title = self.font_large.render("COMBAT", True, self.RED)
        self.screen.blit(title, (self.width // 2 - 80, 20))
        
        # Party (left side)
        party = self.adapter.get_party_members()
        y_pos = 100
        for i, member in enumerate(party):
            # Character box
            char_rect = pygame.Rect(50, y_pos + i * 80, 250, 70)
            pygame.draw.rect(self.screen, self.GREEN, char_rect, 2)
            
            # Name
            name = self.font_medium.render(
                member.get('name', 'Unknown'), True, self.WHITE
            )
            self.screen.blit(name, (60, y_pos + i * 80 + 10))
            
            # HP bar
            max_hp = member.get('max_hp', 100)
            current_hp = member.get('current_hp', max_hp)
            hp_ratio = current_hp / max_hp if max_hp > 0 else 0
            
            hp_bar_width = 200
            hp_bar = pygame.Rect(60, y_pos + i * 80 + 40, int(hp_bar_width * hp_ratio), 10)
            pygame.draw.rect(self.screen, self.GREEN, hp_bar)
            pygame.draw.rect(self.screen, self.WHITE, 
                           pygame.Rect(60, y_pos + i * 80 + 40, hp_bar_width, 10), 1)
            
            hp_text = self.font_small.render(
                f"{current_hp}/{max_hp}", True, self.WHITE
            )
            self.screen.blit(hp_text, (60, y_pos + i * 80 + 52))
        
        # Enemies (right side)
        if 'enemies' in encounter:
            y_pos = 100
            for i, enemy in enumerate(encounter['enemies']):
                # Enemy box
                enemy_rect = pygame.Rect(self.width - 300, y_pos + i * 80, 250, 70)
                pygame.draw.rect(self.screen, self.RED, enemy_rect, 2)
                
                # Name
                name = self.font_medium.render(
                    enemy.get('name', 'Enemy'), True, self.WHITE
                )
                self.screen.blit(name, (self.width - 290, y_pos + i * 80 + 10))
                
                # HP bar
                max_hp = enemy.get('max_hp', 100)
                current_hp = enemy.get('current_hp', max_hp)
                hp_ratio = current_hp / max_hp if max_hp > 0 else 0
                
                hp_bar_width = 200
                hp_bar = pygame.Rect(
                    self.width - 290, 
                    y_pos + i * 80 + 40, 
                    int(hp_bar_width * hp_ratio), 
                    10
                )
                pygame.draw.rect(self.screen, self.RED, hp_bar)
                pygame.draw.rect(self.screen, self.WHITE, 
                               pygame.Rect(self.width - 290, y_pos + i * 80 + 40, 
                                         hp_bar_width, 10), 1)
                
                hp_text = self.font_small.render(
                    f"{current_hp}/{max_hp}", True, self.WHITE
                )
                self.screen.blit(hp_text, (self.width - 290, y_pos + i * 80 + 52))
        
        # Combat actions (bottom)
        actions = self.adapter.get_available_actions()
        action_y = self.height - 120
        
        action_text = self.font_small.render(
            "Actions: [A]ttack [S]kill [I]tem [D]efend", True, self.YELLOW
        )
        self.screen.blit(action_text, (20, action_y))
    
    def _render_ui(self):
        """Render UI overlay elements."""
        # Get UI elements from game logic
        ui_elements = self.adapter.get_ui_elements()
        
        # Render messages/dialogue
        if 'messages' in ui_elements and ui_elements['messages']:
            message_box = pygame.Rect(50, self.height - 150, self.width - 100, 130)
            pygame.draw.rect(self.screen, self.BLACK, message_box)
            pygame.draw.rect(self.screen, self.WHITE, message_box, 2)
            
            y_offset = self.height - 140
            for msg in ui_elements['messages'][-3:]:  # Last 3 messages
                text = self.font_small.render(msg, True, self.WHITE)
                self.screen.blit(text, (60, y_offset))
                y_offset += 30
        
        # Render current menu if any
        if 'current_menu' in ui_elements and ui_elements['current_menu']:
            self._render_menu(ui_elements['current_menu'])
    
    def _render_menu(self, menu_data: Dict[str, Any]):
        """Render menu overlay.
        
        Args:
            menu_data: Menu configuration from game logic
        """
        menu_width = 400
        menu_height = 300
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, self.BLACK, menu_rect)
        pygame.draw.rect(self.screen, self.WHITE, menu_rect, 3)
        
        # Menu title
        title = self.font_medium.render(
            menu_data.get('title', 'Menu'), True, self.WHITE
        )
        self.screen.blit(title, (menu_x + 20, menu_y + 20))
        
        # Menu options
        if 'options' in menu_data:
            y_offset = menu_y + 70
            for i, option in enumerate(menu_data['options']):
                option_text = self.font_small.render(
                    f"{i + 1}. {option}", True, self.WHITE
                )
                self.screen.blit(option_text, (menu_x + 30, y_offset))
                y_offset += 40
    
    # GameEventInterface implementation
    def on_combat_started(self, encounter_data: Dict[str, Any]) -> None:
        """Handle combat start event."""
        self.messages.append("Combat started!")
    
    def on_enemy_defeated(self, enemy_id: str) -> None:
        """Handle enemy defeated event."""
        self.messages.append(f"Enemy defeated!")
    
    def on_damage_dealt(self, amount: int, target_id: str) -> None:
        """Handle damage dealt event."""
        self.messages.append(f"{amount} damage dealt!")
    
    def on_dialogue_displayed(self, dialogue_text: str) -> None:
        """Handle dialogue display event."""
        self.messages.append(dialogue_text)
    
    def on_inventory_changed(self, inventory: Dict[str, Any]) -> None:
        """Handle inventory change event."""
        pass
    
    def on_level_up(self, character_id: str) -> None:
        """Handle level up event."""
        self.messages.append(f"Level up!")
    
    def on_quest_completed(self, quest_id: str) -> None:
        """Handle quest completion event."""
        # Get quest name from game logic
        quest_data = self.adapter.get_quest(quest_id)
        quest_name = quest_data.get('title', 'Quest') if quest_data else 'Quest'
        self.messages.append(f"Quest completed: {quest_name}")
    
    def on_ending_triggered(self, ending_id: str) -> None:
        """Handle ending triggered event."""
        self.messages.append(f"Ending reached!")
