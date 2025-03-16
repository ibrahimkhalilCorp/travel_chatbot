# from langchain.schema import HumanMessage
#
# def handle_missing_fields(missing_fields):
#     if missing_fields:
#         # Format the message for missing fields
#         message = f"✈️ Almost done! Please provide: {', '.join(missing_fields)}."
#
#         # Wrap the message in a HumanMessage object
#         return HumanMessage(content=message)
#     else:
#         return "All data is complete!"
#
# # Example with some missing fields
# missing_fields = ["booking_id", "departure_time", "destination"]
#
# response = handle_missing_fields(missing_fields)
# print(response)


origin = "dhaka"
destination = "sylhet"

domestic_airports = {
    "Dhaka": {"Shahjalal International Airport": "DAC"},
    "Chittagong": {"Shah Amanat International Airport": "CGP"},
    "Sylhet": {"Osmani International Airport": "ZYL"},
    "Cox's Bazar": {"Cox's Bazar Airport": "CXB"},
    "Jessore": {"Jessore Airport": "JSR"},
    "Barishal": {"Barisal Airport": "BZL"},
    "Rajshahi": {"Shah Makhdum Airport": "RJH"},
    "Saidpur": {"Saidpur Airport": "SPD"},
}

# ✅ Check if origin & destination are in the domestic airports list
is_origin_domestic = any(origin.lower() in city.lower() for city in domestic_airports.keys())
is_destination_domestic = any(destination.lower() in city.lower() for city in domestic_airports.keys())

# ✅ Determine flight type
flight_type = "domestic" if is_origin_domestic and is_destination_domestic else "international"

print(f"🛫 Flight Type: {flight_type}")
