# import requests
# import json
# import os
# from dotenv import load_dotenv
#
# from agents.confirm_booking_agent import booking_tracking_id
#
# load_dotenv()
#
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "apikey": os.getenv("API_KEY"),
#     "secretecode": os.getenv("SECRET_CODE")
# }
#
# selected_flight = {
#     "flight_id": "F1TT00041-7",
#     "tracking_id": "781173995999759772ZCJX1",
#     "flight_key": "F1TT00041-7",
#     "price": 9966.44,
#     "departure_departure_time": "2025-02-27T03:20:00.000+06:00",
#     "arrival_departure_time": "2025-02-27T13:55:00.000+01:00",
#     "cabin_class": "Economy",
#     "carrier_operating": "QR",
#     "connecting_airport": [
#         "DOH"
#     ]
# }
#
# flight_key = selected_flight.get("flight_key")
# tracking_id = selected_flight.get("tracking_id")
#
# validate_url = "https://serviceapi.innotraveltech.com/flight/validate"
# validate_payload = {
#     "member_id": "2",
#     "result_type": "general",
#     "data": [
#         {
#             "tracking_id": tracking_id,
#             "flight_key": flight_key,
#             "brand_option": ""
#         }
#     ]
# }
# response = requests.post(validate_url, headers=headers, json=validate_payload)
# response.raise_for_status()
# validate_data = response.json()
# booking_tracking_id = validate_data.get("booking_tracking_id")
# print(booking_tracking_id)
# # return json.dumps(validate_data)

# selected_flight = {
#     "flight_id": "F1TT00041-7",
#     "tracking_id": "781173995999759772ZCJX1",
#     "flight_key": "F1TT00041-7",
#     "price": 9966.44,
#     "departure_departure_time": "2025-02-27T03:20:00.000+06:00",
#     "arrival_departure_time": "2025-02-27T13:55:00.000+01:00",
#     "cabin_class": "Economy",
#     "carrier_operating": "QR",
#     "connecting_airport": [
#         "DOH"
#     ]
# }
#
# selected_flight["booking_tracking_id"]= "782174002236059772VLDYX"
# print(selected_flight)


import json
import os
import openai
import requests
from memory.json_memory import JSONMemory
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# ✅ Define file paths
SELECTED_FLIGHT_FILE = "data/selected_flight.json"
PASSENGER_DATA_FILE = "data/passenger_data.json"

# ✅ Load Passenger Data
passenger_memory = JSONMemory(PASSENGER_DATA_FILE)
passenger_memory_info = passenger_memory.load_data() or {}
passenger_data = passenger_memory_info.get("passengers", [])

# ✅ Load Selected Flight Data
selected_flight = JSONMemory(SELECTED_FLIGHT_FILE)
selected_flight_info = selected_flight.load_data() or {}
booking_tracking_id = selected_flight_info.get("booking_tracking_id", "UNKNOWN_TRACKING_ID")

print(booking_tracking_id)