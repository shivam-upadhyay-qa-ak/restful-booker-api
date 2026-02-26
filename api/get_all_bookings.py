import requests
from config.config import BASE_URL, HEADERS


def get_all_bookings():
    """GET - Retrieve all bookings."""
    url = f"{BASE_URL}/booking"
    response = requests.get(url, headers=HEADERS, timeout=30)

    print("=" * 60)
    print("2. GET - Get All Bookings")
    print("=" * 60)
    print(f"URL:         {url}")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total:       {len(data)} bookings")
    print(f"Response (first 5): {data[:5]}")
    print()

    return data
