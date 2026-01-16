#!/usr/bin/env python3
"""
Quick test of procedural graphics system
"""

import sys
import os

# Add python-core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'coin-operated', 'COIN-OPERATED-JRPG', 'python-core'))

try:
    print("Testing procedural graphics system...")
    print()
    
    # Test imports
    print("✓ Importing modules...")
    from graphics import (
        ColorPalette,
        SpriteGenerator,
        AnimationGenerator,
        EffectGenerator,
        UIGenerator,
        EnvironmentGenerator
    )
    
    # Test color palette
    print("✓ Testing ColorPalette...")
    gold = ColorPalette.get('coin_gold')
    assert gold == (255, 215, 0, 255)
    
    # Test sprite generation
    print("✓ Testing SpriteGenerator...")
    sprite_gen = SpriteGenerator()
    coin_sprite = sprite_gen.generate_coin_sprite()
    assert coin_sprite.size == (32, 32)
    assert coin_sprite.mode == 'RGBA'
    
    # Test animation generation
    print("✓ Testing AnimationGenerator...")
    anim_gen = AnimationGenerator()
    walk_frames = anim_gen.generate_walk_animation(coin_sprite)
    assert len(walk_frames) == 4
    
    # Test effect generation
    print("✓ Testing EffectGenerator...")
    effect_gen = EffectGenerator()
    fire_effect = effect_gen.generate_magic_effect('fire', num_frames=4)
    assert len(fire_effect) == 4
    
    # Test UI generation
    print("✓ Testing UIGenerator...")
    ui_gen = UIGenerator()
    button = ui_gen.generate_button(120, 40, "Test", 'normal')
    assert button.size == (120, 40)
    
    # Test environment generation
    print("✓ Testing EnvironmentGenerator...")
    env_gen = EnvironmentGenerator(tile_size=32)
    grass_tile = env_gen.generate_grass_tile()
    assert grass_tile.size == (32, 32)
    
    print()
    print("=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print()
    print("The procedural graphics system is working correctly.")
    print("All graphics can be generated on-demand without external assets.")
    print()
    
except Exception as e:
    print(f"\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
