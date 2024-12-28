# tests/test_pipeline.py
import pytest
from trip_crawler.pipelines import PostgreSQLPipeline
from trip_crawler.database.base import DatabaseManager
from trip_crawler.database.models import Hotel

def test_process_item(session, mock_hotel_data, mocker):
    """Test pipeline item processing"""
    pipeline = PostgreSQLPipeline('test_connection_string')
    pipeline.db_manager = DatabaseManager()
    pipeline.db_manager.Session = lambda: session

    # Mock the spider argument
    spider_mock = mocker.Mock()

    # Process the item
    processed_item = pipeline.process_item(mock_hotel_data, spider_mock)

    # Check the item was added to the database
    hotels = session.query(Hotel).all()
    assert len(hotels) == 1
    hotel = hotels[0]

    assert hotel.property_title == 'White Palace Hotel'
    assert hotel.city_name == 'Dhaka'
