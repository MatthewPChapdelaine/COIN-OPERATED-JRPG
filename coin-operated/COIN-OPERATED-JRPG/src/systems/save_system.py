"""
COIN:OPERATED JRPG - Save/Load System
Save and load game state
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


class SaveSystem:
    """Handles saving and loading game state"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self.max_save_slots = 10
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
    def save_game(self, slot: int, game_state: Dict) -> bool:
        """Save game to a specific slot"""
        try:
            if slot < 1 or slot > self.max_save_slots:
                print(f"Invalid save slot. Must be between 1 and {self.max_save_slots}.")
                return False
            
            # Add metadata
            save_data = {
                'metadata': {
                    'slot': slot,
                    'timestamp': datetime.now().isoformat(),
                    'playtime': game_state.get('playtime', 0),
                    'act': game_state.get('game_progress', {}).get('act', 1),
                    'player_level': game_state.get('player', {}).get('level', 1),
                    'location': game_state.get('current_location', 'Unknown')
                },
                'game_state': game_state
            }
            
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"\n💾 Game saved to slot {slot}")
            return True
            
        except Exception as e:
            print(f"\n✗ Failed to save game: {e}")
            return False
    
    def load_game(self, slot: int) -> Optional[Dict]:
        """Load game from a specific slot"""
        try:
            if slot < 1 or slot > self.max_save_slots:
                print(f"Invalid save slot. Must be between 1 and {self.max_save_slots}.")
                return None
            
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if not os.path.exists(save_file):
                print(f"\nNo save file found in slot {slot}.")
                return None
            
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            print(f"\n📂 Game loaded from slot {slot}")
            return save_data['game_state']
            
        except Exception as e:
            print(f"\n✗ Failed to load game: {e}")
            return None
    
    def delete_save(self, slot: int) -> bool:
        """Delete a save file"""
        try:
            if slot < 1 or slot > self.max_save_slots:
                return False
            
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_file):
                os.remove(save_file)
                print(f"\n🗑️ Save file {slot} deleted")
                return True
            else:
                print(f"\nNo save file found in slot {slot}.")
                return False
                
        except Exception as e:
            print(f"\n✗ Failed to delete save: {e}")
            return False
    
    def list_saves(self) -> Dict[int, Dict]:
        """List all available save files with metadata"""
        saves = {}
        
        for slot in range(1, self.max_save_slots + 1):
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                        saves[slot] = save_data.get('metadata', {})
                except:
                    saves[slot] = {'error': 'Corrupted save file'}
        
        return saves
    
    def display_saves(self):
        """Display all save files"""
        print(f"\n{'=' * 60}")
        print(" " * 20 + "SAVE FILES")
        print(f"{'=' * 60}")
        
        saves = self.list_saves()
        
        if not saves:
            print("\nNo save files found.")
        else:
            for slot, metadata in saves.items():
                if 'error' in metadata:
                    print(f"\nSlot {slot}: [CORRUPTED]")
                else:
                    timestamp = metadata.get('timestamp', 'Unknown')
                    act = metadata.get('act', '?')
                    level = metadata.get('player_level', '?')
                    location = metadata.get('location', 'Unknown')
                    
                    # Format timestamp
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        time_str = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        time_str = timestamp
                    
                    print(f"\nSlot {slot}:")
                    print(f"  Act {act} | Level {level} | {location}")
                    print(f"  Saved: {time_str}")
    
    def auto_save(self, game_state: Dict) -> bool:
        """Perform auto-save"""
        # Auto-save always goes to slot 0 (special slot)
        try:
            save_file = os.path.join(self.save_directory, "autosave.json")
            
            save_data = {
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'is_autosave': True
                },
                'game_state': game_state
            }
            
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print("\n💾 Auto-saved")
            return True
            
        except Exception as e:
            print(f"\n✗ Auto-save failed: {e}")
            return False
    
    def load_autosave(self) -> Optional[Dict]:
        """Load auto-save"""
        try:
            save_file = os.path.join(self.save_directory, "autosave.json")
            
            if not os.path.exists(save_file):
                print("\nNo auto-save found.")
                return None
            
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            print("\n📂 Auto-save loaded")
            return save_data['game_state']
            
        except Exception as e:
            print(f"\n✗ Failed to load auto-save: {e}")
            return None
    
    def export_save(self, slot: int, export_path: str) -> bool:
        """Export save to a different location"""
        try:
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if not os.path.exists(save_file):
                print(f"\nNo save file found in slot {slot}.")
                return False
            
            import shutil
            shutil.copy(save_file, export_path)
            print(f"\n📤 Save exported to {export_path}")
            return True
            
        except Exception as e:
            print(f"\n✗ Failed to export save: {e}")
            return False
    
    def import_save(self, import_path: str, slot: int) -> bool:
        """Import save from external location"""
        try:
            if not os.path.exists(import_path):
                print(f"\nImport file not found: {import_path}")
                return False
            
            import shutil
            save_file = os.path.join(self.save_directory, f"save_{slot}.json")
            shutil.copy(import_path, save_file)
            print(f"\n📥 Save imported to slot {slot}")
            return True
            
        except Exception as e:
            print(f"\n✗ Failed to import save: {e}")
            return False
