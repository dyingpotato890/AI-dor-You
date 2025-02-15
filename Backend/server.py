from flask import Flask, request, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv
import os
from google import genai

app = Flask(__name__)
CORS(app)

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API Client
client = genai.Client(api_key=gemini_api_key)

# Store conversation history per session
user_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    user_input = data.get("message")
    
    if not session_id or not user_input:
        return jsonify({"error": "Missing session_id or message"}), 400
    
    if session_id not in user_sessions:
        user_sessions[session_id] = {"conv_history": [], "user_messages": []}
    
    session = user_sessions[session_id]
    session["conv_history"].append(f"User: {user_input}")
    session["user_messages"].append(user_input)
    
    context = "\n".join(session["conv_history"][-5:])
    
    prompt = f"""
    Let's have a fun and engaging conversation! Be playful, witty, and genuinely interested
    in getting to know me. Ask thoughtful questions about my passions and dreams.
    Make the conversation feel effortless, warm, and engaging and more importantly, human-like.

    Here's our conversation so far:
    {context}

    AI:
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        
        bot_response = response.text.strip() if hasattr(response, "text") else "No valid response received. Try again later."
    except Exception as e:
        bot_response = f"An error occurred: {str(e)}"
    
    session["conv_history"].append(f"AI: {bot_response}")
    
    return jsonify({"response": bot_response})

@app.route("/stats", methods=["POST"])
def generate_stats():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in user_sessions:
        return jsonify({"error": "Invalid or missing session_id"}), 400
    
    session = user_sessions[session_id]
    user_text = "\n".join(session["user_messages"])
    
    stats_prompt = f"""
    Analyze the following conversation **ONLY based on the user's messages**.
    Provide the following insights:
    
    1. **Flirt Score:** A percentage (0-100%) based on how flirty, playful, or romantic the user's messages were.
    2. **Chat Analysis:** A short summary of the user's conversation style.
    3. **Stronger Areas:** What the user did well (e.g., humor, deep talk, engagement).
    4. **Flaws & Areas for Improvement:** How the user can improve their conversational skills.
    5. **Tips for Next Date:** Fun and useful tips to improve the next conversation.

    Here are the user's messages:
    {user_text}

    Provide your response in a structured format like this:

    **Flirt Score:** X%
    **Chat Analysis:** [Brief Summary]
    **Stronger Areas:** [What was good]
    **Flaws & Areas for Improvement:** [Suggestions]
    **Tips for Next Date:** [Practical tips]
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=stats_prompt
        )
        
        stats = response.text.strip() if hasattr(response, "text") else "No valid analysis received."
    except Exception as e:
        stats = f"An error occurred: {str(e)}"
    
    return jsonify({"stats": stats})

if __name__ == "__main__":
    app.run(debug=True)