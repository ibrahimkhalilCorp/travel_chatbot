# from tools.location_extractor import extract_location, extract_date
#
# user_input = "I want to go Sylhet from Dhaka on Feb 27, it's a one-way trip only for me."
#
# origin = extract_location(user_input, keyword="from")
# destination = extract_location(user_input, keyword="to")
# travel_date = extract_date(user_input)
#
# print(f"Origin: {origin}, Destination: {destination}, Date: {travel_date}")

import re

def check_info(text):
    # Improved regex with better handling of titles and names
    name_match = re.search(r"(?:my name is\s+)?\b(Mr|Ms|Mrs|Dr)?\b\s*([A-Z][a-z]+)[,\s]+([A-Z][a-z]+)(?:\s+(Mr|Ms|Mrs|Dr))?",text,re.IGNORECASE)

    if name_match:
        # Correct title detection (before or after)
        title = name_match.group(1) or name_match.group(4)  # Handles both title positions
        first_name = name_match.group(2).strip()
        last_name = name_match.group(3).strip()

        print(f"{title or 'None'} | {first_name} | {last_name}")

# Test Cases
inputs = [
    "My name is Mr Ibrahim Khalil ibrahim@ibos.com 01515619886 A12345 1990-01-01 male",
    "My name is Mrs Turin Tasmira  1994-01-01",
    "Mrs Ayesha Ibrat Female",
    "Mrs Aaiza, Ibrat",
    "Aaiza, Ibrat Mrs",  # Title at the end
]

for user_input in inputs:
    check_info(user_input)


