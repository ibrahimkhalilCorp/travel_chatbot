from agents.flight_query_agent import flight_query_agent


def process_user_inputs(inputs):
    """
    Process a list of user inputs, detect their intent, and print results.
    Wait for API responses to ensure correct processing.
    """
    for user_input in inputs:
        print(f"\nUser Input: {user_input}")
        intent = flight_query_agent(user_input)
        print(f"🔍 Detected Intent: {intent}\n")


# ✅ Sample user inputs
inputs = [
        "What is the cheapest flight to Dubai?",
        "Are there any flights available from New York to London tomorrow?",
        "How long is the flight from Paris to Tokyo?",
        "Which airlines operate flights from Los Angeles to Sydney?",
        "Can you check flight prices for next weekend?",
        "I need a list of flights departing from Berlin on Friday.",
        "Are there direct flights from Toronto to Madrid?",
        "What’s the best time to book a flight to Singapore?",
        "How much does a business-class ticket to Rome cost?",
        "Do you have flight options for a round trip to Bangkok?",
        "I want to see flights with baggage included.",
        "What airlines have flights from Dhaka to Dubai?",
        "Can you check the available flights for the next week?",
        "Tell me the flight duration from London to New York."
]

# ✅ Run the test
process_user_inputs(inputs)