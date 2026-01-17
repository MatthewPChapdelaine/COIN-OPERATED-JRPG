"""
COIN:OPERATED JRPG - Enemy System (Stub for Phase 3)
Enemy characters and boss battles
"""

from core.character import Character


class EnemyFactory:
    """Factory for creating enemy characters - stub implementation"""
    
    @staticmethod
    def create_drift_soldier(level: int = 1) -> Character:
        """Create Drift Empire soldier enemy - stub"""
        from core.character import create_coin
        return create_coin(level=level)  # Placeholder
    
    @staticmethod
    def create_enemy(name: str, level: int) -> Character:
        """Create generic enemy - stub"""
        from core.character import create_coin
        return create_coin(level=level)  # Placeholder
