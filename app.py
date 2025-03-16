import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, session
from tools.clear_json_file import clear_json_files
from memory.json_memory import store_in_vector_db  # Import FAISS storage function

app = Flask(__name__, template_folder="templates")
app.secret_key = "your_secret_key"  # Required for session management

user_sessions = {}

# ✅ Define Paths for Logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Moves one level up
LOGS_DIR = os.path.join(BASE_DIR, "logs")  # Store logs inside "logs" directory
LOG_FILE = os.path.join(LOGS_DIR, "chatbot.log")  # Full path to chatbot log file

# ✅ Ensure 'logs' directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# ✅ Set up Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@app.route("/")
def home():
    session["user_id"] = session.get("user_id", os.urandom(16).hex())  # Assign a user_id if not present
    return render_template("index.html")  # Loads chat UI

@app.route("/init", methods=["GET"])
def init_chat():
    clear_json_files()
    """Send initial welcome message when chat loads."""
    welcome_msg = "### Hello and welcome to Akij Air! 🌟"
    print("Sending Welcome Message:", welcome_msg)  # Debugging
    return jsonify({"response": welcome_msg})


@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot requests."""
    from agents.agent_selector import select_agent  # Import inside function to prevent circular dependency

    user_id = session.get("user_id")  # Retrieve user_id from session
    user_input = request.json.get("message")

    chatbot_response = select_agent(user_input, user_id)  # Pass user input to chatbot

    if isinstance(chatbot_response, dict):
        response_text = chatbot_response.get("response", "Sorry, I couldn't process that.")
    else:
        response_text = str(chatbot_response)

    return jsonify({"response": response_text})


def log_conversation(user_id, user_message, bot_response):
    """
    Logs each user-bot conversation turn and stores it in the vector database.
    """
    log_entry = f"[{user_id}] User: {user_message}\n[{user_id}] Bot: {bot_response}\n"
    logging.info(log_entry)

    # ✅ Store in FAISS
    store_in_vector_db(user_id, user_message, bot_response)

if __name__ == "__main__":
    print("### Hello and welcome to Akij Air! 🌟")  # Show in terminal
    app.run(host="0.0.0.0", port=80, debug=True)




