import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Initialize the OpenAI client

def _analyze_gender(name):
    prompt = f"""
    You are an expert in name-based gender identification.

    - Determine the gender of the given name: '{name}'.
    - If the name is commonly associated with males, return `"male"`.
    - If the name is commonly associated with females, return `"female"`.
    - If the name is gender-neutral or ambiguous, **still choose either "male" or "female"** based on the closest match.
    - **Never return "unknown".**
    - **Strictly return only JSON, no explanations.**

    **Output must be a strict JSON object:**  
    Example:
    {{"gender": "male"}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You analyze names and return gender as structured JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.5,
            response_format={"type": "json_object"},  # ✅ Fixed: Changed "json" to "json_object"
        )

        response_data = response.choices[0].message.content  # Since response_format is JSON, it's already a dict
        response_data = json.loads(response_data)
        return response_data.get("gender", "male")  # Default fallback is "male" if anything goes wrong

    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "male"  # Fallback for API errors

# Example usage:
print(_analyze_gender("Ibrahim"))
