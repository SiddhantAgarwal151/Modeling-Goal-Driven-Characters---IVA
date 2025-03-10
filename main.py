import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    """Generates a response using GPT based on the given prompt."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Changed from "gpt-4" to "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a simulation engine for interactive storytelling."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Character beliefs and emotional states
characters = {
    "Sid": {"state": "Calm", "beliefs": {"malfunction": 0.8, "hiding": 0.0}},
    "Captain Raymond": {"state": "Suspicious", "beliefs": {"Sid hiding": 0.5}},
    "Dr. Bao": {"state": "Neutral", "beliefs": {"Sid trust": 0.7}}
}

# Events and character responses
story_events = [
    "Sid discovers a broken airlock panel but hides it.",
    "Raymond observes Sid acting strangely.",
    "Raymond confronts Sid.",
    "A sudden alarm forces cooperation."
]

for event in story_events:
    prompt = f"The current scenario: {event}\n\n" \
            f"Sid's beliefs: {characters['Sid']['beliefs']}\n" \
            f"Captain Raymond's beliefs: {characters['Captain Raymond']['beliefs']}\n" \
            f"Dr. Bao's beliefs: {characters['Dr. Bao']['beliefs']}\n" \
            "What happens next based on their beliefs and emotions?"
    result = generate_response(prompt)
    print(f"Event: {event}\nResponse: {result}\n")

# Example use
prompt = "You are Captain Raymond. You suspect Sid is hiding something. How do you confront him?"
response = generate_response(prompt)
print(response)