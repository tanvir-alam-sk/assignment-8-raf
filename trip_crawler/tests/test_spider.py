import requests
import scrapy
from scrapy.http import HtmlResponse, Request
from trip_crawler.spiders.tripCrawler import RandomCityHotelsSpider

def test_parse_method(mocker):
    """Test the initial parse method of the spider for Dhaka hotels"""
    spider = RandomCityHotelsSpider()
    
    # Mock the script data with Dhaka-specific JSON
    mock_script_data = '''
    window.IBU_HOTEL = {
        "initData": {
            "htlsData": {
                "inboundCities": [
                    {"name": "Dhaka", "id": "733", "recommendHotels": true},
                    {"name": "Rajshahi", "id": "5762", "recommendHotels": true}
                ],
                "outboundCities": [
                    {"name": "London", "id": "338", "recommendHotels": true}
                ]
            }
        }
    };
    '''
    
    # Create a mock response
    response = HtmlResponse(
        url='https://uk.trip.com/hotels/', 
        body=f'<script>{mock_script_data}</script>'.encode('utf-8'),
        encoding='utf-8'
    )
    
    # Patch random.choice to select Dhaka
    mocker.patch('random.choice', return_value={"name": "Dhaka", "id": "733", "recommendHotels": True})
    
    # Call parse method and collect requests
    requests = list(spider.parse(response))
    
    # Verify the request is generated for Dhaka
    assert len(requests) == 1
    assert requests[0].url == "https://uk.trip.com/hotels/list?city=733"
    assert requests[0].meta['city_name'] == "Dhaka"

def test_parse_city_hotels(mocker):
    """Test parsing of city hotels for Dhaka"""
    spider = RandomCityHotelsSpider()
    
    # Mock the script data with hotel list
    mock_script_data = '''
    window.IBU_HOTEL = {
        "initData": {
            "firstPageList": {
                "hotelList": [
                    {
                        "hotelBasicInfo": {
                            "hotelId": "45570507",
                            "hotelName": "White Palace Hotel",
                            "hotelImg": "https://ak-d.tripcdn.com/images/0581612000d3euoz5C29D_R_250_250_R5_D.jpg",
                            "price": "36"
                        },
                        "commentInfo": {
                            "commentScore": "4.2"
                        },
                        "positionInfo": {
                            "positionName": "Near Hazrat Shahjalal International Airport",
                            "coordinate": {
                                "lat": 23.879744,
                                "lng": 90.39683
                            }
                        },
                        "roomInfo": {
                            "physicalRoomName": "Super Deluxe Twin Room"
                        }
                    }
                ]
            }
        }
    };
    '''
    
    # Create a mock request with meta information
    mock_request = Request(
        url="https://uk.trip.com/hotels/list?city=733",
        meta={"city_name": "Dhaka"}
    )
    
    # Create a mock response with the script data
    response = HtmlResponse(
        url=mock_request.url, 
        body=f'<script>{mock_script_data}</script>'.encode('utf-8'),
        encoding='utf-8',
        request=mock_request
    )
    
    # Patch os.makedirs to prevent directory creation during test
    mocker.patch('os.makedirs')
    
    # Patch requests.get to prevent actual image download
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.content = b'fake image content'
    mock_get.return_value = mock_response
    
    # Call parse_city_hotels method and collect items
    items = list(spider.parse_city_hotels(response))
    
    # Verify the items
    assert len(items) == 1
    
    hotel_item = items[0]
    assert hotel_item['city_name'] == 'Dhaka'
    assert hotel_item['property_title'] == 'White Palace Hotel'
    assert hotel_item['hotel_id'] == '45570507'
    assert hotel_item['price'] == '36'
    assert hotel_item['rating'] == '4.2'
    assert hotel_item['address'] == 'Near Hazrat Shahjalal International Airport'
    assert hotel_item['latitude'] == 23.879744
    assert hotel_item['longitude'] == 90.39683
    assert hotel_item['room_type'] == 'Super Deluxe Twin Room'