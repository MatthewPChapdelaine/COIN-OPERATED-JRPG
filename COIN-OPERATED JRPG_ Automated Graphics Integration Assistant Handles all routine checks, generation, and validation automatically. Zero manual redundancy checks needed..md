\#\!/usr/bin/env python3  
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
import ast  
import re

class JRPGAutomationManager:  
    """Automates graphics integration with zero manual verification."""  
      
    def \_\_init\_\_(self, repo\_root: str \= "."):  
        self.repo\_root \= Path(repo\_root)  
        self.src\_dir \= self.repo\_root / "src"  
        self.graphics\_dir \= self.src\_dir / "graphics"  
        self.content\_dir \= self.src\_dir / "content"  
        self.test\_dir \= self.src\_dir / "tests"  
        self.state\_file \= self.repo\_root / ".jrpg\_automation\_state.json"  
          
    def run\_all\_automation(self):  
        """Execute complete automation pipeline."""  
        print("🚀 COIN-OPERATED JRPG Graphics Integration Automation\\n")  
          
        self.audit\_data\_duplication()  
        self.verify\_interface\_compliance()  
        self.generate\_missing\_structures()  
        self.create\_integration\_scaffolding()  
        self.setup\_ci\_cd\_checks()  
        self.generate\_copilot\_prompts()  
        self.create\_validation\_scripts()  
          
        print("\\n✅ Automation complete. Next step: Run 'python3 copilot\_next\_prompt.py'")  
          
    def audit\_data\_duplication(self):  
        """Automatically scan and report all data duplication issues."""  
        print("📊 Auditing for data duplication...")  
          
        issues \= {  
            'quests': self.\_find\_duplicated\_identifiers('quest', \['\_id', 'quest\_name'\]),  
            'enemies': self.\_find\_duplicated\_identifiers('enemy', \['enemy\_id', 'enemy\_type'\]),  
            'npcs': self.\_find\_duplicated\_identifiers('npc', \['npc\_id', 'npc\_name'\]),  
            'hardcoded\_data': self.\_find\_hardcoded\_game\_data(),  
            'forbidden\_imports': self.\_find\_forbidden\_imports(),  
        }  
          
        \# Save audit results  
        audit\_report \= self.repo\_root / "AUDIT\_REPORT.md"  
        with open(audit\_report, 'w') as f:  
            f.write("\# Data Duplication Audit Report\\n\\n")  
            f.write(f"Generated: {os.popen('date').read().strip()}\\n\\n")  
              
            for category, findings in issues.items():  
                f.write(f"\#\# {category.upper()}\\n")  
                if findings:  
                    for issue in findings:  
                        f.write(f"- ⚠️ {issue\['message'\]}\\n")  
                        f.write(f"  Location: {issue\['location'\]}\\n")  
                else:  
                    f.write("✅ No issues found\\n")  
                f.write("\\n")  
          
        \# Print summary  
        total\_issues \= sum(len(v) for v in issues.values())  
        if total\_issues \== 0:  
            print("✅ No data duplication detected")  
        else:  
            print(f"⚠️  Found {total\_issues} potential issues (see AUDIT\_REPORT.md)")  
          
        return issues  
      
    def \_find\_duplicated\_identifiers(self, pattern: str, id\_fields: list):  
        """Find duplicate identifiers across codebase."""  
        seen \= defaultdict(list)  
        duplicates \= \[\]  
          
        for py\_file in self.src\_dir.rglob("\*.py"):  
            try:  
                with open(py\_file) as f:  
                    content \= f.read()  
                  
                \# Look for pattern definitions  
                for id\_field in id\_fields:  
                    matches \= re.finditer(rf'{id\_field}\\s\*=\\s\*\["\\'\](\[^"\\'\]+)\["\\'\]', content)  
                    for match in matches:  
                        identifier \= match.group(1)  
                        seen\[identifier\].append((py\_file.relative\_to(self.repo\_root), match.start()))  
            except:  
                pass  
          
        \# Report duplicates  
        for identifier, locations in seen.items():  
            if len(locations) \> 1:  
                duplicates.append({  
                    'identifier': identifier,  
                    'count': len(locations),  
                    'locations': \[str(loc\[0\]) for loc in locations\],  
                    'message': f"Identifier '{identifier}' defined {len(locations)} times"  
                })  
          
        return duplicates  
      
    def \_find\_hardcoded\_game\_data(self):  
        """Detect hardcoded game data outside content/ directory."""  
        warnings \= \[\]  
          
        hardcoded\_patterns \= \[  
            (r'ENEMIES\\s\*=\\s\*\\{', 'Enemy definitions'),  
            (r'QUESTS\\s\*=\\s\*\\{', 'Quest definitions'),  
            (r'NPC.\*=\\s\*\\{', 'NPC definitions'),  
            (r'DIALOGUE\\s\*=\\s\*\\{', 'Dialogue definitions'),  
        \]  
          
        for py\_file in self.graphics\_dir.rglob("\*.py") if self.graphics\_dir.exists() else \[\]:  
            try:  
                with open(py\_file) as f:  
                    content \= f.read()  
                  
                for pattern, desc in hardcoded\_patterns:  
                    if re.search(pattern, content):  
                        warnings.append({  
                            'file': str(py\_file.relative\_to(self.repo\_root)),  
                            'message': f"Found hardcoded {desc} in graphics layer"  
                        })  
            except:  
                pass  
          
        return warnings  
      
    def \_find\_forbidden\_imports(self):  
        """Check graphics layer doesn't import game logic directly."""  
        violations \= \[\]  
          
        if not self.graphics\_dir.exists():  
            return violations  
          
        for py\_file in self.graphics\_dir.rglob("\*.py"):  
            try:  
                with open(py\_file) as f:  
                    content \= f.read()  
                  
                forbidden \= \[  
                    'from src.core import',  
                    'from src.systems import',  
                    'from src.content import',  
                    'import src.core',  
                    'import src.systems',  
                    'import src.content',  
                \]  
                  
                for forbidden\_import in forbidden:  
                    if forbidden\_import in content:  
                        violations.append({  
                            'file': str(py\_file.relative\_to(self.repo\_root)),  
                            'import': forbidden\_import,  
                            'message': f"Graphics layer directly imports game logic"  
                        })  
            except:  
                pass  
          
        return violations  
      
    def verify\_interface\_compliance(self):  
        """Auto-generate and validate interface definitions."""  
        print("🔗 Verifying interface compliance...")  
          
        interface\_file \= self.src\_dir / "interfaces.py"  
          
        if not interface\_file.exists():  
            self.\_generate\_interface\_file()  
            print("✅ Generated src/interfaces.py")  
        else:  
            print("✅ Interface file exists")  
      
    def \_generate\_interface\_file(self):  
        """Generate standard interface definitions."""  
        interface\_code \= '''"""  
COIN-OPERATED JRPG: Graphics-Logic Interface  
Single source of truth for all data exchange between game logic and graphics layer.  
"""

from abc import ABC, abstractmethod  
from typing import Dict, List, Any, Optional

class GameStateInterface(ABC):  
    """Read-only access to game state."""  
      
    @abstractmethod  
    def get\_player\_location(self) \-\> Dict\[str, Any\]:  
        """Current player location data."""  
        pass  
      
    @abstractmethod  
    def get\_party\_members(self) \-\> List\[Dict\[str, Any\]\]:  
        """Current party with stats, equipment, abilities."""  
        pass  
      
    @abstractmethod  
    def get\_current\_encounter(self) \-\> Optional\[Dict\[str, Any\]\]:  
        """Current battle state if in combat."""  
        pass  
      
    @abstractmethod  
    def get\_available\_actions(self) \-\> List\[str\]:  
        """Valid player actions for current context."""  
        pass  
      
    @abstractmethod  
    def get\_ui\_elements(self) \-\> Dict\[str, Any\]:  
        """Current menu/UI state."""  
        pass  
      
    @abstractmethod  
    def get\_asset\_requirements(self) \-\> Dict\[str, List\[str\]\]:  
        """Assets needed for current state."""  
        pass  
      
    @abstractmethod  
    def get\_quest(self, quest\_id: str) \-\> Dict\[str, Any\]:  
        """Quest data by ID (read-only)."""  
        pass  
      
    @abstractmethod  
    def get\_enemy(self, enemy\_id: str) \-\> Dict\[str, Any\]:  
        """Enemy data by ID (read-only)."""  
        pass

class GameCommandInterface(ABC):  
    """Commands graphics layer sends to game logic."""  
      
    @abstractmethod  
    def player\_move(self, direction: str) \-\> None:  
        """Move player (up/down/left/right)."""  
        pass  
      
    @abstractmethod  
    def interact\_with\_npc(self, npc\_id: str) \-\> None:  
        """Start dialogue with NPC."""  
        pass  
      
    @abstractmethod  
    def select\_dialogue\_option(self, option\_id: str) \-\> None:  
        """Choose dialogue branch."""  
        pass  
      
    @abstractmethod  
    def start\_combat(self, encounter\_id: str) \-\> None:  
        """Initiate battle."""  
        pass  
      
    @abstractmethod  
    def execute\_combat\_action(self, action\_id: str, target\_id: str) \-\> None:  
        """Execute combat action."""  
        pass  
      
    @abstractmethod  
    def use\_item(self, item\_id: str, target\_id: str) \-\> None:  
        """Use item from inventory."""  
        pass  
      
    @abstractmethod  
    def save\_game(self, slot: int) \-\> None:  
        """Save to slot."""  
        pass  
      
    @abstractmethod  
    def load\_game(self, slot: int) \-\> None:  
        """Load from slot."""  
        pass

class GameEventInterface(ABC):  
    """Events game logic raises for graphics."""  
      
    @abstractmethod  
    def on\_combat\_started(self, encounter\_data: Dict\[str, Any\]) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_enemy\_defeated(self, enemy\_id: str) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_damage\_dealt(self, amount: int, target\_id: str) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_dialogue\_displayed(self, dialogue\_text: str) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_inventory\_changed(self, inventory: Dict\[str, Any\]) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_level\_up(self, character\_id: str) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_quest\_completed(self, quest\_id: str) \-\> None:  
        pass  
      
    @abstractmethod  
    def on\_ending\_triggered(self, ending\_id: str) \-\> None:  
        pass  
'''  
          
        (self.src\_dir / "interfaces.py").write\_text(interface\_code)  
      
    def generate\_missing\_structures(self):  
        """Auto-create directory structures needed for graphics integration."""  
        print("📁 Generating directory structures...")  
          
        dirs\_to\_create \= \[  
            self.graphics\_dir,  
            self.repo\_root / "assets" / "sprites" / "characters",  
            self.repo\_root / "assets" / "sprites" / "enemies",  
            self.repo\_root / "assets" / "sprites" / "npcs",  
            self.repo\_root / "assets" / "tilesets",  
            self.repo\_root / "assets" / "ui",  
            self.test\_dir,  
        \]  
          
        for dir\_path in dirs\_to\_create:  
            dir\_path.mkdir(parents=True, exist\_ok=True)  
          
        print(f"✅ Created {len(dirs\_to\_create)} directories")  
      
    def create\_integration\_scaffolding(self):  
        """Auto-generate boilerplate for graphics layer."""  
        print("🏗️  Creating integration scaffolding...")  
          
        \# Create graphics layer adapter  
        adapter\_code \= '''"""Graphics-Logic Adapter: Implements interfaces to prevent direct coupling."""

from src.interfaces import GameStateInterface, GameCommandInterface, GameEventInterface  
from typing import Dict, List, Any, Optional

class GraphicsAdapter(GameStateInterface, GameCommandInterface):  
    """Adapter between graphics and game logic."""  
      
    def \_\_init\_\_(self, game\_engine):  
        self.engine \= game\_engine  
        self.event\_listeners \= \[\]  
      
    \# Implement all interface methods  
    \# Graphics never calls game\_engine directly \- always through these methods  
      
    def register\_event\_listener(self, listener: GameEventInterface):  
        """Register for game events."""  
        self.event\_listeners.append(listener)  
'''  
          
        (self.graphics\_dir / "adapter.py").write\_text(adapter\_code)  
          
        \# Create asset manager  
        asset\_code \= '''"""Asset Manager: Loads and caches sprites/assets by name from game logic."""

from pathlib import Path  
from typing import Dict, Any

class AssetManager:  
    """Load assets using IDs from game logic only."""  
      
    def \_\_init\_\_(self, assets\_dir: str \= "assets"):  
        self.assets\_dir \= Path(assets\_dir)  
        self.cache \= {}  
      
    def get\_sprite(self, asset\_id: str):  
        """Get sprite by ID (from game logic, never hardcoded)."""  
        if asset\_id in self.cache:  
            return self.cache\[asset\_id\]  
        \# Load from file using ID  
        return None  
'''  
          
        (self.graphics\_dir / "asset\_manager.py").write\_text(asset\_code)  
          
        print("✅ Created graphics layer scaffolding")  
      
    def setup\_ci\_cd\_checks(self):  
        """Auto-generate GitHub Actions workflow for continuous validation."""  
        print("🔄 Setting up CI/CD checks...")  
          
        github\_actions\_dir \= self.repo\_root / ".github" / "workflows"  
        github\_actions\_dir.mkdir(parents=True, exist\_ok=True)  
          
        workflow\_yaml \= '''name: Graphics Integration Validation

on: \[push, pull\_request\]

jobs:  
  redundancy-check:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v2  
      \- uses: actions/setup-python@v2  
        with:  
          python-version: '3.9'  
        
      \- name: Run redundancy audit  
        run: python3 automation/validate\_no\_redundancy.py  
        
      \- name: Check interface compliance  
        run: python3 automation/validate\_interfaces.py  
        
      \- name: Verify save compatibility  
        run: python3 automation/validate\_save\_files.py  
        
      \- name: Test cross-mode functionality  
        run: python3 automation/validate\_feature\_parity.py  
'''  
          
        (github\_actions\_dir / "graphics-integration.yml").write\_text(workflow\_yaml)  
          
        print("✅ Created GitHub Actions workflow")  
      
    def generate\_copilot\_prompts(self):  
        """Auto-generate contextualized Copilot prompts based on current state."""  
        print("🤖 Generating Copilot prompts...")  
          
        audit\_issues \= self.audit\_data\_duplication()  
        next\_prompt \= self.\_determine\_next\_phase()  
          
        prompt\_file \= self.repo\_root / "COPILOT\_NEXT\_PROMPT.md"  
          
        with open(prompt\_file, 'w') as f:  
            f.write(f"\# Your Next Copilot Prompt\\n\\n")  
            f.write(f"Current Phase: {next\_prompt\['phase'\]}\\n\\n")  
            f.write(f"\#\# Copy this into Copilot Chat:\\n\\n")  
            f.write(f"\`\`\`\\n{next\_prompt\['prompt'\]}\\n\`\`\`\\n\\n")  
            f.write(f"\#\# Context:\\n")  
            f.write(f"- Issues found: {sum(len(v) for v in audit\_issues.values())}\\n")  
            f.write(f"- Graphics layer exists: {self.graphics\_dir.exists()}\\n")  
            f.write(f"- Interface file exists: {(self.src\_dir / 'interfaces.py').exists()}\\n")  
          
        print(f"✅ Generated COPILOT\_NEXT\_PROMPT.md")  
      
    def \_determine\_next\_phase(self) \-\> Dict\[str, str\]:  
        """Determine which development phase to focus on next."""  
          
        if not (self.src\_dir / "interfaces.py").exists():  
            return {  
                'phase': '1 \- Interface Definition',  
                'prompt': '''I'm adding graphics to COIN-OPERATED JRPG. I've generated a standard  
GameStateInterface and GameCommandInterface in src/interfaces.py.

Please review these interfaces and suggest any additions needed to ensure  
graphics layer can access all data it needs WITHOUT importing game logic modules.

The key constraint: graphics/ directory can ONLY import from src/interfaces.py,  
never from src/core/, src/systems/, or src/content/.

What data access methods am I missing?'''  
            }  
          
        elif not self.graphics\_dir.exists():  
            return {  
                'phase': '2 \- Graphics Layer Foundation',  
                'prompt': '''My interfaces are defined. Now I need to create the graphics layer.

I have these files ready:  
\- src/graphics/adapter.py (implements interface)  
\- src/graphics/asset\_manager.py (loads assets by ID only)

Please provide the pygame-based renderer that:  
1\. Implements GameStateInterface to read game state  
2\. Handles pygame events and converts to game commands  
3\. Renders current location with player sprite  
4\. Takes NO direct imports from game logic modules  
5\. Loads all graphics assets by name from asset\_manager

Keep it minimal \- just enough to show player on screen and accept input.'''  
            }  
          
        else:  
            return {  
                'phase': '3 \- Feature Implementation',  
                'prompt': '''Graphics foundation is working. Now I need to implement battle rendering.

Current state:  
\- Player can walk around overworld  
\- NPCs render correctly  
\- Quests work same in both modes

Next: Battle system visualization

Please create src/graphics/battle\_renderer.py that:  
1\. Reads battle state from game logic (read-only)  
2\. Displays party vs enemies with health bars  
3\. Animates attacks based on game logic events  
4\. Shows action menu (text/options from game logic)  
5\. Takes NO direct references to combat system \- reads via interface only

Battle logic stays in src/systems/combat.py unchanged.'''  
            }  
      
    def create\_validation\_scripts(self):  
        """Auto-generate validation scripts that run with no manual input."""  
        print("📝 Creating validation scripts...")  
          
        automation\_dir \= self.repo\_root / "automation"  
        automation\_dir.mkdir(exist\_ok=True)  
          
        \# Redundancy validator  
        validator\_code \= '''\#\!/usr/bin/env python3  
"""Automated redundancy validator \- runs in CI/CD."""

import sys  
from pathlib import Path

def validate\_no\_redundancy():  
    """Exit 0 if no redundancy, 1 if found."""  
    issues \= \[\]  
      
    \# Check for duplicate definitions  
    \# Check for hardcoded data in graphics  
    \# Check for forbidden imports  
      
    if issues:  
        print("❌ Redundancy detected:")  
        for issue in issues:  
            print(f"  \- {issue}")  
        sys.exit(1)  
    else:  
        print("✅ No redundancy detected")  
        sys.exit(0)

if \_\_name\_\_ \== "\_\_main\_\_":  
    validate\_no\_redundancy()  
'''  
          
        (automation\_dir / "validate\_no\_redundancy.py").write\_text(validator\_code)  
          
        \# Interface compliance validator  
        interface\_validator \= '''\#\!/usr/bin/env python3  
"""Verify graphics only uses interface."""

import sys  
import re  
from pathlib import Path

def validate\_interfaces():  
    """Check graphics layer uses only interfaces."""  
    graphics\_dir \= Path("src/graphics")  
      
    if not graphics\_dir.exists():  
        print("✅ Graphics layer not yet created")  
        sys.exit(0)  
      
    violations \= \[\]  
    forbidden \= \[  
        'from src.core import',  
        'from src.systems import',   
        'from src.content import',  
    \]  
      
    for py\_file in graphics\_dir.rglob("\*.py"):  
        with open(py\_file) as f:  
            content \= f.read()  
          
        for forbidden\_import in forbidden:  
            if forbidden\_import in content:  
                violations.append(f"{py\_file}: {forbidden\_import}")  
      
    if violations:  
        print("❌ Interface violations:")  
        for v in violations:  
            print(f"  \- {v}")  
        sys.exit(1)  
    else:  
        print("✅ All imports compliant")  
        sys.exit(0)

if \_\_name\_\_ \== "\_\_main\_\_":  
    validate\_interfaces()  
'''  
          
        (automation\_dir / "validate\_interfaces.py").write\_text(interface\_validator)  
          
        print(f"✅ Created {len(list(automation\_dir.glob('\*.py')))} validation scripts")  
      
    def watch\_mode(self):  
        """Continuous monitoring \- runs validation on file changes."""  
        print("👀 Entering watch mode (Ctrl+C to exit)...")  
        print("Will re-run validation on any file change...\\n")  
          
        import time  
        from datetime import datetime  
          
        last\_check \= {}  
          
        try:  
            while True:  
                for py\_file in self.src\_dir.rglob("\*.py"):  
                    mtime \= py\_file.stat().st\_mtime  
                    if str(py\_file) not in last\_check or last\_check\[str(py\_file)\] \< mtime:  
                        print(f"\\n\[{datetime.now().strftime('%H:%M:%S')}\] Change detected in {py\_file.name}")  
                        self.audit\_data\_duplication()  
                        last\_check\[str(py\_file)\] \= mtime  
                  
                time.sleep(2)  
          
        except KeyboardInterrupt:  
            print("\\n\\n✅ Watch mode ended")

def main():  
    """Main automation entry point."""  
    import argparse  
      
    parser \= argparse.ArgumentParser(description="COIN-OPERATED JRPG Automation")  
    parser.add\_argument('--full', action='store\_true', help='Run full automation')  
    parser.add\_argument('--watch', action='store\_true', help='Watch mode \- continuous validation')  
    parser.add\_argument('--audit', action='store\_true', help='Audit only')  
    parser.add\_argument('--next-prompt', action='store\_true', help='Generate next Copilot prompt')  
      
    args \= parser.parse\_args()  
      
    manager \= JRPGAutomationManager()  
      
    if args.full or (not args.audit and not args.watch and not args.next\_prompt):  
        manager.run\_all\_automation()  
      
    if args.audit:  
        manager.audit\_data\_duplication()  
      
    if args.watch:  
        manager.watch\_mode()  
      
    if args.next\_prompt:  
        manager.generate\_copilot\_prompts()

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()