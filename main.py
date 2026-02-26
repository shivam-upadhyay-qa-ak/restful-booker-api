from api.create_booking import create_booking
from api.get_all_bookings import get_all_bookings
from api.get_booking_by_id import get_booking_by_id


def main():
    print("\n*** Restful Booker API Testing ***\n")

    # 1. POST - Create a new booking
    created = create_booking()
    booking_id = created.get("bookingid")
    print(f">> Booking created with ID: {booking_id}\n")

    # 2. GET - Get all bookings
    get_all_bookings()

    # 3. GET - Get specific booking by ID
    if booking_id:
        get_booking_by_id(booking_id)


if __name__ == "__main__":
    main()
