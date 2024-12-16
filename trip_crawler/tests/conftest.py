# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_crawler.database.base import Base
from trip_crawler.database.models import Hotel

@pytest.fixture(scope='session')
def connection_string():
    """Fixture for test database connection string"""
    return 'postgresql+psycopg2://test_user:test_password@localhost:5432/test_trip_crawler'

@pytest.fixture(scope='session')
def engine(connection_string):
    """Create a SQLAlchemy engine for testing"""
    return create_engine(connection_string)

@pytest.fixture(scope='session')
def tables(engine):
    """Create tables for testing"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    """Create a new database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def mock_hotel_data():
    """Fixture with sample hotel data for testing"""
    return {
        'city_name': 'London',
        'property_title': 'Test Hotel',
        'hotel_id': 'test_hotel_123',
        'price': '100',
        'rating': '4.5',
        'address': 'Test Street 123',
        'latitude': 51.5074,
        'longitude': -0.1278,
        'room_type': 'Standard Room',
        'image': 'http://example.com/hotel.jpg',
        'local_image_path': '/path/to/hotel_image.jpg'
    }