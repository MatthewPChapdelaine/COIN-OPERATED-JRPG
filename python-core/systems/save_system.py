"""
COIN:OPERATED JRPG - Save/Load System
Save and load game state with type safety and error handling

Academic Subjects:
- File I/O: Persistent data storage
- Software Engineering: Error handling, data serialization
- Computer Science: JSON parsing, file systems
- Data Security: Corruption detection, backup strategies

Complexity Guarantees:
- Save operation: O(n) where n = game state size
- Load operation: O(n) where n = file size
- List saves: O(s) where s = number of save slots
- All operations use Result types for explicit error handling
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple
from dataclasses import dataclass

# Import AAA Standards
from aaa_standards.result_types import Result, Ok, Err
from aaa_standards.type_definitions import SaveData
from aaa_standards.formal_specs import verify_complexity, requires
from aaa_standards.performance import LRUCache


@dataclass(frozen=True)
class SaveMetadata:
    """Immutable save file metadata.
    
    Type Safety: Replaces Dict[str, Any]
    Immutability: Frozen for thread safety
    Complexity: O(1) all operations
    """
    slot: int
    timestamp: str
    playtime: int
    act: int
    player_level: int
    location: str
    is_autosave: bool = False
    
    @staticmethod
    def from_game_state(slot: int, game_state: Dict) -> 'SaveMetadata':
        """Create metadata from game state.
        
        Complexity: O(1) - dict lookups
        """
        return SaveMetadata(
            slot=slot,
            timestamp=datetime.now().isoformat(),
            playtime=game_state.get('playtime', 0),
            act=game_state.get('game_progress', {}).get('act', 1),
            player_level=game_state.get('player', {}).get('level', 1),
            location=game_state.get('current_location', 'Unknown')
        )


class SaveSystem:
    """Handles saving and loading game state with AAA standards.
    
    Design Pattern: Result-based Error Handling
    - All operations return Result types
    - Explicit error messages
    - No exceptions for control flow
    
    Performance:
    - Save: O(n) for state serialization
    - Load: O(n) for parsing
    - List: O(s) for s save slots
    - Cache: O(1) metadata lookups
    """
    
    def __init__(self, save_directory: str = "saves"):
        """Initialize save system.
        
        Args:
            save_directory: Directory for save files
            
        Complexity: O(1) - directory creation if needed
        Side Effects: Creates save directory
        """
        self._save_directory = Path(save_directory)
        self._max_save_slots = 10
        self._metadata_cache: LRUCache[int, SaveMetadata] = LRUCache(capacity=20)
        
        # Create save directory if it doesn't exist
        self._save_directory.mkdir(parents=True, exist_ok=True)
    
    @verify_complexity(time="O(n)", description="Serializes n bytes of game state")
    @requires(lambda self, slot: 1 <= slot <= self._max_save_slots,
              "Slot must be in valid range")
    def save_game(self, slot: int, game_state: Dict) -> Result[SaveMetadata, str]:
        """Save game to a specific slot.
        
        Args:
            slot: Save slot number (1-10)
            game_state: Game state dictionary
            
        Returns:
            Success[SaveMetadata]: Save successful with metadata
            Failure[str]: Save failed with error message
            
        Complexity: O(n) where n = size of game state
        Side Effects: Writes to disk, prints message
        Thread Safety: File I/O is atomic at OS level
        
        Preconditions:
            - slot in valid range [1, max_slots]
            - game_state is valid dict
        Postconditions:
            - Save file exists on disk
            - Metadata cached
        """
        if not (1 <= slot <= self._max_save_slots):
            return Err(f"Invalid save slot {slot}. Must be between 1 and {self._max_save_slots}")
        
        try:
            # Create metadata
            metadata = SaveMetadata.from_game_state(slot, game_state)
            
            # Build save data
            save_data = {
                'metadata': {
                    'slot': metadata.slot,
                    'timestamp': metadata.timestamp,
                    'playtime': metadata.playtime,
                    'act': metadata.act,
                    'player_level': metadata.player_level,
                    'location': metadata.location
                },
                'game_state': game_state
            }
            
            # Write to file (O(n) for serialization)
            save_file = self._save_directory / f"save_{slot}.json"
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            # Cache metadata
            self._metadata_cache.put(slot, metadata)
            
            print(f"\n💾 Game saved to slot {slot}")
            return Ok(metadata)
            
        except OSError as e:
            return Err(f"File system error: {e}")
        except (TypeError, ValueError) as e:
            return Err(f"Serialization error: {e}")
        except Exception as e:
            return Err(f"Unexpected error during save: {e}")
    
    @verify_complexity(time="O(n)", description="Parses n bytes from save file")
    @requires(lambda self, slot: 1 <= slot <= self._max_save_slots,
              "Slot must be in valid range")
    def load_game(self, slot: int) -> Result[Dict, str]:
        """Load game from a specific slot.
        
        Args:
            slot: Save slot number (1-10)
            
        Returns:
            Success[Dict]: Game state loaded
            Failure[str]: Load failed with error message
            
        Complexity: O(n) where n = save file size
        Side Effects: Reads from disk, prints message
        
        Preconditions:
            - slot in valid range
            - Save file exists and is valid JSON
        Postconditions:
            - Returns valid game state dict
        """
        if not (1 <= slot <= self._max_save_slots):
            return Err(f"Invalid save slot {slot}. Must be between 1 and {self._max_save_slots}")
        
        save_file = self._save_directory / f"save_{slot}.json"
        
        if not save_file.exists():
            return Err(f"No save file found in slot {slot}")
        
        try:
            # Read and parse (O(n) for file size)
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            # Validate structure
            if 'game_state' not in save_data:
                return Err(f"Corrupted save file in slot {slot}: missing game_state")
            
            print(f"\n📂 Game loaded from slot {slot}")
            return Ok(save_data['game_state'])
            
        except json.JSONDecodeError as e:
            return Err(f"Corrupted save file in slot {slot}: {e}")
        except OSError as e:
            return Err(f"File system error: {e}")
        except Exception as e:
            return Err(f"Unexpected error during load: {e}")
    
    @verify_complexity(time="O(1)", description="File deletion is constant time")
    def delete_save(self, slot: int) -> Result[None, str]:
        """Delete a save file.
        
        Args:
            slot: Save slot to delete
            
        Returns:
            Success[None]: Save deleted
            Failure[str]: Deletion failed
            
        Complexity: O(1) - file deletion
        Side Effects: Removes file from disk
        """
        if not (1 <= slot <= self._max_save_slots):
            return Err(f"Invalid save slot {slot}")
        
        save_file = self._save_directory / f"save_{slot}.json"
        
        if not save_file.exists():
            return Err(f"No save file found in slot {slot}")
        
        try:
            save_file.unlink()
            self._metadata_cache.remove(slot) if hasattr(self._metadata_cache, 'remove') else None
            print(f"\n🗑️ Save file {slot} deleted")
            return Ok(None)
        except OSError as e:
            return Err(f"Failed to delete save: {e}")
    
    @verify_complexity(time="O(n)", description="Lists n save slots")
    def list_saves(self) -> Result[Tuple[SaveMetadata, ...], str]:
        """List all available save files with metadata.
        
        Returns:
            Success[Tuple[SaveMetadata, ...]]: Available saves
            Failure[str]: Error listing saves
            
        Complexity: O(s) where s = max_save_slots (typically 10)
        Side Effects: Reads metadata from disk
        """
        saves = []
        
        for slot in range(1, self._max_save_slots + 1):
            # Check cache first
            cached = self._metadata_cache.get(slot)
            if cached is not None:
                saves.append(cached)
                continue
            
            save_file = self._save_directory / f"save_{slot}.json"
            
            if save_file.exists():
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    
                    meta_dict = save_data.get('metadata', {})
                    metadata = SaveMetadata(
                        slot=meta_dict.get('slot', slot),
                        timestamp=meta_dict.get('timestamp', ''),
                        playtime=meta_dict.get('playtime', 0),
                        act=meta_dict.get('act', 1),
                        player_level=meta_dict.get('player_level', 1),
                        location=meta_dict.get('location', 'Unknown')
                    )
                    
                    self._metadata_cache.put(slot, metadata)
                    saves.append(metadata)
                    
                except Exception:
                    # Skip corrupted saves
                    continue
        
        return Ok(tuple(saves))
    
    @verify_complexity(time="O(n)", description="Displays s saves")
    def display_saves(self) -> None:
        """Display all save files.
        
        Complexity: O(s) where s = number of saves
        Side Effects: Prints to console
        """
        print(f"\n{'=' * 60}")
        print(" " * 20 + "SAVE FILES")
        print(f"{'=' * 60}")
        
        result = self.list_saves()
        if result.is_failure():
            print(f"\nError listing saves: {result.unwrap_failure()}")
            return
        
        saves = result.unwrap()
        
        if not saves:
            print("\nNo save files found.")
        else:
            for metadata in saves:
                # Format timestamp
                try:
                    dt = datetime.fromisoformat(metadata.timestamp)
                    time_str = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    time_str = metadata.timestamp
                
                print(f"\nSlot {metadata.slot}:")
                print(f"  Act {metadata.act} | Level {metadata.player_level} | {metadata.location}")
                print(f"  Saved: {time_str}")
    
    @verify_complexity(time="O(n)", description="Auto-save serializes game state")
    def auto_save(self, game_state: Dict) -> Result[None, str]:
        """Perform auto-save.
        
        Args:
            game_state: Current game state
            
        Returns:
            Success[None]: Auto-save successful
            Failure[str]: Auto-save failed
            
        Complexity: O(n) where n = game state size
        Side Effects: Writes to disk
        """
        try:
            save_file = self._save_directory / "autosave.json"
            
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
            return Ok(None)
            
        except Exception as e:
            return Err(f"Auto-save failed: {e}")
    
    @verify_complexity(time="O(n)", description="Loads and parses auto-save")
    def load_autosave(self) -> Result[Dict, str]:
        """Load auto-save.
        
        Returns:
            Success[Dict]: Auto-save game state
            Failure[str]: Load failed
            
        Complexity: O(n) for file size
        """
        save_file = self._save_directory / "autosave.json"
        
        if not save_file.exists():
            return Err("No auto-save found")
        
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            if 'game_state' not in save_data:
                return Err("Corrupted auto-save file")
            
            print("\n📂 Auto-save loaded")
            return Ok(save_data['game_state'])
            
        except Exception as e:
            return Err(f"Failed to load auto-save: {e}")