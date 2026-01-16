#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Graphics System Test Suite
Comprehensive testing for all graphics components.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add python-core to path
sys.path.insert(0, str(Path(__file__).parent / 'python-core'))


class TestInterfaces(unittest.TestCase):
    """Test interface definitions."""
    
    def test_interfaces_exist(self):
        """Test that all interfaces are defined."""
        from interfaces import GameStateInterface, GameCommandInterface, GameEventInterface
        
        self.assertTrue(hasattr(GameStateInterface, 'get_player_location'))
        self.assertTrue(hasattr(GameStateInterface, 'get_party_members'))
        self.assertTrue(hasattr(GameStateInterface, 'get_current_encounter'))
        self.assertTrue(hasattr(GameCommandInterface, 'player_move'))
        self.assertTrue(hasattr(GameCommandInterface, 'save_game'))
        self.assertTrue(hasattr(GameEventInterface, 'on_combat_started'))
    
    def test_interface_methods(self):
        """Test interface method signatures."""
        from interfaces import GameStateInterface
        import inspect
        
        # Check get_party_members returns List[Dict]
        sig = inspect.signature(GameStateInterface.get_party_members)
        self.assertIsNotNone(sig.return_annotation)


class TestGraphicsAdapter(unittest.TestCase):
    """Test graphics adapter implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        from graphics.adapter import GraphicsAdapter
        
        # Create mock game engine
        self.mock_engine = Mock()
        self.mock_engine.state = 'in_game'
        self.mock_engine.player = Mock()
        self.mock_engine.player.name = "TestPlayer"
        self.mock_engine.player.stats = Mock()
        self.mock_engine.player.stats.current_hp = 100
        self.mock_engine.player.stats.max_hp = 100
        self.mock_engine.player.stats.current_mp = 50
        self.mock_engine.player.stats.max_mp = 50
        self.mock_engine.party = []
        self.mock_engine.current_location = Mock()
        self.mock_engine.current_location.name = "Test Location"
        self.mock_engine.current_location.description = "Test"
        self.mock_engine.current_location.npcs = []
        
        self.adapter = GraphicsAdapter(self.mock_engine)
    
    def test_adapter_initialization(self):
        """Test adapter initializes correctly."""
        self.assertIsNotNone(self.adapter.engine)
        self.assertEqual(len(self.adapter.event_listeners), 0)
    
    def test_get_player_location(self):
        """Test getting player location."""
        location = self.adapter.get_player_location()
        
        self.assertIsInstance(location, dict)
        self.assertIn('name', location)
        self.assertEqual(location['name'], "Test Location")
    
    def test_get_party_members(self):
        """Test getting party members."""
        party = self.adapter.get_party_members()
        
        self.assertIsInstance(party, list)
        self.assertGreater(len(party), 0)  # Should include player
        self.assertIn('name', party[0])
        self.assertEqual(party[0]['name'], "TestPlayer")
    
    def test_get_available_actions(self):
        """Test getting available actions."""
        actions = self.adapter.get_available_actions()
        
        self.assertIsInstance(actions, list)
        self.assertIn('move_up', actions)
        self.assertIn('interact', actions)
    
    def test_event_listener_registration(self):
        """Test event listener registration."""
        listener = Mock()
        self.adapter.register_event_listener(listener)
        
        self.assertEqual(len(self.adapter.event_listeners), 1)
        self.assertEqual(self.adapter.event_listeners[0], listener)
    
    def test_event_notification(self):
        """Test event notifications."""
        listener = Mock()
        listener.on_damage_dealt = Mock()
        
        self.adapter.register_event_listener(listener)
        self.adapter._notify_listeners('on_damage_dealt', 50, 'enemy_1')
        
        listener.on_damage_dealt.assert_called_once_with(50, 'enemy_1')


class TestConfiguration(unittest.TestCase):
    """Test configuration manager."""
    
    def test_default_config_loads(self):
        """Test default configuration loads."""
        from config import ConfigManager
        
        config = ConfigManager()
        self.assertIsNotNone(config.config)
        self.assertIn('graphics', config.config)
        self.assertIn('mode', config.config['graphics'])
    
    def test_get_config_value(self):
        """Test getting config value."""
        from config import ConfigManager
        
        config = ConfigManager()
        mode = config.get('graphics.mode')
        
        self.assertIsNotNone(mode)
        self.assertIn(mode, ['text', 'graphics', 'retro16'])
    
    def test_set_config_value(self):
        """Test setting config value."""
        from config import ConfigManager
        
        config = ConfigManager()
        config.set('graphics.mode', 'test_mode')
        
        self.assertEqual(config.get('graphics.mode'), 'test_mode')
    
    def test_get_resolution(self):
        """Test getting resolution."""
        from config import ConfigManager
        
        config = ConfigManager()
        resolution = config.get_resolution()
        
        self.assertIsInstance(resolution, tuple)
        self.assertEqual(len(resolution), 2)
        self.assertGreater(resolution[0], 0)
        self.assertGreater(resolution[1], 0)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_clamp(self):
        """Test clamp function."""
        from utils import clamp
        
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-5, 0, 10), 0)
        self.assertEqual(clamp(15, 0, 10), 10)
    
    def test_lerp(self):
        """Test linear interpolation."""
        from utils import lerp
        
        self.assertEqual(lerp(0, 10, 0), 0)
        self.assertEqual(lerp(0, 10, 1), 10)
        self.assertEqual(lerp(0, 10, 0.5), 5)
    
    def test_color_lerp(self):
        """Test color interpolation."""
        from utils import color_lerp
        
        color1 = (0, 0, 0)
        color2 = (255, 255, 255)
        
        result = color_lerp(color1, color2, 0.5)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(0 <= c <= 255 for c in result))
    
    def test_validate_mode(self):
        """Test mode validation."""
        from utils import validate_mode
        
        self.assertTrue(validate_mode('text'))
        self.assertTrue(validate_mode('graphics'))
        self.assertTrue(validate_mode('retro16'))
        self.assertFalse(validate_mode('invalid'))
    
    def test_format_time(self):
        """Test time formatting."""
        from utils import format_time
        
        self.assertEqual(format_time(30), "30s")
        self.assertEqual(format_time(90), "1m 30s")
        self.assertEqual(format_time(3665), "1h 1m 5s")


class TestValidation(unittest.TestCase):
    """Test validation scripts."""
    
    def test_interface_validator_exists(self):
        """Test interface validator script exists."""
        validator_path = Path(__file__).parent / 'automation' / 'validate_interfaces.py'
        self.assertTrue(validator_path.exists())
    
    def test_redundancy_validator_exists(self):
        """Test redundancy validator script exists."""
        validator_path = Path(__file__).parent / 'automation' / 'validate_no_redundancy.py'
        self.assertTrue(validator_path.exists())


class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def test_adapter_with_mock_engine(self):
        """Test adapter works with mock engine."""
        from graphics.adapter import GraphicsAdapter
        
        engine = Mock()
        engine.state = 'in_game'
        engine.player = Mock()
        engine.player.name = "Test"
        engine.player.stats = Mock()
        engine.player.stats.current_hp = 100
        engine.player.stats.max_hp = 100
        engine.party = []
        engine.current_location = Mock()
        engine.current_location.name = "Test"
        engine.current_location.description = ""
        engine.current_location.npcs = []
        
        adapter = GraphicsAdapter(engine)
        
        # Test various interface methods
        location = adapter.get_player_location()
        party = adapter.get_party_members()
        actions = adapter.get_available_actions()
        ui = adapter.get_ui_elements()
        
        self.assertIsInstance(location, dict)
        self.assertIsInstance(party, list)
        self.assertIsInstance(actions, list)
        self.assertIsInstance(ui, dict)
    
    def test_event_flow(self):
        """Test event flow through system."""
        from graphics.adapter import GraphicsAdapter
        
        engine = Mock()
        adapter = GraphicsAdapter(engine)
        
        # Create mock listener
        listener = Mock()
        listener.on_combat_started = Mock()
        listener.on_damage_dealt = Mock()
        
        adapter.register_event_listener(listener)
        
        # Trigger events
        adapter._notify_listeners('on_combat_started', {'test': 'data'})
        adapter._notify_listeners('on_damage_dealt', 50, 'target')
        
        # Verify calls
        listener.on_combat_started.assert_called_once()
        listener.on_damage_dealt.assert_called_once_with(50, 'target')


class TestFileStructure(unittest.TestCase):
    """Test file structure and organization."""
    
    def test_interfaces_file_exists(self):
        """Test interfaces.py exists."""
        interfaces_path = Path(__file__).parent / 'python-core' / 'interfaces.py'
        self.assertTrue(interfaces_path.exists())
    
    def test_adapter_file_exists(self):
        """Test adapter.py exists."""
        adapter_path = Path(__file__).parent / 'python-core' / 'graphics' / 'adapter.py'
        self.assertTrue(adapter_path.exists())
    
    def test_pygame_renderer_exists(self):
        """Test pygame_renderer.py exists."""
        renderer_path = Path(__file__).parent / 'python-core' / 'graphics' / 'pygame_renderer.py'
        self.assertTrue(renderer_path.exists())
    
    def test_retro16_renderer_exists(self):
        """Test snes_pygame_renderer.py exists (Retro16 renderer)."""
        renderer_path = Path(__file__).parent / 'python-core' / 'graphics' / 'snes_pygame_renderer.py'
        self.assertTrue(renderer_path.exists())
    
    def test_config_file_exists(self):
        """Test config.py exists."""
        config_path = Path(__file__).parent / 'python-core' / 'config.py'
        self.assertTrue(config_path.exists())
    
    def test_utils_file_exists(self):
        """Test utils.py exists."""
        utils_path = Path(__file__).parent / 'python-core' / 'utils.py'
        self.assertTrue(utils_path.exists())


def run_tests(verbose=True):
    """Run all tests.
    
    Args:
        verbose: Print detailed output
        
    Returns:
        True if all tests passed, False otherwise
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestInterfaces))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphicsAdapter))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestFileStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    """Main test entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="COIN-OPERATED JRPG Graphics Tests")
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal output')
    parser.add_argument('--pattern', '-p', help='Run tests matching pattern')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("COIN-OPERATED JRPG Graphics System Test Suite".center(60))
    print("=" * 60)
    print()
    
    if args.pattern:
        # Run specific tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(args.pattern)
        runner = unittest.TextTestRunner(verbosity=1 if args.quiet else 2)
        result = runner.run(suite)
    else:
        # Run all tests
        success = run_tests(verbose=not args.quiet)
        result = Mock()
        result.wasSuccessful = lambda: success
    
    print()
    print("=" * 60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED".center(60))
        print("=" * 60)
        return 0
    else:
        print("❌ SOME TESTS FAILED".center(60))
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
