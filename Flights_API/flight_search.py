import requests
import json

server = "https://api.tequila.kiwi.com"
API_KEY = ""
AFFIL_ID = ""
header = {
    "Content-Type": "application/json",
    "apikey": "yourapikeyvalue",

}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.departure_begin = None
        self.departure_begin_from = None
        self.departure_end = None
        self.departure_end_from = None
        self.server = server
        self.header = header
        self.affil_id = AFFIL_ID
        self.date_start = 0
        self_date_stop = 0
        self.currency = "GBP"
        self.price = 0
        self.departure_city = "LON"

    def get_city_code(self, city):
        apikey = ""
        self.header["apikey"] = apikey
        # print(self.header)
        address = f"{self.server}/locations/query"
        body = {
            "term": city,
            "location_types": "city",
        }
        response = requests.get(url=address, headers=self.header, params=body)
        # response.raise_for_status()
        response = response.json()
        return response["locations"][0]["code"]
        #
        # with open("IATA.json", "w") as file:
        #     json.dump(response, file, indent=4)

    def get_flight(self, fly_to, date_from, date_to):
        self.header["apikey"] = ""
        # print(self.header)
        address = f"{self.server}/v2/search"
        body = {
            "fly_from": self.departure_city,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
        }

        response = requests.get(url=address, headers=self.header, params=body)
        # print(response.text)
        response.raise_for_status()
        response = response.json()
        try:
            response = response["data"][0]
            self.price = response["price"]
            self.departure_begin = response["route"][0]["local_departure"].split("T")[0]
            self.departure_begin_from = response["route"][0]["flyFrom"]
            self.departure_end = response["route"][1]["local_departure"].split("T")[0]
            self.departure_end_from = response["route"][1]["flyFrom"]
        except IndexError:
            print(f"No such flight {body["fly_from"]} to {body["fly_to"]}")
            self.price = None
            self.departure_begin = None
            self.departure_begin_from = None
            self.departure_end = None
            self.departure_end_from = None

        # with open("flight_data.json", "w") as file:
        #     json.dump(response, file, indent=4)
