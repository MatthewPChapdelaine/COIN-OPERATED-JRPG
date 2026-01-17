#!/usr/bin/env python3
"""
COIN:OPERATED JRPG - Desktop GUI Launcher
No terminal required - launches directly with GUI splash screen
"""

import sys
import os

# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# Add python-core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-core'))

def show_splash_screen():
    """Show splash screen while loading"""
    import pygame
    pygame.init()
    
    # Create splash window (no window decorations initially)
    splash = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("COIN:OPERATED - Loading...")
    
    # Colors
    DARK_BG = (20, 20, 30)
    GOLD = (255, 215, 0)
    LIGHT_GOLD = (255, 235, 100)
    SILVER = (192, 192, 192)
    PURPLE = (138, 43, 226)
    
    # Fonts
    try:
        title_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 32)
        text_font = pygame.font.Font(None, 24)
    except:
        title_font = pygame.font.SysFont('serif', 72, bold=True)
        subtitle_font = pygame.font.SysFont('serif', 32)
        text_font = pygame.font.SysFont('serif', 24)
    
    # Draw splash screen
    splash.fill(DARK_BG)
    
    # Draw golden coin in center
    coin_center = (300, 150)
    coin_radius = 60
    
    # Outer glow
    for i in range(5, 0, -1):
        alpha_surface = pygame.Surface((600, 400), pygame.SRCALPHA)
        color = (*GOLD[:3], 30 * i)
        pygame.draw.circle(alpha_surface, color, coin_center, coin_radius + i * 5)
        splash.blit(alpha_surface, (0, 0))
    
    # Main coin body
    pygame.draw.circle(splash, GOLD, coin_center, coin_radius)
    pygame.draw.circle(splash, LIGHT_GOLD, coin_center, coin_radius, 3)
    
    # Inner circle
    pygame.draw.circle(splash, LIGHT_GOLD, coin_center, coin_radius - 10, 2)
    
    # Center symbol (stylized "C")
    pygame.draw.arc(splash, SILVER, 
                    pygame.Rect(coin_center[0] - 25, coin_center[1] - 30, 50, 60),
                    0.3, 5.9, 5)
    
    # Title
    title_text = title_font.render("COIN:OPERATED", True, GOLD)
    title_rect = title_text.get_rect(center=(300, 270))
    
    # Title shadow
    title_shadow = title_font.render("COIN:OPERATED", True, (50, 50, 50))
    splash.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    splash.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_text = subtitle_font.render("A Universe Beyond the Universe", True, PURPLE)
    subtitle_rect = subtitle_text.get_rect(center=(300, 315))
    splash.blit(subtitle_text, subtitle_rect)
    
    # Loading text
    loading_text = text_font.render("Loading... Please wait", True, SILVER)
    loading_rect = loading_text.get_rect(center=(300, 360))
    splash.blit(loading_text, loading_rect)
    
    pygame.display.flip()
    return splash

def main():
    """Launch the game with GUI splash screen"""
    
    # Check for pygame first
    try:
        import pygame
    except ImportError:
        # Show error dialog using tkinter (always available on Linux)
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Missing Dependency",
                "Pygame is not installed!\n\n"
                "To install, run:\n"
                "pip install pygame\n\n"
                "Or use your package manager:\n"
                "sudo apt install python3-pygame"
            )
            root.destroy()
        except:
            print("ERROR: Pygame not installed!")
            print("Install with: pip install pygame")
        sys.exit(1)
    
    # Show splash screen
    splash = show_splash_screen()
    
    # Import game modules (this takes time, so splash is shown)
    try:
        from core.game_engine import GameEngine, GameState
        from core.character import Coin
        from graphics.adapter import GraphicsAdapter
        from graphics.snes_pygame_renderer import Retro16PygameRenderer
        from config import get_config
    except ImportError as e:
        pygame.quit()
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Game Error",
                f"Failed to load game modules:\n{e}\n\n"
                f"Make sure you're running from the game directory."
            )
            root.destroy()
        except:
            print(f"ERROR: {e}")
        sys.exit(1)
    
    # Load configuration
    config = get_config()
    
    # Initialize game engine
    try:
        engine = GameEngine()
        engine.initialize()
    except Exception as e:
        pygame.quit()
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Game Error", f"Failed to initialize game:\n{e}")
            root.destroy()
        except:
            print(f"ERROR: {e}")
        sys.exit(1)
    
    # Create Coin (the protagonist)
    from core.character import CharacterRole, CharacterFaction
    coin = Coin(age_state="young")
    coin.stats.max_hp = 100
    coin.stats.current_hp = 100
    coin.stats.max_mp = 50
    coin.stats.current_mp = 50
    engine.player = coin
    engine.state = GameState.IN_GAME
    
    # Create adapter
    adapter = GraphicsAdapter(engine)
    
    # Get scale from config (default 3x for 16-bit look)
    scale = config.get('graphics.scale', 3)
    
    # Close splash and create game window
    pygame.quit()
    pygame.init()
    
    # Create Retro16 renderer (authentic 16-bit JRPG style)
    try:
        renderer = Retro16PygameRenderer(adapter, scale=scale)
        adapter.register_event_listener(renderer)
    except Exception as e:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Graphics Error", f"Failed to initialize graphics:\n{e}")
            root.destroy()
        except:
            print(f"ERROR: {e}")
        sys.exit(1)
    
    # Run the game
    try:
        renderer.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Game Error", f"An error occurred:\n{e}")
            root.destroy()
        except:
            print(f"ERROR: {e}")
    finally:
        # Save config on exit
        config.save()
        pygame.quit()


if __name__ == "__main__":
    main()
