import json
import os
import openai
import requests
from tabulate import tabulate
from memory.json_memory import JSONMemory
from dotenv import load_dotenv
import json
# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves one level up
DATA_DIR = os.path.join(BASE_DIR, "data")

FLIGHT_API_URL = os.getenv("FLIGHT_API_URL")  # API to fetch flights
flight_memory = JSONMemory(os.path.join(DATA_DIR, "flight_search_data.json"))
flight_list_file = os.path.join(DATA_DIR, "flight_list.json")
passenger_memory = JSONMemory(os.path.join(DATA_DIR, "passenger_data.json"))
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "apikey": os.getenv("API_KEY"),
    "secretecode": os.getenv("SECRET_CODE")
}
airlines_dict = {
            "AA": "American Airlines",
            "AF": "Air France",
            "AI": "Air India",
            "AK": "AirAsia",
            "BA": "British Airways",
            "BG": "Biman Bangladesh Airlines",
            "BR": "EVA Air",
            "BS": "US-Bangla Airlines",
            "CA": "Air China",
            "CX": "Cathay Pacific",
            "DL": "Delta Air Lines",
            "EK": "Emirates",
            "ET": "Ethiopian Airlines",
            "EY": "Etihad Airways",
            "FR": "Ryanair",
            "IB": "Iberia",
            "JL": "Japan Airlines",
            "KE": "Korean Air",
            "KLM": "KLM Royal Dutch Airlines",
            "LH": "Lufthansa",
            "MH": "Malaysia Airlines",
            "QF": "Qantas",
            "QR": "Qatar Airways",
            "SQ": "Singapore Airlines",
            "TK": "Turkish Airlines",
            "UA": "United Airlines",
            "VS": "Virgin Atlantic",
            "WN": "Southwest Airlines"
        }

# Flight Search API Agent
def flight_search_api_agent():
    flight_details = flight_memory.load_data() or {}
    if not flight_details.get("origin") or not flight_details.get("destination"):
        return "❌ Missing flight details. Please provide origin and destination."

    payload = create_payload(flight_details)
    payload = payload.replace("None", "null")
    search_payload = json.loads(payload)
    response = requests.post("https://serviceapi.innotraveltech.com/flight/search",json=search_payload, headers=headers)
    if response.status_code == 200:
        flights = response.json()

        if "data" not in flights or not flights["data"]:
            print("❌ API response does not contain valid flight data!")
            return "❌ No flights available. Please try again later."

        with open(flight_list_file, "w") as f:
            json.dump(flights, f, indent=4)

        print("✅ Flight list successfully saved!")
        flight_list = _format_results(flights)
        return flight_list
    else:
        print(f"❌ Flight API Error: {response.status_code}, Response: {response.text}")
        return f"❌ Flight search failed. Error: {response.status_code}"

def _format_results(response_data):
    if "data" in response_data:
        data = response_data["data"]
        tracking_id = data[0].get("tracking_id", None)
        filtered_data = [
            {
                "tracking_id": tracking_id,
                "price": entry.get("filter", {}).get("price", "N/A"),
                "carrier_operating": entry.get("filter", {}).get("carrier_operating", "N/A"),
                "cabin_class": entry.get("filter", {}).get("cabin_class", "N/A"),
                "departure_departure_time": entry.get("filter", {}).get("departure_departure_time", "N/A"),
                "arrival_departure_time": entry.get("filter", {}).get("arrival_departure_time", "N/A"),
                "connecting_airport": entry.get("filter", {}).get("connecting_airport", "None"),
                "id": entry.get("filter", {}).get("id", "N/A"),
            }
            for entry in data
        ]

        flight_list = clean_data(filtered_data)
        table = tabulate(flight_list, headers="keys", tablefmt="grid")
        # Prepare OpenAI request
        user_request = f"""
                    Format the following flight details in a **clean, well-structured, and user-friendly way**.
                    Ensure **ALL flights are displayed**, without omitting any data.
                    Use **proper spacing, indentation, and emojis/icons** for readability.

                    For each flight, include:

                    ✈ **Flight Date**  
                    💰 **Price (BDT)**  
                    🏢 **Airline** (Full Name)  
                    🎟 **Cabin Class**  
                    🕒 **Departure Time** (Local Time)  
                    🛬 **Arrival Time** (Local Time)  
                    🔗 **Connecting Airports** (Mention 'None' if there are no layovers)

                    ### Formatting Requirements:
                    - **DO NOT OMIT ANY FLIGHTS.** Display all available options.
                    - Each flight should be **separated by a blank line** for better readability.
                    - Each flight should be **clearly numbered** (1️⃣, 2️⃣, 3️⃣, etc.).
                    - Use **bullet points and spacing** to avoid clutter.
                    - The summary should be **well-structured and easy to read**.
                    - **Avoid tables, Markdown, or HTML formatting** (keep it text-based).

                    At the end, provide a **summary** in this format:

                    📌 **Summary:**  
                    💰 **Lowest Price:** (BDT Amount)  
                    ✈️ **Airline with Lowest Price:** (Airline Name)  

                    ---

                    ✅ **Selection Prompt:**  
                    At the end, ask the user to **select a flight** by providing an example.  
                    Use the following final message:

                    **"Please select a flight from the available options. For example: US-Bangla Airlines Departure Time: 16:30."**

                    Ensure the response is **properly formatted, well-spaced, and easy to read**.
                    """
        client = openai.OpenAI()
        # Make OpenAI API call to refine the HTML
        response_ = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_request},
                {"role": "system", "content": json.dumps(flight_list)}
            ]
        )

        # Extract content
        html_content = response_.choices[0].message.content.strip()
        # html_content = html_content.replace("<html>", "").replace("</html>", "").strip()
        # print(f"Generated Tabular Data:\n{table}")
        return html_content
    return "No data found in the response."

def clean_data(flights_data):
    for flight in flights_data:
        arrival_datetime = flight['arrival_departure_time']
        departure_datetime = flight['departure_departure_time']
        flight['arrival_date'], flight['arrival_time'] = arrival_datetime.split('T')[0], arrival_datetime.split('T')[1]
        flight['departure_date'], flight['departure_time'] = departure_datetime.split('T')[0], departure_datetime.split('T')[1]
        del flight['arrival_departure_time']
        del flight['departure_departure_time']
        flight['arrival_time'] = flight['arrival_time'][:-6]
        flight['departure_time'] = flight['departure_time'][:-6]
        if flight['carrier_operating'] in airlines_dict:
            flight['carrier_operating'] = airlines_dict[flight['carrier_operating']]
    return flights_data

def create_payload(flight_details):
    payload = {
        "journey_type": flight_details.get("journey_type", "OneWay"),
        "segment": [
            {
                "departure_airport_type": "AIRPORT",
                "departure_airport": get_airport_code(flight_details["origin"]),
                # Use IATA code if available
                "arrival_airport_type": "AIRPORT",
                "arrival_airport": get_airport_code(flight_details["destination"]),
                # Use IATA code if available
                "departure_date": flight_details["date_of_travel"],
            }
        ],
        "travelers_adult": flight_details.get("num_adults", 1),
        "travelers_child": flight_details.get("num_children", 0),
        "travelers_child_age": [],  # Can be populated if ages are collected
        "travelers_infants": 0,  # Defaulted to 0, can be updated dynamically
        "travelers_infants_age": [],  # Can be populated if ages are collected
        "fare_type": None,
        "fare_option": None,
        "content_type": None,
        "ptc_option": None,
        "agency_ethnic_list": None,
        "preferred_carrier": [],
        "non_stop_flight": "any",
        "baggage_option": "any",
        "booking_class": "Economy",
        "supplier_uid": "F1TT00041",  # Replace with actual supplier UID if dynamic
        "partner_id": "78",  # Replace with actual partner ID if dynamic
        "language": "en",
        "short_ref": "12121212121",  # Replace with a dynamic reference if needed
        "version": None,
    }

    if flight_details["journey_type"] == "RoundTrip" and flight_details["return_date"]:
        payload["segment"].append({
            "departure_airport": get_airport_code(flight_details["destination"]),
            "arrival_airport": get_airport_code(flight_details["origin"]),
            "departure_date": flight_details["return_date"],
        })
    else:
        payload["team_profile"] = [
            {
                "member_id": "1",
                "pax_type": "ADT"
            },
            {
                "member_id": "2",
                "pax_type": "CNN"
            },
            {
                "member_id": "3",
                "pax_type": "INF"
            }
        ]

    # print(f"payload: {json.dumps(payload)}")
    return json.dumps(payload)

def get_airport_code(city):
    airports = {
        "Dhaka": {"Shahjalal International Airport": "DAC"},
        "Kathmandu": {"Tribhuvan International Airport": "KTM"},
        "Kolkata": {"Netaji Subhas Chandra Bose International Airport": "CCU"},
        "Chennai": {"Chennai International Airport": "MAA"},
        "Bangkok": {
            "Suvarnabhumi Airport": "BKK",
            "Don Mueang International Airport": "DMK"
        },
        "Phuket": {"Phuket International Airport": "HKT"},
        "Singapore": {"Singapore Changi Airport": "SIN"},
        "Kuala Lumpur": {"Kuala Lumpur International Airport": "KUL"},
        "Langkawi": {"Langkawi International Airport": "LGK"},
        "Dubai": {
            "Dubai International Airport": "DXB",
            "Al Maktoum International Airport": "DWC"
        },
        "London": {
            "Heathrow Airport": "LHR",
            "Gatwick Airport": "LGW",
            "London City Airport": "LCY",
            "Luton Airport": "LTN",
            "Stansted Airport": "STN"
        },
        "Manchester": {"Manchester Airport": "MAN"},
        "Tokyo (Narita)": {"Narita International Airport": "NRT"},
        "Doha": {"Hamad International Airport": "DOH"},
        "Maldives": {
            "Velana International Airport (Male)": "MLE",
            "Gan International Airport": "GAN"
        },
        "Muscat": {"Muscat International Airport": "MCT"},
        "Rome": {
            "Leonardo da Vinci–Fiumicino Airport": "FCO",
            "Ciampino–G. B. Pastine International Airport": "CIA"
        },
        "New York": {
            "John F. Kennedy International Airport": "JFK",
            "LaGuardia Airport": "LGA",
            "Newark Liberty International Airport": "EWR"
        },
        "Washington": {
            "Washington Dulles International Airport": "IAD",
            "Ronald Reagan Washington National Airport": "DCA",
            "Baltimore/Washington International Thurgood Marshall Airport": "BWI"
        },
        "Orlando, Florida": {
            "Orlando International Airport": "MCO",
            "Orlando Sanford International Airport": "SFB"
        },
        "Miami": {
            "Miami International Airport": "MIA",
            "Fort Lauderdale-Hollywood International Airport": "FLL"
        },
        "Bali": {"Ngurah Rai International Airport (Denpasar)": "DPS"},
        "Jakarta": {
            "Soekarno-Hatta International Airport": "CGK",
            "Halim Perdanakusuma International Airport": "HLP"
        },
        "Hanoi": {"Noi Bai International Airport": "HAN"},
        "Ho Chi Minh City": {"Tan Son Nhat International Airport": "SGN"},
        "Philippines": {
            "Ninoy Aquino International Airport (Manila)": "MNL",
            "Mactan-Cebu International Airport": "CEB",
            "Clark International Airport": "CRK"
        },
        "Guangzhou": {"Guangzhou Baiyun International Airport": "CAN"},
        "Kunming": {"Kunming Changshui International Airport": "KMG"},
        "Shanghai": {
            "Shanghai Pudong International Airport": "PVG",
            "Shanghai Hongqiao International Airport": "SHA"
        },
        "Chengdu": {
            "Chengdu Shuangliu International Airport": "CTU",
            "Chengdu Tianfu International Airport": "TFU"
        },
        "Hong Kong": {"Hong Kong International Airport": "HKG"},
        "Sydney": {"Sydney Kingsford Smith Airport": "SYD"},
        "Melbourne": {
            "Melbourne Airport (Tullamarine)": "MEL",
            "Avalon Airport": "AVV"
        },
        "Brisbane": {"Brisbane Airport": "BNE"},
        "Adelaide": {"Adelaide Airport": "ADL"},
        "Perth": {"Perth Airport": "PER"},
        "Wellington": {"Wellington International Airport": "WLG"},
        "Rio de Janeiro": {
            "Rio de Janeiro–Galeão International Airport": "GIG",
            "Santos Dumont Airport": "SDU"
        },
        "Buenos Aires": {
            "Ministro Pistarini International Airport (Ezeiza)": "EZE",
            "Jorge Newbery Airfield": "AEP"
        },
        "Mexico City": {"Mexico City International Airport": "MEX"},
        "Nairobi": {"Jomo Kenyatta International Airport": "NBO"},
        "Alexandria": {"Borg El Arab Airport": "HBE"},
        "Cairo": {"Cairo International Airport": "CAI"},
        "Moscow": {
            "Sheremetyevo International Airport": "SVO",
            "Domodedovo International Airport": "DME",
            "Vnukovo International Airport": "VKO"
        },
        "Tashkent": {"Tashkent International Airport": "TAS"},
        "Tbilisi": {"Tbilisi International Airport": "TBS"},
        "Ethiopia": {"Addis Ababa Bole International Airport": "ADD"},
        "Amsterdam": {"Amsterdam Airport Schiphol": "AMS"},
        "Paris": {
            "Charles de Gaulle Airport": "CDG",
            "Orly Airport": "ORY"
        },
        "Venice": {
            "Venice Marco Polo Airport": "VCE",
            "Treviso Airport": "TSF"
        },
        "Naples": {"Naples International Airport": "NAP"},
        "Barcelona": {"Barcelona–El Prat Airport": "BCN"},
        "Madrid": {"Adolfo Suárez Madrid–Barajas Airport": "MAD"},
        "Lisbon": {"Humberto Delgado Airport (Lisbon Airport)": "LIS"},
        "Malaga": {"Málaga-Costa del Sol Airport": "AGP"},
        "Toronto": {
            "Toronto Pearson International Airport": "YYZ",
            "Billy Bishop Toronto City Airport": "YTZ"
        },
        "Montreal": {"Montréal–Pierre Elliott Trudeau International Airport": "YUL"},
        "Zurich": {"Zurich Airport": "ZRH"},
        "Warsaw": {"Warsaw Chopin Airport": "WAW"},
        "Lagos": {"Murtala Muhammed International Airport": "LOS"},
        "Addis Ababa": {"Addis Ababa Bole International Airport": "ADD"},
        "Barishal": {"Barisal Airport": "BZL"},
        "Chittagong": {"Shah Amanat International Airport": "CGP"},
        "Saidpur": {"Saidpur Airport": "SPD"},
        "Rajshahi": {"Shah Makhdum Airport": "RJH"},
        "Sylhet": {"Osmani International Airport": "ZYL"},
        "Cox's Bazar": {"Cox's Bazar Airport": "CXB"},
        "Jessore": {"Jessore Airport": "JSR"}
    }
    city = city.lower()  # Convert input city name to lowercase
    for location, airports in airports.items():
        if location.lower() == city:  # Compare in lowercase
            return list(airports.values())[0]  # Return the first airport code found
    return None