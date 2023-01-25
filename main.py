from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os


data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

data_manager.update_codes()

for entry in data_manager.sheet_data.get("prices"):
    flight_data = flight_search.get_flight_cost(fly_to=entry.get("iataCode"))
    if flight_data.price < entry.get("lowestPrice"):
        price_alert = f"Low price alert! Only $%.2f to fly from {flight_data.origin_city}-" \
                      f"{flight_data.origin_airport} " \
                      f"to {flight_data.destination_city}-{flight_data.destination_airport}, " \
                      f"from {flight_data.out_date}" \
                      f" to {flight_data.return_date}" % flight_data.price
        notification_manager.create_message(user_message=price_alert)
        notification_manager.send_alert()
        sheet_input = {
            "price": {
                "lowestPrice": flight_data.price
            }
        }
        print(sheet_input)
        data_manager.edit_row(row=f"{entry['id']}", json=sheet_input)
