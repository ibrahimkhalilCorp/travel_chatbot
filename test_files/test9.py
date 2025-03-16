from agents.confirm_booking_agent import confirm_booking_agent
import json
payload = confirm_booking_agent()
print(json.dumps(payload, indent=4))
