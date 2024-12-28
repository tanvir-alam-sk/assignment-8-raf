# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_crawler.database.base import Base
from trip_crawler.database.models import Hotel
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

@pytest.fixture(scope='session')
def connection_string():
    """Fixture for test database connection string
    
    If you use postgres(not docker), than you should creat database

    "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres
    CREATE DATABASE test_db;

    DB_USERNAME='postgres'
    DB_PASSWORD='postgres'
    DB_NAME='test_db'
    DB_PORT='5432'
    DB_HOST='localhost'
    """
    # return f'postgresql+psycopg2://postgres:postgres@localhost:5432/test_db'
    return f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

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
        'city_name': 'Dhaka',
        'property_title': 'White Palace Hotel',
        'hotel_id': 45570507,
        'price': 36,
        'rating': "4.2",
        'address': "Near Hazrat Shahjalal International Airport",
        'latitude': 23.879744,
        'longitude': 90.39683,
        'room_type': "Super Deluxe Twin Room",
        'image': "https://ak-d.tripcdn.com/images/0581612000d3euoz5C29D_R_250_250_R5_D.jpg",
        'local_image_path': "hotel_images/dhaka/45570507_White_Palace_Hotel.jpg"
    }