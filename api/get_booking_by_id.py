import requests
from config.config import BASE_URL, HEADERS


def get_booking_by_id(booking_id):
    """GET - Retrieve a specific booking by ID."""
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.get(url, headers=HEADERS, timeout=30)

    print("=" * 60)
    print(f"3. GET - Get Booking By ID ({booking_id})")
    print("=" * 60)
    print(f"URL:         {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:    {response.json()}")
    print()

    return response.json()
