import re
import os
import requests
from typing import Optional, Tuple
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.tools import StructuredTool
from langchain.memory import ConversationBufferMemory
from memory.json_memory import JSONMemory
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from tools.utils import get_current_time
from tools.detect_intent import detect_intent
from agents.flight_search_agent import extract_flight_details
from agents.flight_selection_agent import flight_selection_agent
from agents.flight_query_agent import flight_query_agent
from agents.confirm_booking_agent import confirm_booking_agent
from agents.passenger_details_agent import collect_passenger_details, extract_passenger_details
from agents.smart_assistant_agent import smart_assistant_agent
from dotenv import load_dotenv


# ✅ Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Initialize GPT-4o Model
llm = ChatOpenAI(model="gpt-4o")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves one level up
DATA_DIR = os.path.join(BASE_DIR, "data")  # Set the data folder inside the project

# Ensure the 'data' folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# ✅ Memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
passenger_memory = JSONMemory(os.path.join(DATA_DIR, "passenger_data.json"))
flight_memory = JSONMemory(os.path.join(DATA_DIR, "flight_search_data.json"))

# ✅ Define Schemas for Structured Tools
class TimeInputSchema(BaseModel):
    pass  # No input required for time retrieval

class FlightSearchInputSchema(BaseModel):
    origin: str
    destination: str
    date_of_travel: str
    journey_type: str
    num_adults: int
    num_children: int
    flight_type: str

class PassengerDetailsInputSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    passport_number: str

class PassengerDetailsAgent:
    def __init__(self):
        self.ocr_data = None
        self.nid_ocr_data = None

    def process_passport_ocr(self, passport_file: Tuple[str, bytes, str]):
        """
        Process the passport OCR and extract details.
        """
        try:
            file_name, file_content, content_type = passport_file  # Extract file details

            # ✅ Send the correct file format for OCR API
            response = requests.post(
                "https://ocr.ibos.io/passport_ocr",
                files={"file": (file_name, file_content, content_type)}
            )

            if response.status_code == 200:
                self.ocr_data = response.json()
                return self._auto_fill_passenger_data()
            else:
                return "❌ There was an issue processing the passport. Please enter details manually."

        except Exception as e:
            return f"⚠️ Error processing passport: {e}"

    def process_nid_ocr(self, nid_file: Tuple[str, bytes, str]):
        """
        Process the NID OCR and extract details.
        """
        try:
            file_name, file_content, content_type = nid_file  # Extract file details

            # ✅ Send the correct file format for OCR API
            response = requests.post(
                "https://ocr.ibos.io/nid_ocr",
                files={"file": (file_name, file_content, content_type)}
            )

            if response.status_code == 200:
                self.nid_ocr_data = response.json()
                return self._auto_fill_passenger_nid_data()
            else:
                return "❌ There was an issue processing the NID. Please enter details manually."

        except Exception as e:
            return f"⚠️ Error processing NID: {e}"

    def _auto_fill_passenger_data(self):
        """
        Auto-fill passenger data from OCR-extracted passport details.
        """
        if not self.ocr_data:
            return "❌ No OCR data available."

        # Example: Extract fields from OCR data
        first_name = self.ocr_data.get("first_name")
        last_name = self.ocr_data.get("last_name")
        passport_number = self.ocr_data.get("passport_number")

        # ✅ Call Passenger Details Agent to save the extracted data
        return collect_passenger_details(
            passenger_index=0,  # Replace with the correct passenger index
            first_name=first_name,
            last_name=last_name,
            passport_number=passport_number
        )

    def _auto_fill_passenger_nid_data(self):
        """
        Auto-fill passenger data from OCR-extracted NID details.
        """
        if not self.nid_ocr_data:
            return "❌ No OCR data available."

        # Example: Extract fields from OCR data
        first_name = self.nid_ocr_data.get("first_name")
        last_name = self.nid_ocr_data.get("last_name")
        nid_number = self.nid_ocr_data.get("nid_number")

        # ✅ Call Passenger Details Agent to save the extracted data
        return collect_passenger_details(
            passenger_index=0,  # Replace with the correct passenger index
            first_name=first_name,
            last_name=last_name,
            passport_number=nid_number  # Use NID number as a placeholder
        )

    def _prompt_missing_fields(self):
        """
        Prompt the user for missing fields after auto-filling.
        """
        # ✅ Identify missing fields and prompt the user
        missing_fields = self._get_missing_fields()
        if missing_fields:
            return f"📝 Almost done! Please provide: {', '.join(missing_fields)}."
        return "🛂 Passenger details saved successfully."

    def _get_missing_fields(self):
        """
        Identify missing fields in the passenger data.
        """
        # ✅ Check which fields are missing
        required_fields = ["first_name", "last_name", "email", "phone", "passport_number"]
        passenger_data = passenger_memory.load_data().get("passengers", [])[0]  # Replace with the correct passenger index
        return [field for field in required_fields if not passenger_data.get(field)]

# ✅ Define Structured Tools
tools = [
    StructuredTool(
        name="Time",
        func=get_current_time,
        description="Provides the current time.",
        args_schema=TimeInputSchema
    ),
    StructuredTool(
        name="FlightSearch",
        func=extract_flight_details,
        description="Collects flight search details dynamically.",
        args_schema=FlightSearchInputSchema
    ),
    StructuredTool(
        name="PassengerDetails",
        func=collect_passenger_details,
        description="Collects passenger details dynamically.",
        args_schema=PassengerDetailsInputSchema
    )
]

# ✅ Load structured chat prompt
try:
    prompt = hub.pull("hwchase17/structured-chat-agent")
except:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly AI assistant."),
        ("user", "{input}")
    ])

# ✅ Create Agents
greet_agent = create_structured_chat_agent(llm=llm, tools=[], prompt=prompt)
flight_search_agent = create_structured_chat_agent(llm=llm, tools=[tools[1]], prompt=prompt)
passenger_details_agent = create_structured_chat_agent(llm=llm, tools=[tools[2]], prompt=prompt)

def select_agent(user_input, user_id, file_upload=None):
    from app import log_conversation
    """
    Dynamically selects the appropriate agent based on LLM intent classification.
    """
    # Step 1: Detect Intent
    intent = detect_intent(user_input)

    if intent == "greeting":
        response = "👋 Hello! How can I assist you today?"

    elif intent == "flight_booking":
        response = extract_flight_details(user_input)


    elif intent == "providing_date":
        response = extract_flight_details(user_input)

    elif intent == "providing_location":
        response = extract_flight_details(user_input)

    elif intent == "passenger_details":
        # ✅ Load flight search data to determine number of passengers and flight type
        flight_details = flight_memory.load_data() or {}
        num_adults = flight_details.get("num_adults", 1)
        num_children = flight_details.get("num_children", 0)
        total_passengers = num_adults + num_children
        flight_type = flight_details.get("flight_type", "domestic")  # Default to domestic if not specified
        # ✅ Load existing passenger data
        passenger_details = passenger_memory.load_data() or {"passengers": []}
        # ✅ Define required fields based on flight type
        if flight_type == "domestic":
            required_fields = ["title", "gender", "first_name", "last_name", "email", "phone", "dob"]
        else:
            required_fields = ["title", "gender", "first_name", "last_name", "email", "phone", "dob", "passport_number",
                               "nationality", "date_of_issue", "date_of_expiry"]
        # ✅ Find the next passenger with missing details
        passenger_index = 0
        for i, passenger in enumerate(passenger_details.get("passengers", [])):
            if not all(passenger.get(field) for field in required_fields):
                passenger_index = i
                break
        else:
            if len(passenger_details.get("passengers", [])) >= total_passengers:
                response = "✅ All passengers' details have already been collected."
            passenger_index = len(passenger_details.get("passengers", []))
        # ✅ Extract Passenger Data
        extracted_data = extract_passenger_details(user_input)
        # ✅ Call Passenger Details Agent with flight type
        response = collect_passenger_details(
            passenger_index=passenger_index,
            flight_type=flight_type,
            **extracted_data  # Pass all extracted fields as keyword arguments
        )

    elif intent == "flight_query":
        response = flight_query_agent(user_input)

    elif intent == "flight_selection":
        response = flight_selection_agent(user_input)

    elif intent == "confirm_booking" or intent == "booking_confirmation":
        print("🚀 Calling confirm_booking_agent...")
        response = confirm_booking_agent()

    elif intent == "other":
        response = smart_assistant_agent(user_input, user_id)

    else:
        response = "🤔 I'm not sure how to handle that. You can ask about flights, passenger details, or check the time."

    # ✅ Log the conversation
    log_conversation(user_id, user_input, response)

    return response