import requests
from config.config import BASE_URL, HEADERS, BOOKING_PAYLOAD


def create_booking():
    """POST - Create a new booking."""
    url = f"{BASE_URL}/booking"
    response = requests.post(url, json=BOOKING_PAYLOAD, headers=HEADERS, timeout=30)

    print("=" * 60)
    print("1. POST - Create Booking")
    print("=" * 60)
    print(f"URL:         {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:    {response.json()}")
    print()

    return response.json()
