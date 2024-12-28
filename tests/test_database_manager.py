# tests/test_database_manager.py
from trip_crawler.database.base import DatabaseManager

def test_database_manager_singleton(connection_string):
    """Test DatabaseManager is a singleton"""
    manager1 = DatabaseManager()
    manager1.initialize(connection_string)
    
    manager2 = DatabaseManager()
    
    assert manager1 is manager2

def test_database_manager_session_creation(connection_string):
    """Test database session creation"""
    manager = DatabaseManager()
    manager.initialize(connection_string)
    
    session = manager.get_session()
    assert session is not None
    session.close()