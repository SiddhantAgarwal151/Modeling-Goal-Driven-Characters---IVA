import openai

def generate_response(prompt):
    """Generates a response using GPT based on the given prompt."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a simulation engine for interactive storytelling."},
                  {"role": "user", "content": prompt}]
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
