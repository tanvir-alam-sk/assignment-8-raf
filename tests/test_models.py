# tests/test_models.py
from trip_crawler.database.models import Hotel

def test_hotel_model_creation(session, mock_hotel_data):
    """Test Hotel model creation and repr method"""
    # Create and add hotel object
    hotel = Hotel(**mock_hotel_data)
    session.add(hotel)
    session.commit()
    
    # Retrieve and verify
    retrieved_hotel = session.query(Hotel).filter_by(hotel_id="45570507").first()
    assert retrieved_hotel is not None
    assert repr(retrieved_hotel) == "<Hotel(name=White Palace Hotel, city=Dhaka)>"
