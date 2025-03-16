import time
from tools.clear_json_file import clear_json_files
clear_json_files()

from agents.agent_selector import select_agent

user_id = str(123456)

def process_user_inputs(inputs):
    """
    Process a list of user inputs, detect their intent, and print results.
    Wait for API responses to ensure correct processing.
    """

    for user_input in inputs:
        print(f"\nUser Input: {user_input}")
        intent = select_agent(user_input, user_id)
        print(f"🔍 Detected Intent: {intent}\n")
        # ✅ Wait for 2 seconds before the next request to allow API processing
        time.sleep(20)

inputs = [
    "I want to go sylhet from dhaka",
    "Can you tell me your name?",
    "Please tell me a joke",
    "What kind of place is Sylhet",
    "on april 19, only for me and one way trip",
    "What is the cheapest flight?",
    "I want to book this flight",
    "My name is Ibrahim khalil ibrahim@ibos.com 01515619886 A12345 1990-01-01",
    "Please proceed with the booking.",
    "Can you give me a trip plan to visit this place"
]

# ✅ Run the test
process_user_inputs(inputs)
