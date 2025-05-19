import gradio as gr
import json
import random
import re
from openai import OpenAI  # type: ignore

# Load intents
with open("intents.json", encoding="utf-8") as file:
    intents = json.load(file)

# Initialize OpenAI client


import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
 # ✅ Safe
    base_url="https://openrouter.ai/api/v1"
)

# Intent classification
def classify_intent(user_input):
    user_input = user_input.lower()
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if re.search(pattern.lower(), user_input):
                return random.choice(intent['responses'])
    return None

# Chatbot logic
def chatbot(user_input, history):
    response = classify_intent(user_input)
    if response:
        return response
    else:
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are FarmBot, a helpful assistant for farmers."},
                    {"role": "user", "content": user_input}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

# 💅 Fancy Light Green CSS
custom_css = """
/* 🌿 Overall container styling */
.gradio-container {
    background: linear-gradient(to bottom right, #f1fff0, #e8f5e9);
    font-family: 'Segoe UI', 'Poppins', sans-serif;
    padding: 3rem 2rem;
}

/* 🌾 Title styling */
h1 {
    font-size: 3rem !important;
    color: #2e7d32 !important;
    text-align: center;
    background: linear-gradient(90deg, #81c784, #c8e6c9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
    font-weight: 800;
    letter-spacing: 1px;
}

/* 🧱 Panel/card styling */
.gr-panel {
    background: #ffffff !important;
    border-radius: 1.5rem !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    padding: 2rem !important;
}

/* ✅ Primary button styling */
.gr-button-primary {
    background: linear-gradient(90deg, #4caf50, #a5d6a7) !important;
    color: white !important;
    border-radius: 1rem !important;
    padding: 0.8rem 1.6rem !important;
    font-size: 1rem;
    font-weight: bold;
    transition: all 0.3s ease;
}
.gr-button-primary:hover {
    background: linear-gradient(90deg, #66bb6a, #c8e6c9) !important;
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
}

/* ✍️ Textbox input styling */
.gr-textbox input {
    border: 2px solid #c8e6c9 !important;
    border-radius: 1rem !important;
    padding: 0.75rem 1rem;
    font-size: 1.1rem;
}
.gr-textbox input:focus {
    border-color: #4caf50 !important;
    box-shadow: 0 0 12px rgba(76, 175, 80, 0.3);
}

/* 💬 Chatbot message styling */
.gr-chatbot .message {
    padding: 1rem 1.4rem;
    border-radius: 1.2rem !important;
    margin: 0.5rem 0;
    font-size: 1.05rem;
}
.gr-chatbot .message.user {
    background: #d0f8ce !important;
    color: #1b5e20;
    align-self: flex-end;
    border-bottom-right-radius: 0.3rem !important;
}
.gr-chatbot .message.bot {
    background: #e8f5e9 !important;
    color: #2e7d32;
    align-self: flex-start;
    border-bottom-left-radius: 0.3rem !important;
}

/* 📎 Example buttons */
.gr-examples .gr-button {
    background: #f1f8e9 !important;
    color: #388e3c !important;
    border-radius: 0.75rem !important;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
}
.gr-examples .gr-button:hover {
    background: #dcedc8 !important;
    transform: translateY(-2px);
}
.gradio-container {{
    background: {bg_color}
}}



"""

from datetime import datetime

def get_season():
    month = datetime.now().month
    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "autumn"
    else:
        return "winter"

season = get_season()

if season == "summer":
    bg_color = "linear-gradient(to right, #fffde7, #fff9c4);"  # Yellowish
elif season == "winter":
    bg_color = "linear-gradient(to right, #e3f2fd, #bbdefb);"  # Cool blue
elif season == "autumn":
    bg_color = "linear-gradient(to right, #ffe0b2, #ffcc80);"  # Orangey
else:  # Spring
    bg_color = "linear-gradient(to right, #e8f5e9, #a5d6a7);"  # Fresh green
def emoji_tagged_response(user_input):
    tags = {
        "plant": "🌱",
        "rain": "🌧️",
        "sun": "☀️",
        "fertilizer": "🧪",
        "insect": "🐛",
        "soil": "🪴",
        "harvest": "🌾",
    }
    for keyword, emoji in tags.items():
        if keyword in user_input.lower():
            user_input = emoji + " " + user_input
    return chatbot(user_input)



chat_ui = gr.ChatInterface(
    fn=chatbot,
    title="🌱 FarmBot Chat Assistant",
    description="<span style='color: #1b5e20; font-weight: bold; font-size: 16px;'>Ask about crops, fertilizers, organic farming, seasons, and more 💬</span>",
    theme=gr.themes.Soft(),
    examples=[
        "What is the best time to plant paddy?",
        "How can I protect my plants naturally?",
        "Suggest a crop rotation plan.",
        "How to grow chillies?",
    ],
    css=custom_css
)





if __name__ == "__main__":
    chat_ui.launch(server_name="0.0.0.0", server_port=10000)
