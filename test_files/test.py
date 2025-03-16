from tools.detect_intent import detect_intent

def detect_intents_for_inputs(inputs):
    """
    Detect intents for a list of user inputs and print the results.
    """
    print("\n🔍 Detecting Intents for User Inputs...\n")
    for user_input in inputs:
        intent = detect_intent(user_input)
        print(f"🗣️ User Input: {user_input}\n🎯 Detected Intent: {intent}\n{'-' * 50}")

# Sample user inputs
user_inputs = [
    # # Greeting examples
    # 'hi there',
    # 'hello!',
    # 'Hey, how are you?',
    # 'Good morning',
    #
    # # Flight booking examples
    # 'I need to book a flight to Tokyo',
    # 'Can you help me book a ticket to London?',
    # 'I am looking for a flight to Paris next week',
    # 'I want to fly to Barcelona on March 5th',
    # 'I want to fly to Rangpur',
    # "From Sylhet on Feb 28",
    #
    # # Date providing examples
    # 'I will arrive on February 15th',
    # 'The event is scheduled for March 10',
    # 'I’m planning for April 3',
    # 'I’m available from 27th February to 5th March',
    #
    # # Location providing examples
    # 'Flying from New York to Los Angeles',
    # 'Departing from Paris to Berlin',
    # 'I’m traveling from Sydney to Auckland',
    # 'I will be flying from Toronto to Vancouver',
    # "It's a one-way trip only for me",
    #
    # # Passenger details examples
    # 'My name is Alice Johnson',
    # 'I need a ticket for John Doe',
    # 'Can you book a flight for Mary Smith?',
    # 'The passenger is Robert Taylor',
    # "My name is Turin Tasmira",
    # "Turin@akij.com 01750671424 A54321",
    #
    # # Flight query examples
    # 'What is the cheapest flight to Dubai?',
    # 'Are there any flights available from New York to London tomorrow?',
    # 'How long is the flight from Paris to Tokyo?',
    # 'Which airlines operate flights from Los Angeles to Sydney?',
    # 'Can you check flight prices for next weekend?',
    # 'Tell me more about the flight options',
    #
    # # Flight selection examples
    # 'I will take the first option.',
    # 'Book the second flight from the list.',
    # 'I want to choose the Emirates flight.',
    # 'Select the flight departing at 10 AM.',
    # 'I’ll go with the cheapest option.',
    #
    # # Booking confirmation examples
    "Yes, confirm my booking.",
    "I want to finalize my reservation.",
    "Please proceed with the booking.",
    "Confirm my flight ticket.",
    "Everything looks good, go ahead with the booking.",
    "I am ready to book now.",
    "Yes, book the selected flight.",
    "I want to complete the payment and confirm.",
    "Confirm the reservation for me.",
    "Go ahead and issue the ticket.",
    "Yes, please proceed with the final booking.",
    "All details are correct, confirm the booking.",
    "Finalize my flight ticket now.",
    "I want to complete my booking.",
    "Yes, confirm it.",
    "Go ahead with the booking.",
    "Yes, proceed with confirmation.",
    "Confirm my flight.",
    "Book it now.",
    #
    # # Other scenarios
    # 'What is the weather like in New York?',
    # 'I need assistance with my luggage',
    # 'Can you recommend a good hotel in Rome?',
]

# Process the sample user inputs
detect_intents_for_inputs(user_inputs)
