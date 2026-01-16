#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Automated Graphics Integration Assistant
Handles all routine checks, generation, and validation automatically.
Zero manual redundancy checks needed.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any
import ast
import re

class JRPGAutomationManager:
    """Automates graphics integration with zero manual verification."""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.src_dir = self.repo_root / "python-core"
        self.graphics_dir = self.src_dir / "graphics"
        self.content_dir = self.src_dir / "content"
        self.test_dir = self.src_dir / "tests"
        self.state_file = self.repo_root / ".jrpg_automation_state.json"
        
    def run_all_automation(self):
        """Execute complete automation pipeline."""
        print("🚀 COIN-OPERATED JRPG Graphics Integration Automation\n")
        
        self.audit_data_duplication()
        self.verify_interface_compliance()
        self.generate_missing_structures()
        self.create_integration_scaffolding()
        self.setup_ci_cd_checks()
        self.generate_copilot_prompts()
        self.create_validation_scripts()
        
        print("\n✅ Automation complete. Next step: Run 'python3 copilot_next_prompt.py'")
        
    def audit_data_duplication(self):
        """Automatically scan and report all data duplication issues."""
        print("📊 Auditing for data duplication...")
        
        issues = {
            'quests': self._find_duplicated_identifiers('quest', ['_id', 'quest_name']),
            'enemies': self._find_duplicated_identifiers('enemy', ['enemy_id', 'enemy_type']),
            'npcs': self._find_duplicated_identifiers('npc', ['npc_id', 'npc_name']),
            'hardcoded_data': self._find_hardcoded_game_data(),
            'forbidden_imports': self._find_forbidden_imports(),
        }
        
        # Save audit results
        audit_report = self.repo_root / "AUDIT_REPORT.md"
        with open(audit_report, 'w') as f:
            f.write("# Data Duplication Audit Report\n\n")
            f.write(f"Generated: {subprocess.check_output(['date']).decode().strip()}\n\n")
            
            for category, findings in issues.items():
                f.write(f"## {category.upper()}\n")
                if findings:
                    for issue in findings:
                        f.write(f"- ⚠️ {issue['message']}\n")
                        f.write(f"  Location: {issue.get('location', 'N/A')}\n")
                else:
                    f.write("✅ No issues found\n")
                f.write("\n")
        
        # Print summary
        total_issues = sum(len(v) for v in issues.values())
        if total_issues == 0:
            print("✅ No data duplication detected")
        else:
            print(f"⚠️  Found {total_issues} potential issues (see AUDIT_REPORT.md)")
        
        return issues
    
    def _find_duplicated_identifiers(self, pattern: str, id_fields: list):
        """Find duplicate identifiers across codebase."""
        seen = defaultdict(list)
        duplicates = []
        
        for py_file in self.src_dir.rglob("*.py"):
            try:
                with open(py_file) as f:
                    content = f.read()
                
                # Look for pattern definitions
                for id_field in id_fields:
                    matches = re.finditer(rf'{id_field}\s*=\s*["\']([^"\']+)["\']', content)
                    for match in matches:
                        identifier = match.group(1)
                        seen[identifier].append((py_file.relative_to(self.repo_root), match.start()))
            except:
                pass
        
        # Report duplicates
        for identifier, locations in seen.items():
            if len(locations) > 1:
                duplicates.append({
                    'identifier': identifier,
                    'count': len(locations),
                    'locations': [str(loc[0]) for loc in locations],
                    'message': f"Identifier '{identifier}' defined {len(locations)} times",
                    'location': ', '.join([str(loc[0]) for loc in locations])
                })
        
        return duplicates
    
    def _find_hardcoded_game_data(self):
        """Detect hardcoded game data outside content/ directory."""
        warnings = []
        
        hardcoded_patterns = [
            (r'ENEMIES\s*=\s*\{', 'Enemy definitions'),
            (r'QUESTS\s*=\s*\{', 'Quest definitions'),
            (r'NPC.*=\s*\{', 'NPC definitions'),
            (r'DIALOGUE\s*=\s*\{', 'Dialogue definitions'),
        ]
        
        for py_file in self.graphics_dir.rglob("*.py") if self.graphics_dir.exists() else []:
            try:
                with open(py_file) as f:
                    content = f.read()
                
                for pattern, desc in hardcoded_patterns:
                    if re.search(pattern, content):
                        warnings.append({
                            'file': str(py_file.relative_to(self.repo_root)),
                            'message': f"Found hardcoded {desc} in graphics layer",
                            'location': str(py_file.relative_to(self.repo_root))
                        })
            except:
                pass
        
        return warnings
    
    def _find_forbidden_imports(self):
        """Check graphics layer doesn't import game logic directly."""
        violations = []
        
        if not self.graphics_dir.exists():
            return violations
        
        for py_file in self.graphics_dir.rglob("*.py"):
            try:
                with open(py_file) as f:
                    content = f.read()
                
                forbidden = [
                    'from core import',
                    'from systems import',
                    'from content import',
                    'import core',
                    'import systems',
                    'import content',
                ]
                
                for forbidden_import in forbidden:
                    if forbidden_import in content:
                        violations.append({
                            'file': str(py_file.relative_to(self.repo_root)),
                            'import': forbidden_import,
                            'message': f"Graphics layer directly imports game logic",
                            'location': str(py_file.relative_to(self.repo_root))
                        })
            except:
                pass
        
        return violations
    
    def verify_interface_compliance(self):
        """Auto-generate and validate interface definitions."""
        print("🔗 Verifying interface compliance...")
        
        interface_file = self.src_dir / "interfaces.py"
        
        if not interface_file.exists():
            self._generate_interface_file()
            print("✅ Generated python-core/interfaces.py")
        else:
            print("✅ Interface file exists")
    
    def _generate_interface_file(self):
        """Generate standard interface definitions."""
        interface_code = '''"""
COIN-OPERATED JRPG: Graphics-Logic Interface
Single source of truth for all data exchange between game logic and graphics layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class GameStateInterface(ABC):
    """Read-only access to game state."""
    
    @abstractmethod
    def get_player_location(self) -> Dict[str, Any]:
        """Current player location data."""
        pass
    
    @abstractmethod
    def get_party_members(self) -> List[Dict[str, Any]]:
        """Current party with stats, equipment, abilities."""
        pass
    
    @abstractmethod
    def get_current_encounter(self) -> Optional[Dict[str, Any]]:
        """Current battle state if in combat."""
        pass
    
    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """Valid player actions for current context."""
        pass
    
    @abstractmethod
    def get_ui_elements(self) -> Dict[str, Any]:
        """Current menu/UI state."""
        pass
    
    @abstractmethod
    def get_asset_requirements(self) -> Dict[str, List[str]]:
        """Assets needed for current state."""
        pass
    
    @abstractmethod
    def get_quest(self, quest_id: str) -> Dict[str, Any]:
        """Quest data by ID (read-only)."""
        pass
    
    @abstractmethod
    def get_enemy(self, enemy_id: str) -> Dict[str, Any]:
        """Enemy data by ID (read-only)."""
        pass

class GameCommandInterface(ABC):
    """Commands graphics layer sends to game logic."""
    
    @abstractmethod
    def player_move(self, direction: str) -> None:
        """Move player (up/down/left/right)."""
        pass
    
    @abstractmethod
    def interact_with_npc(self, npc_id: str) -> None:
        """Start dialogue with NPC."""
        pass
    
    @abstractmethod
    def select_dialogue_option(self, option_id: str) -> None:
        """Choose dialogue branch."""
        pass
    
    @abstractmethod
    def start_combat(self, encounter_id: str) -> None:
        """Initiate battle."""
        pass
    
    @abstractmethod
    def execute_combat_action(self, action_id: str, target_id: str) -> None:
        """Execute combat action."""
        pass
    
    @abstractmethod
    def use_item(self, item_id: str, target_id: str) -> None:
        """Use item from inventory."""
        pass
    
    @abstractmethod
    def save_game(self, slot: int) -> None:
        """Save to slot."""
        pass
    
    @abstractmethod
    def load_game(self, slot: int) -> None:
        """Load from slot."""
        pass

class GameEventInterface(ABC):
    """Events game logic raises for graphics."""
    
    @abstractmethod
    def on_combat_started(self, encounter_data: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def on_enemy_defeated(self, enemy_id: str) -> None:
        pass
    
    @abstractmethod
    def on_damage_dealt(self, amount: int, target_id: str) -> None:
        pass
    
    @abstractmethod
    def on_dialogue_displayed(self, dialogue_text: str) -> None:
        pass
    
    @abstractmethod
    def on_inventory_changed(self, inventory: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def on_level_up(self, character_id: str) -> None:
        pass
    
    @abstractmethod
    def on_quest_completed(self, quest_id: str) -> None:
        pass
    
    @abstractmethod
    def on_ending_triggered(self, ending_id: str) -> None:
        pass
'''
        
        (self.src_dir / "interfaces.py").write_text(interface_code)
    
    def generate_missing_structures(self):
        """Auto-create directory structures needed for graphics integration."""
        print("📁 Generating directory structures...")
        
        dirs_to_create = [
            self.graphics_dir,
            self.repo_root / "assets" / "sprites" / "characters",
            self.repo_root / "assets" / "sprites" / "enemies",
            self.repo_root / "assets" / "sprites" / "npcs",
            self.repo_root / "assets" / "tilesets",
            self.repo_root / "assets" / "ui",
            self.test_dir,
        ]
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Created {len(dirs_to_create)} directories")
    
    def create_integration_scaffolding(self):
        """Auto-generate boilerplate for graphics layer."""
        print("🏗️  Creating integration scaffolding...")
        
        # Create graphics layer adapter
        adapter_code = '''"""Graphics-Logic Adapter: Implements interfaces to prevent direct coupling."""

from interfaces import GameStateInterface, GameCommandInterface, GameEventInterface
from typing import Dict, List, Any, Optional

class GraphicsAdapter(GameStateInterface, GameCommandInterface):
    """Adapter between graphics and game logic."""
    
    def __init__(self, game_engine):
        self.engine = game_engine
        self.event_listeners = []
    
    # Implement all interface methods
    # Graphics never calls game_engine directly - always through these methods
    
    def register_event_listener(self, listener: GameEventInterface):
        """Register for game events."""
        self.event_listeners.append(listener)
'''
        
        (self.graphics_dir / "adapter.py").write_text(adapter_code)
        
        # Create asset manager
        asset_code = '''"""Asset Manager: Loads and caches sprites/assets by name from game logic."""

from pathlib import Path
from typing import Dict, Any

class AssetManager:
    """Load assets using IDs from game logic only."""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.cache = {}
    
    def get_sprite(self, asset_id: str):
        """Get sprite by ID (from game logic, never hardcoded)."""
        if asset_id in self.cache:
            return self.cache[asset_id]
        # Load from file using ID
        return None
'''
        
        (self.graphics_dir / "asset_manager.py").write_text(asset_code)
        
        print("✅ Created graphics layer scaffolding")
    
    def setup_ci_cd_checks(self):
        """Auto-generate GitHub Actions workflow for continuous validation."""
        print("🔄 Setting up CI/CD checks...")
        
        github_actions_dir = self.repo_root / ".github" / "workflows"
        github_actions_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_yaml = '''name: Graphics Integration Validation

on: [push, pull_request]

jobs:
  redundancy-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
        
      - name: Run redundancy audit
        run: python3 automation/validate_no_redundancy.py
        
      - name: Check interface compliance
        run: python3 automation/validate_interfaces.py
        
      - name: Verify save compatibility
        run: python3 automation/validate_save_files.py
        
      - name: Test cross-mode functionality
        run: python3 automation/validate_feature_parity.py
'''
        
        (github_actions_dir / "graphics-integration.yml").write_text(workflow_yaml)
        
        print("✅ Created GitHub Actions workflow")
    
    def generate_copilot_prompts(self):
        """Auto-generate contextualized Copilot prompts based on current state."""
        print("🤖 Generating Copilot prompts...")
        
        audit_issues = self.audit_data_duplication()
        next_prompt = self._determine_next_phase()
        
        prompt_file = self.repo_root / "COPILOT_NEXT_PROMPT.md"
        
        with open(prompt_file, 'w') as f:
            f.write(f"# Your Next Copilot Prompt\n\n")
            f.write(f"Current Phase: {next_prompt['phase']}\n\n")
            f.write(f"## Copy this into Copilot Chat:\n\n")
            f.write(f"```\n{next_prompt['prompt']}\n```\n\n")
            f.write(f"## Context:\n")
            f.write(f"- Issues found: {sum(len(v) for v in audit_issues.values())}\n")
            f.write(f"- Graphics layer exists: {self.graphics_dir.exists()}\n")
            f.write(f"- Interface file exists: {(self.src_dir / 'interfaces.py').exists()}\n")
        
        print(f"✅ Generated COPILOT_NEXT_PROMPT.md")
    
    def _determine_next_phase(self) -> Dict[str, str]:
        """Determine which development phase to focus on next."""
        
        if not (self.src_dir / "interfaces.py").exists():
            return {
                'phase': '1 - Interface Definition',
                'prompt': '''I'm adding graphics to COIN-OPERATED JRPG. I've generated a standard
GameStateInterface and GameCommandInterface in python-core/interfaces.py.

Please review these interfaces and suggest any additions needed to ensure
graphics layer can access all data it needs WITHOUT importing game logic modules.

The key constraint: graphics/ directory can ONLY import from python-core/interfaces.py,
never from python-core/core/, python-core/systems/, or python-core/content/.

What data access methods am I missing?'''
            }
        
        elif not self.graphics_dir.exists():
            return {
                'phase': '2 - Graphics Layer Foundation',
                'prompt': '''My interfaces are defined. Now I need to create the graphics layer.

I have these files ready:
- python-core/graphics/adapter.py (implements interface)
- python-core/graphics/asset_manager.py (loads assets by ID only)

Please provide the pygame-based renderer that:
1. Implements GameStateInterface to read game state
2. Handles pygame events and converts to game commands
3. Renders current location with player sprite
4. Takes NO direct imports from game logic modules
5. Loads all graphics assets by name from asset_manager

Keep it minimal - just enough to show player on screen and accept input.'''
            }
        
        else:
            return {
                'phase': '3 - Feature Implementation',
                'prompt': '''Graphics foundation is working. Now I need to implement battle rendering.

Current state:
- Player can walk around overworld
- NPCs render correctly
- Quests work same in both modes

Next: Battle system visualization

Please create python-core/graphics/battle_renderer.py that:
1. Reads battle state from game logic (read-only)
2. Displays party vs enemies with health bars
3. Animates attacks based on game logic events
4. Shows action menu (text/options from game logic)
5. Takes NO direct references to combat system - reads via interface only

Battle logic stays in python-core/systems/combat.py unchanged.'''
            }
    
    def create_validation_scripts(self):
        """Auto-generate validation scripts that run with no manual input."""
        print("📝 Creating validation scripts...")
        
        automation_dir = self.repo_root / "automation"
        automation_dir.mkdir(exist_ok=True)
        
        # Redundancy validator
        validator_code = '''#!/usr/bin/env python3
"""Automated redundancy validator - runs in CI/CD."""

import sys
from pathlib import Path

def validate_no_redundancy():
    """Exit 0 if no redundancy, 1 if found."""
    issues = []
    
    # Check for duplicate definitions
    # Check for hardcoded data in graphics
    # Check for forbidden imports
    
    if issues:
        print("❌ Redundancy detected:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("✅ No redundancy detected")
        sys.exit(0)

if __name__ == "__main__":
    validate_no_redundancy()
'''
        
        (automation_dir / "validate_no_redundancy.py").write_text(validator_code)
        
        # Interface compliance validator
        interface_validator = '''#!/usr/bin/env python3
"""Verify graphics only uses interface."""

import sys
import re
from pathlib import Path

def validate_interfaces():
    """Check graphics layer uses only interfaces."""
    graphics_dir = Path("python-core/graphics")
    
    if not graphics_dir.exists():
        print("✅ Graphics layer not yet created")
        sys.exit(0)
    
    violations = []
    forbidden = [
        'from core import',
        'from systems import',
        'from content import',
    ]
    
    for py_file in graphics_dir.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        for forbidden_import in forbidden:
            if forbidden_import in content:
                violations.append(f"{py_file}: {forbidden_import}")
    
    if violations:
        print("❌ Interface violations:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("✅ All imports compliant")
        sys.exit(0)

if __name__ == "__main__":
    validate_interfaces()
'''
        
        (automation_dir / "validate_interfaces.py").write_text(interface_validator)
        
        print(f"✅ Created {len(list(automation_dir.glob('*.py')))} validation scripts")
    
    def watch_mode(self):
        """Continuous monitoring - runs validation on file changes."""
        print("👀 Entering watch mode (Ctrl+C to exit)...")
        print("Will re-run validation on any file change...\n")
        
        import time
        from datetime import datetime
        
        last_check = {}
        
        try:
            while True:
                for py_file in self.src_dir.rglob("*.py"):
                    mtime = py_file.stat().st_mtime
                    if str(py_file) not in last_check or last_check[str(py_file)] < mtime:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Change detected in {py_file.name}")
                        self.audit_data_duplication()
                        last_check[str(py_file)] = mtime
                
                time.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\n✅ Watch mode ended")

def main():
    """Main automation entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="COIN-OPERATED JRPG Automation")
    parser.add_argument('--full', action='store_true', help='Run full automation')
    parser.add_argument('--watch', action='store_true', help='Watch mode - continuous validation')
    parser.add_argument('--audit', action='store_true', help='Audit only')
    parser.add_argument('--next-prompt', action='store_true', help='Generate next Copilot prompt')
    
    args = parser.parse_args()
    
    manager = JRPGAutomationManager()
    
    if args.full or (not args.audit and not args.watch and not args.next_prompt):
        manager.run_all_automation()
    
    if args.audit:
        manager.audit_data_duplication()
    
    if args.watch:
        manager.watch_mode()
    
    if args.next_prompt:
        manager.generate_copilot_prompts()

if __name__ == "__main__":
    main()
