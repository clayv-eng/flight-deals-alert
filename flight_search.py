import requests
import datetime as dt
from flight_data import FlightData
import os

FLIGHT_API_KEY = os.environ.get("FLIGHT_API_KEY")
FLIGHT_ENDPOINT = os.environ.get("FLIGHT_ENDPOINT")
TODAY = dt.datetime.today().date()
SIX_MONTHS = TODAY + dt.timedelta(days=186)


class FlightSearch:
    def __init__(self, key: str = FLIGHT_API_KEY):
        self.endpoint = FLIGHT_ENDPOINT
        self.header = {"apikey": key}

    def get_iata_code(self, city: str):
        parameters = {"term": city}
        response = requests.get(url=f"{self.endpoint}locations/query", params=parameters, headers=self.header)
        response.raise_for_status()
        result = response.json()
        return result['locations'][0].get("code")

    def get_flight_cost(self,
                        fly_to: str,
                        fly_from: str = "YTO",
                        date_from: str = f"{TODAY.strftime('%d/%m/%Y')}",
                        date_to: str = f"{SIX_MONTHS.strftime('%d/%m/%Y')}",
                        nights_in_dst_from: str = "7",
                        nights_in_dst_to: str = "28",
                        curr: str = "CAD"
                        ):
        parameters = {
            "fly_to": fly_to,
            "fly_from": fly_from,
            "dateFrom": date_from,
            "dateTo": date_to,
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "one_for_city": 1,
            "curr": curr
        }
        response = requests.get(url=f"{self.endpoint}v2/search", params=parameters, headers=self.header)
        response.raise_for_status()
        # print(response.json())
        try:
            data = response.json()["data"][0]
            lowest_price = float(data.get("price"))
        except IndexError:
            print(f"No flights found for {fly_to}.")
            return None

        flight_data = FlightData(price=lowest_price,
                                 origin_city=data.get("route")[0]["cityFrom"],
                                 origin_airport= data.get("route")[0]["flyFrom"],
                                 destination_city=data.get("route")[0]["cityTo"],
                                 destination_airport=data.get("route")[0]["flyTo"],
                                 out_date=data.get("route")[0]["local_departure"].split("T")[0],
                                 return_date=data.get("route")[1]["local_departure"].split("T")[0]
                                 )
        print(f"{flight_data.destination_city}: ${flight_data.price} CAD")
        return flight_data

# This class is responsible for talking to the Flight Search API.
