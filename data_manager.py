import requests
from flight_search import FlightSearch
import os

SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
SHEET_HEADER = {
    "Authorization": f"Bearer {os.environ.get('SHEET_TOKEN')}"
}


class DataManager:
    def __init__(self, endpoint: str = SHEET_ENDPOINT, header: dict = SHEET_HEADER):
        self.endpoint = endpoint
        self.header = header
        self.sheet_data = self.get_all()
        self.flight_search = FlightSearch()

    def get_all(self):
        response = requests.get(url=self.endpoint, headers=self.header)
        response.raise_for_status()
        result = response.json()
        print(result)
        return result

    def get_row(self, row: str):
        response = requests.get(url=f"{self.endpoint}/{row}", headers=self.header)
        response.raise_for_status()
        result = response.json()
        return result

    def add_row(self, json: dict):
        response = requests.post(url=self.endpoint, json=json, headers=self.header)
        response.raise_for_status()
        # print(response.text)

    def edit_row(self, row: str, json: dict):
        response = requests.put(url=f"{self.endpoint}/{row}", json=json, headers=self.header)
        response.raise_for_status()
        # print(response.text)

    def update_codes(self):
        for entry in self.sheet_data.get("prices"):
            if entry.get('iataCode') == "":
                sheet_input = {
                    "price": {
                        "iataCode": self.flight_search.get_iata_code(city=f"{entry['city']}")
                    }
                }
                self.edit_row(row=f"{entry['id']}", json=sheet_input)

    # This class is responsible for talking to the Google Sheet.
