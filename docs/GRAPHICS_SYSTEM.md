# Procedural Graphics System Documentation

## Overview

The COIN:OPERATED JRPG features a complete procedural graphics system that generates all visual assets through code. No external image files or art assets are required - everything from character sprites to UI elements is generated programmatically using Python and PIL (Pillow).

## System Architecture

### Core Modules

The graphics system consists of six main modules:

1. **ColorPalette** - Centralized color management
2. **SpriteGenerator** - Character and enemy sprites
3. **AnimationGenerator** - Animated sprite sequences
4. **EffectGenerator** - Visual effects for magic and combat
5. **UIGenerator** - User interface elements
6. **EnvironmentGenerator** - Tiles, props, and backgrounds

## Module Details

### ColorPalette (`color_palette.py`)

Provides consistent color management across all graphics modules.

**Features:**
- 40+ predefined colors for various game elements
- Character-specific color palettes
- Faction color schemes (Light Cabal, Dark Cabal, Drift Empire)
- Color manipulation utilities (lighten, darken, blend, lerp)
- Alpha channel support

**Usage:**
```python
from graphics import ColorPalette

# Get predefined colors
gold = ColorPalette.get('coin_gold')
magic = ColorPalette.get('magic_time')

# Manipulate colors
lighter = ColorPalette.lighten(gold, 0.3)
darker = ColorPalette.darken(gold, 0.2)
blended = ColorPalette.blend(gold, magic, 0.5)

# Character palettes
coin_palette = ColorPalette.get_character_palette('coin')
```

### SpriteGenerator (`sprite_generator.py`)

Generates pixel art sprites for all game characters and enemies.

**Character Sprites:**
- Coin (protagonist - golden coin form)
- Jinn-Lir (wizard companion)
- Orbius (ancient master)
- Coireena (warrior)
- Selene (dark mage)
- Typhus (ancient creature)

**Enemy Types:**
- Shadow Creature
- Corrupted Coin
- Time Wraith
- Cabal Soldier

**Features:**
- 32x32 pixel character sprites
- Character-specific visual designs
- Procedurally generated details (robes, weapons, effects)
- Consistent shading and highlighting

**Usage:**
```python
from graphics import SpriteGenerator

sprite_gen = SpriteGenerator()

# Generate character sprites
coin = sprite_gen.generate_coin_sprite()
jinn_lir = sprite_gen.generate_jinn_lir_sprite()

# Generate enemy sprites
shadow = sprite_gen.generate_enemy_sprite('shadow_creature')
wraith = sprite_gen.generate_enemy_sprite('time_wraith')

# Save sprites
coin.save('coin.png', 'PNG')
```

### AnimationGenerator (`animation_generator.py`)

Creates animated sprite sequences from base sprites.

**Animation Types:**
- Walk cycles (4-direction movement)
- Attack sequences
- Spell casting
- Damage flashing
- Idle breathing
- Victory celebrations
- Death fading

**Features:**
- Frame-by-frame animation generation
- Spritesheet creation (combines frames into single image)
- Configurable frame counts and durations
- Smooth transitions between frames

**Usage:**
```python
from graphics import SpriteGenerator, AnimationGenerator

sprite_gen = SpriteGenerator()
anim_gen = AnimationGenerator()

coin_sprite = sprite_gen.generate_coin_sprite()

# Generate animations
walk_frames = anim_gen.generate_walk_animation(coin_sprite)
attack_frames = anim_gen.generate_attack_animation(coin_sprite)
cast_frames = anim_gen.generate_cast_animation(coin_sprite)

# Create spritesheet
spritesheet = anim_gen.create_spritesheet(walk_frames, columns=4)
spritesheet.save('coin_walk_spritesheet.png', 'PNG')
```

### EffectGenerator (`effect_generator.py`)

Produces visual effects for magic spells and combat actions.

**Magic Effects:**
- Time Magic (spirals, clock symbols)
- Fire Magic (rising flames, embers)
- Ice Magic (crystals, frost)
- Lightning Magic (electric bolts)
- Healing Magic (sparkles, restoration)
- Dark Magic (wisps, shadows)

**Combat Effects:**
- Slash effects (weapon strikes)
- Impact effects (hit confirmation)
- Particle systems (explosions, sparkles)

**Features:**
- Multi-frame animated effects
- Particle-based systems
- Element-specific visual themes
- Configurable intensity and size

**Usage:**
```python
from graphics import EffectGenerator

effect_gen = EffectGenerator()

# Generate magic effects (returns list of frames)
fire_effect = effect_gen.generate_magic_effect('fire', num_frames=8)
time_effect = effect_gen.generate_magic_effect('time', num_frames=10)
healing_effect = effect_gen.generate_magic_effect('healing', num_frames=6)

# Generate combat effects
slash = effect_gen.generate_slash_effect()
impact = effect_gen.generate_impact_effect()

# Particle effects
particles = effect_gen.generate_particle_effect(num_particles=20, particle_type='sparkle')

# Save frames
for i, frame in enumerate(fire_effect):
    frame.save(f'fire_frame_{i}.png', 'PNG')
```

### UIGenerator (`ui_generator.py`)

Creates all user interface elements procedurally.

**UI Elements:**
- Buttons (normal, primary, danger, success styles)
- Windows and dialog boxes
- Health bars (color-coded by percentage)
- Mana/MP bars
- Progress bars
- Icons (attack, magic, defense, item, coin)
- Cursors/pointers
- Menu panels (faction-themed)
- Dialogue boxes with name plates

**Features:**
- Multiple style variations
- Faction-themed designs
- Gradient and shadow effects
- Text rendering with shadows
- Responsive sizing

**Usage:**
```python
from graphics import UIGenerator

ui_gen = UIGenerator()

# Generate buttons
normal_btn = ui_gen.generate_button(120, 40, "Start", 'normal')
primary_btn = ui_gen.generate_button(120, 40, "Attack", 'primary')
danger_btn = ui_gen.generate_button(120, 40, "Quit", 'danger')

# Generate windows
menu_window = ui_gen.generate_window(320, 200, "Main Menu")

# Generate bars
health = ui_gen.generate_health_bar(200, 20, current=75, maximum=100)
mana = ui_gen.generate_mana_bar(200, 20, current=50, maximum=100)
progress = ui_gen.generate_progress_bar(200, 20, progress=0.65)

# Generate icons
attack_icon = ui_gen.generate_icon('attack', size=32)
magic_icon = ui_gen.generate_icon('magic', size=32)
coin_icon = ui_gen.generate_icon('coin', size=32)

# Generate faction-themed panels
light_panel = ui_gen.generate_menu_panel(300, 200, 'light_cabal')
dark_panel = ui_gen.generate_menu_panel(300, 200, 'dark_cabal')

# Generate dialogue box
dialogue = ui_gen.generate_dialogue_box(600, 120, character_name="Coin")

# Save UI elements
menu_window.save('menu_window.png', 'PNG')
```

### EnvironmentGenerator (`environment_generator.py`)

Generates environment tiles, props, and background scenes.

**Tile Types:**
- Grass
- Dirt
- Stone/Rock
- Water (animated)
- Wood floor
- Metal floor

**Walls:**
- Stone walls
- Wooden walls
- Metal walls

**Props:**
- Trees (small, medium, large)
- Rocks/Boulders (small, medium, large)

**Backgrounds:**
- Sky
- Night sky with stars
- Cave
- Forest
- Temple interior

**Features:**
- Configurable tile size
- Variation support (multiple versions of same tile)
- Animated tiles (water)
- Layered backgrounds
- Procedural texture generation

**Usage:**
```python
from graphics import EnvironmentGenerator

env_gen = EnvironmentGenerator(tile_size=32)

# Generate tiles
grass = env_gen.generate_grass_tile(variation=0)
dirt = env_gen.generate_dirt_tile(variation=1)
stone = env_gen.generate_stone_tile(variation=2)
water = env_gen.generate_water_tile(frame=0)  # Animated
wood = env_gen.generate_wood_tile()
metal = env_gen.generate_metal_tile()

# Generate walls
stone_wall = env_gen.generate_wall('stone', width=64, height=96)
wood_wall = env_gen.generate_wall('wood', width=64, height=96)

# Generate props
tree_small = env_gen.generate_tree('small')
tree_medium = env_gen.generate_tree('medium')
tree_large = env_gen.generate_tree('large')
rock = env_gen.generate_rock('medium')

# Generate backgrounds
sky_bg = env_gen.generate_background(640, 480, 'sky')
night_bg = env_gen.generate_background(640, 480, 'night')
cave_bg = env_gen.generate_background(640, 480, 'cave')
forest_bg = env_gen.generate_background(640, 480, 'forest')
temple_bg = env_gen.generate_background(640, 480, 'temple')

# Generate complete tileset
env_gen.generate_tileset(output_dir='my_tiles')

# Save tiles
grass.save('grass_tile.png', 'PNG')
```

## Demo Script

Run the included demo script to generate sample graphics:

```bash
python graphics_demo.py
```

This will create a `generated_graphics` directory containing:
- Character sprites
- Enemy sprites
- Animation frames and spritesheets
- Magic and combat effects
- UI elements
- Environment tiles and props
- Background scenes
- Color palette reference

## Integration with Game Engine

### Basic Integration

```python
from graphics import (
    SpriteGenerator,
    AnimationGenerator,
    UIGenerator,
    EffectGenerator,
    EnvironmentGenerator
)

class Game:
    def __init__(self):
        self.sprite_gen = SpriteGenerator()
        self.anim_gen = AnimationGenerator()
        self.ui_gen = UIGenerator()
        self.effect_gen = EffectGenerator()
        self.env_gen = EnvironmentGenerator()
        
        # Generate game assets on startup
        self.load_assets()
    
    def load_assets(self):
        """Generate all game assets"""
        # Character sprites
        self.coin_sprite = self.sprite_gen.generate_coin_sprite()
        
        # Animations
        self.coin_walk = self.anim_gen.generate_walk_animation(self.coin_sprite)
        self.coin_attack = self.anim_gen.generate_attack_animation(self.coin_sprite)
        
        # UI elements
        self.health_bar_template = self.ui_gen.generate_health_bar(200, 20, 100, 100)
        self.menu_window = self.ui_gen.generate_window(320, 240, "Menu")
        
        # Environment
        self.grass_tile = self.env_gen.generate_grass_tile()
        self.background = self.env_gen.generate_background(640, 480, 'forest')
```

### Caching Assets

For performance, generate assets once and cache them:

```python
class AssetCache:
    def __init__(self):
        self.cache = {}
        self.sprite_gen = SpriteGenerator()
    
    def get_sprite(self, character_name):
        if character_name not in self.cache:
            if character_name == 'coin':
                self.cache[character_name] = self.sprite_gen.generate_coin_sprite()
            elif character_name == 'jinn_lir':
                self.cache[character_name] = self.sprite_gen.generate_jinn_lir_sprite()
            # ... etc
        return self.cache[character_name]
```

### Dynamic Generation

Generate assets on-demand for variations:

```python
# Generate enemy with random color variation
def spawn_enemy(enemy_type):
    sprite = sprite_gen.generate_enemy_sprite(enemy_type)
    # Sprite is unique each time
    return Enemy(sprite)

# Generate UI with current stats
def update_health_bar(current_hp, max_hp):
    return ui_gen.generate_health_bar(200, 20, current_hp, max_hp)
```

## Performance Considerations

### Generation Time

- **Sprites**: ~10-50ms per sprite
- **Animations**: ~50-200ms per animation sequence
- **Effects**: ~100-500ms per effect sequence
- **UI Elements**: ~5-30ms per element
- **Tiles**: ~5-15ms per tile

### Optimization Strategies

1. **Pre-generate at startup**: Generate all common assets during game initialization
2. **Cache aggressively**: Store generated assets in memory
3. **Lazy loading**: Generate assets only when first needed
4. **Background generation**: Generate non-critical assets in background threads
5. **Spritesheet usage**: Combine animation frames into single images

### Memory Usage

- Each 32x32 sprite: ~4KB
- Each animation (8 frames): ~32KB
- Each effect sequence: ~50-100KB
- Total for all assets: ~5-10MB

## Advantages of Procedural Graphics

1. **No external dependencies**: No need for image files or art assets
2. **Consistency**: All graphics follow same style and color palette
3. **Flexibility**: Easy to modify colors, sizes, and styles
4. **Variation**: Generate unlimited variations procedurally
5. **Small file size**: Entire graphics system is pure code
6. **Version control friendly**: No binary image files to track
7. **Dynamic theming**: Change entire visual style at runtime
8. **Accessibility**: Can adjust colors for different vision needs

## Customization

### Modifying Colors

Edit `color_palette.py` to change the game's color scheme:

```python
COLORS = {
    'coin_gold': (255, 215, 0),  # Change gold color
    'magic_time': (138, 43, 226),  # Change time magic color
    # ... etc
}
```

### Adding New Sprites

Add new character methods to `sprite_generator.py`:

```python
def generate_new_character_sprite(self) -> Image:
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Your sprite generation code here
    
    return img
```

### Creating Custom Effects

Add new effect types to `effect_generator.py`:

```python
def generate_custom_effect(self, num_frames: int = 8) -> List[Image]:
    frames = []
    for i in range(num_frames):
        frame = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Your effect generation code here
        
        frames.append(frame)
    return frames
```

## Technical Requirements

- **Python**: 3.8+
- **PIL/Pillow**: 9.0+

Install dependencies:
```bash
pip install Pillow
```

## Future Enhancements

Potential additions to the graphics system:

- Particle system improvements (physics-based)
- Procedural sound effect generation
- Dynamic lighting and shadows
- Weather effects (rain, snow, fog)
- More animation types (jump, run, crouch)
- Equipment variations (different weapons/armor)
- Facial expressions and emotions
- Special move effects
- Status effect indicators
- Damage numbers and floating text

## Support

For questions or issues with the procedural graphics system:
1. Check this documentation
2. Run `graphics_demo.py` to see examples
3. Review the source code comments in each module
4. Examine generated output for visual reference

---

*COIN:OPERATED JRPG - All graphics generated by code*
