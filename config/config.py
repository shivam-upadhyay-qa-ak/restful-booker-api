BASE_URL = "https://restful-booker.herokuapp.com"

HEADERS = {
    "Content-Type": "application/json"
}

BOOKING_PAYLOAD = {
    "firstname": "dearpostman1",
    "lastname": "dearTapali1",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"
}
