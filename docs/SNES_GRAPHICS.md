# SNES-Style JRPG Visual System

## Overview

COIN:OPERATED JRPG now features an authentic **SNES-style 16-bit visual system** that recreates the look and feel of classic JRPGs like Final Fantasy IV-VI, Chrono Trigger, and Secret of Mana. All graphics are generated procedurally using authentic SNES hardware specifications and design aesthetics.

## SNES Hardware Specifications

The system accurately emulates SNES capabilities:

- **Resolution**: 256×224 pixels (NTSC standard)
- **Color Depth**: 15-bit RGB (5 bits per channel = 32,768 total colors)
- **Sprites**: 16×16 or 24×24 pixels
- **Tiles**: 8×8 or 16×16 pixels
- **Palette**: Limited colors per sprite (authentic SNES constraints)

## System Components

### 1. SNESPalette (`snes_palette.py`)

Authentic 15-bit color palette system matching SNES hardware.

**Features:**
- 5-bit per channel RGB (0-31 range)
- 60+ predefined SNES-era colors
- Character-specific palettes
- Environment colors (grass, water, stone, etc.)
- Magic effect colors
- UI colors (blue windows, yellow cursor)

**Usage:**
```python
from graphics import SNESPalette

# Get SNES colors
gold = SNESPalette.get('hero_gold')
blue = SNESPalette.get('hero_blue')

# Get character palette
coin_palette = SNESPalette.get_palette_for_character('coin')

# Create gradient
gradient = SNESPalette.get_gradient('fire_yellow', 'fire_red', 8)
```

### 2. SNESSpriteGenerator (`snes_sprite_generator.py`)

Generates pixel-perfect 16-bit character and enemy sprites.

**Character Sprites (16×16):**
- Coin (golden protagonist)
- Jinn-Lir (blue wizard)
- Coireena (armored warrior)
- Orbius (white mage)
- Selene (dark mage)
- Typhus (creature companion)

**Enemy Types:**
- Slime (classic blob enemy)
- Shadow (dark creature)
- Soldier (armored enemy)
- Generic monsters

**NPC Types:**
- Citizens
- Merchants
- Priests

**Features:**
- Pixel-perfect art
- SNES color limitations
- Character-appropriate designs
- Simple yet expressive

**Usage:**
```python
from graphics import SNESSpriteGenerator

sprite_gen = SNESSpriteGenerator(sprite_size=16)

# Generate characters
coin = sprite_gen.generate_coin_sprite()
jinn_lir = sprite_gen.generate_jinn_lir_sprite()
warrior = sprite_gen.generate_warrior_sprite()

# Generate enemies
slime = sprite_gen.generate_enemy_sprite('slime')
shadow = sprite_gen.generate_enemy_sprite('shadow')

# Generate NPCs
citizen = sprite_gen.generate_npc_sprite('citizen')
merchant = sprite_gen.generate_npc_sprite('merchant')

# Save sprite (scales 3x for visibility)
sprite_gen.save_sprite(coin, 'coin.png', 'output_dir')
```

### 3. SNESTileGenerator & SNESMapRenderer (`snes_tilemap.py`)

Tile-based map system for overworld and dungeons.

**Tile Types:**
- Grass (with variations)
- Water (animated)
- Dirt/Path
- Stone floor
- Walls (stone/wood)
- Trees
- Mountains

**Features:**
- 16×16 tile standard
- Animated tiles (water)
- Variation support
- Tile caching for performance
- Complete map rendering

**Usage:**
```python
from graphics import SNESTileGenerator, SNESMapRenderer

# Generate individual tiles
tile_gen = SNESTileGenerator(tile_size=16)
grass = tile_gen.generate_grass_tile(variant=0)
water = tile_gen.generate_water_tile(frame=0)  # Animated
tree = tile_gen.generate_tree_tile()

# Render complete map
map_renderer = SNESMapRenderer(tile_size=16)

# Define map (2D array of tile types)
map_data = [
    ['grass', 'grass', 'water', 'water'],
    ['grass', 'dirt', 'dirt', 'water'],
    ['grass', 'tree', 'grass', 'water'],
    ['grass', 'grass', 'grass', 'water'],
]

# Render map
map_img = map_renderer.render_map(map_data, width=4, height=4)

# Quick generation methods
overworld = map_renderer.create_simple_overworld(16, 16)
dungeon = map_renderer.create_dungeon_room(12, 10)

# Save map
map_renderer.save_map(overworld, 'overworld.png', 'maps')
```

### 4. SNESBattleScreen (`snes_battle_screen.py`)

Classic side-view battle system like FF4-6.

**Features:**
- Side-view battle layout
- Party on left, enemies on right
- Multiple background types (grassland, cave, castle)
- Battle menu windows
- HP/MP bars
- Character status displays
- Command menu system

**Battle Backgrounds:**
- Grassland (gradient sky + grass ground)
- Cave (dark stone environment)
- Castle (interior with pillars)

**Usage:**
```python
from graphics import SNESBattleScreen

battle = SNESBattleScreen()

# Generate battle background
bg = battle.generate_battle_background('grassland')

# Render complete battle
party = [
    (coin_sprite, "Coin"),
    (jinn_sprite, "Jinn-Lir")
]

enemies = [
    (shadow_sprite, "Shadow"),
    (slime_sprite, "Slime")
]

battle_screen = battle.render_battle_screen(party, enemies, 'grassland')

# Create battle UI elements
command_menu = battle.render_battle_command_menu(
    ["Attack", "Magic", "Item", "Defend"],
    selected=0
)

hp_bar = battle.render_hp_bar(85, 100, width=40)

status = battle.render_character_status("Coin", 85, 100, 30, 50)

# Generate complete scene
full_battle = battle.create_full_battle_scene()

# Save
battle.save_battle_screen(full_battle, 'battle.png', 'battles')
```

### 5. SNESUI (`snes_ui.py`)

Classic JRPG UI system with authentic SNES styling.

**UI Elements:**
- Text windows (multiple border styles)
- Dialogue boxes with speaker names
- Menu cursor (animated pointer)
- Main menu
- Status windows (HP/MP bars, character info)
- Item menus
- Save slot displays
- Title screen

**Window Styles:**
- Classic (FF-style double border)
- Fancy (ornate corners)
- Simple (single border)

**Features:**
- Dark blue window backgrounds (authentic SNES JRPG style)
- Light gray borders
- Yellow cursor
- Color-coded HP bars (green/yellow/red)
- Blue MP bars
- Simplified pixel fonts

**Usage:**
```python
from graphics import SNESUI

ui = SNESUI()

# Create windows
text_window = ui.create_text_window(200, 100, border_style='classic')
dialogue = ui.create_dialogue_box(240, 64, speaker_name="Coin")

# Create menus
main_menu = ui.create_main_menu(120, 140)
item_menu = ui.create_item_menu(["Potion", "Ether", "Elixir"], selected=0)

# Create status display
status = ui.create_status_window(
    char_name="Coin",
    level=12,
    hp=85,
    max_hp=100,
    mp=30,
    max_mp=50
)

# Create save slot
save_slot = ui.create_save_slot_display(
    slot_num=1,
    character_name="Coin",
    location="Acadmium City",
    playtime="12:34:56",
    level=12
)

# Create title screen
title = ui.create_title_screen("COIN:OPERATED")

# Save UI elements
ui.save_ui_element(main_menu, 'menu.png', 'ui_output')
```

### 6. SNESGameRenderer (`snes_renderer.py`)

Main rendering engine that combines all systems.

**Capabilities:**
- Complete scene rendering at SNES resolution (256×224)
- Overworld exploration with scrolling camera
- Battle scenes with full UI
- Menu screens
- Scene transitions (fade, wipe, battle swirl)
- Asset caching for performance

**Scene Types:**
- Title screen
- Overworld (tile-based with player sprite)
- Battle (side-view with UI)
- Menus (main, status, item, save)
- Dialogue (scene + dialogue box)

**Usage:**
```python
from graphics import SNESGameRenderer

renderer = SNESGameRenderer()

# Render overworld scene
map_data = [['grass'] * 20 for _ in range(20)]  # Simple grass map
overworld = renderer.render_overworld_scene(
    map_data,
    player_x=10,
    player_y=10,
    character_name='coin'
)

# Render battle
party_data = [
    ('coin', 85, 100, 30, 50),  # name, hp, max_hp, mp, max_mp
    ('jinn_lir', 120, 150, 45, 80)
]

enemy_data = [
    ('shadow', 'Shadow Beast'),
    ('slime', 'Blue Slime')
]

battle = renderer.render_battle(party_data, enemy_data, 'grassland')

# Render menu
menu_party = [
    {'name': 'Coin', 'level': 12, 'hp': 85, 'max_hp': 100, 'mp': 30, 'max_mp': 50},
    {'name': 'Jinn-Lir', 'level': 15, 'hp': 120, 'max_hp': 150, 'mp': 45, 'max_mp': 80}
]

menu = renderer.render_menu_screen('main', party=menu_party)

# Render title
title = renderer.render_menu_screen('title', title='COIN:OPERATED')

# Create transitions
fade = renderer.render_transition(scene1, scene2, 'fade', progress=0.5)
wipe = renderer.render_transition(scene1, scene2, 'wipe', progress=0.5)
battle_trans = renderer.render_transition(scene1, scene2, 'battle_swirl', progress=0.5)

# Save scene (scales 2x for visibility)
renderer.save_scene(overworld, 'overworld.png', 'scenes', scale=2)

# Generate complete demo
renderer.create_demo_scenes('output_directory')
```

## Demo Script

Run the included demo to generate sample SNES-style graphics:

```bash
python3 snes_demo.py
```

This generates:
- 5 character sprites (Coin, Jinn-Lir, Coireena, Orbius, Selene)
- 3 enemy types (Slime, Shadow, Soldier)
- 2 complete maps (Overworld 16×16, Dungeon 12×10)
- 1 battle screen (full scene with UI)
- 5 UI elements (title, dialogue, menus, status, save)
- 4 complete game scenes (title, overworld, battle, menu)

Output is saved to `snes_demo_output/` directory.

## Technical Details

### SNES Color Conversion

Colors are defined in authentic 5-bit format:

```python
# SNES uses 5 bits per channel (0-31)
def snes_rgb(r5, g5, b5):
    # Convert to 8-bit (0-255) for PIL
    r8 = int((r5 / 31.0) * 255)
    g8 = int((g5 / 31.0) * 255)
    b8 = int((b5 / 31.0) * 255)
    return (r8, g8, b8, 255)

# Example: Pure red in SNES
red = snes_rgb(31, 0, 0)  # Maximum red, no green/blue
```

### Resolution & Scaling

- **Native Resolution**: 256×224 pixels (SNES standard)
- **Display Scaling**: 2× or 3× for modern screens
- **Sprite Scaling**: NEAREST neighbor (pixel-perfect)
- **Map Viewport**: Scrolling camera centered on player

### Pixel Art Guidelines

When creating new sprites or tiles:

1. **Size**: Use 16×16 for sprites, tiles
2. **Colors**: Limit to 4-6 colors per sprite
3. **Style**: Simple, clean, readable at small size
4. **Palette**: Use SNESPalette.get() for authentic colors
5. **Detail**: Less is more - SNES sprites were simple

### Performance

- **Sprite Generation**: ~10-30ms per sprite
- **Tile Generation**: ~5-15ms per tile
- **Map Rendering**: ~50-200ms (depends on size)
- **Battle Screen**: ~100-300ms (full scene)
- **UI Elements**: ~20-50ms per element

**Optimization:**
- Sprites and tiles are cached after first generation
- Use renderer.get_character_sprite() for cached access
- Pre-generate common assets at game start

## Integration with Game Engine

### Basic Game Loop

```python
from graphics import SNESGameRenderer

class SNESJRPGGame:
    def __init__(self):
        self.renderer = SNESGameRenderer()
        self.current_scene = None
        self.game_state = 'overworld'  # or 'battle', 'menu'
    
    def update_display(self):
        if self.game_state == 'overworld':
            self.current_scene = self.renderer.render_overworld_scene(
                self.map_data,
                self.player.x,
                self.player.y,
                self.player.character_name
            )
        
        elif self.game_state == 'battle':
            self.current_scene = self.renderer.render_battle(
                self.party_data,
                self.enemy_data,
                self.battle_background
            )
        
        elif self.game_state == 'menu':
            self.current_scene = self.renderer.render_menu_screen(
                self.menu_type,
                party=self.party_data
            )
        
        # Display self.current_scene to screen
        self.display(self.current_scene)
```

### Save Screenshots

```python
# Save current game state as image
renderer.save_scene(current_scene, 'screenshot.png', 'screenshots')

# Save with different scales
renderer.save_scene(scene, 'small.png', scale=1)  # Native 256×224
renderer.save_scene(scene, 'normal.png', scale=2)  # 512×448
renderer.save_scene(scene, 'large.png', scale=3)  # 768×672
```

## Comparison: Modern vs SNES System

| Feature | Modern System | SNES System |
|---------|--------------|-------------|
| **Sprite Size** | 32×32 pixels | 16×16 pixels |
| **Resolution** | Flexible | 256×224 fixed |
| **Color Depth** | 32-bit RGBA | 15-bit RGB |
| **Style** | Modern pixel art | Authentic 16-bit |
| **UI** | Modern design | Classic JRPG |
| **Maps** | Procedural | Tile-based |
| **Battles** | Abstract | Side-view screen |

Both systems coexist - choose based on desired aesthetic!

## Authentic SNES Features

### What Makes It SNES-Style?

✅ **Resolution**: True 256×224 SNES resolution
✅ **Color Palette**: 15-bit RGB (5 bits per channel)
✅ **Sprites**: 16×16 pixel character sprites
✅ **Tiles**: 16×16 tile-based maps
✅ **UI**: Dark blue windows with light borders
✅ **Battles**: Side-view layout (FF4-6 style)
✅ **Menus**: Classic JRPG menu design
✅ **Text Boxes**: Bottom-screen dialogue boxes
✅ **Cursor**: Yellow pointing cursor
✅ **HP Bars**: Color-coded (green/yellow/red)
✅ **Pixel Perfect**: No anti-aliasing, NEAREST scaling

### Inspired By

- **Final Fantasy IV-VI** (battle system, UI style)
- **Chrono Trigger** (sprite quality, color palette)
- **Secret of Mana** (overworld style)
- **Dragon Quest** (menu layouts)
- **Earthbound** (dialogue boxes)

## Customization

### Creating New Character Sprites

Add to `snes_sprite_generator.py`:

```python
def generate_new_character_sprite(self) -> Image:
    img = Image.new('RGBA', (self.sprite_size, self.sprite_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Get colors from palette
    pal = self.palette.get_palette_for_character('custom')
    
    # Draw character (16×16 pixels)
    # ... your pixel art code ...
    
    return img
```

### Creating New Tile Types

Add to `snes_tilemap.py`:

```python
def generate_custom_tile(self) -> Image:
    img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw tile pattern
    # ... your tile code ...
    
    return img
```

### Adding New UI Styles

Modify `snes_ui.py` border styles or create new window types.

## Future Enhancements

Potential additions to the SNES system:

- [ ] Character walking animations (4-frame cycles)
- [ ] Battle animations (attack, spell effects)
- [ ] More tile types (lava, ice, desert)
- [ ] Weather effects (rain, snow)
- [ ] Mode 7-style scaling effects
- [ ] Enhanced transition effects
- [ ] Parallax scrolling backgrounds
- [ ] Character portraits for dialogue
- [ ] Equipment sprites (visible on character)
- [ ] Status effect indicators

## Troubleshooting

### Sprites look blurry
- Ensure using `Image.NEAREST` for resizing
- Never use BILINEAR or LANCZOS on pixel art

### Colors look wrong
- Use SNESPalette.get() for all colors
- Verify 5-bit RGB conversion

### Maps don't tile properly
- Check tile size matches (16×16)
- Ensure transparent areas use alpha channel

### Performance issues
- Pre-generate and cache common sprites
- Use renderer's built-in caching
- Generate assets on background thread

## Support

For SNES system questions:
1. Check this documentation
2. Run `snes_demo.py` for examples
3. Review source code comments
4. Examine generated output

---

**COIN:OPERATED JRPG - Authentic SNES-Style Graphics**  
*Just like the golden age of 16-bit RPGs*
