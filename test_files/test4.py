# import re
#
#
# passenger_details = {}
# value = 'ibrahim@ibos.io'
# if "@" in value:  # Email detection
#     passenger_details["email"] = re.search(r'[\w\.-]+@[\w\.-]+', value).group()
#
# value = '01515619886'
# if re.search(r'\b\d{11}\b', value):  # Phone number detection
#     passenger_details["contact_number"] = re.search(r'\b\d{11}\b', value).group()
#
# value = 'A123456'
# if re.search(r'[A-Z]\d{5,}', value):  # Passport detection
#     passenger_details["passport_number"] = re.search(r'[A-Z]\d{5,}', value).group()
#
# print(passenger_details)



#********************************************************************************************************************************************


# required_flight_fields = ["origin", "destination", "date_of_travel", "journey_type", "num_adults", "num_children", "flight_type"]
#
# pending_flight_data = {'date_of_travel': '2025-02-27', 'destination': 'Sylhet', 'flight_type': 'Economy', 'journey_type': 'OneWay', 'num_adults': 1, 'num_children': 0, 'origin': 'Dhaka'}
#
# missing_fields = [field for field in required_flight_fields if
#                           field not in pending_flight_data or not pending_flight_data[field]]
#
# print(missing_fields)
#
# missing_fields = [field for field in required_flight_fields if
#                   (field not in pending_flight_data) or (pending_flight_data[field] in [None, "", [], {}])]
#
# print(missing_fields)

#******************************************************************************************************************

pending_passenger_data = {'name': 'My name is Ibrahim khalil ibrahim@ibos.io 01515619886 A12345'}

required_passenger_fields = ["title", "gender", "first_name", "last_name", "email", "contact_number", "dob", "passport_number"]
missing_fields = [field for field in required_passenger_fields if (field not in pending_passenger_data)  or (pending_passenger_data[field] in [None, "", [], {}])]

print(missing_fields)