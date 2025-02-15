from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Store conversation history per session
user_sessions = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    user_input = data.get("message")
    
    if not session_id or not user_input:
        return jsonify({"error": "Missing session_id or message", "status": "error"}), 400
    
    if session_id not in user_sessions:
        user_sessions[session_id] = {"conv_history": [], "user_messages": []}
    
    session = user_sessions[session_id]
    session["conv_history"].append(f"User: {user_input}")
    session["user_messages"].append(user_input)
    
    context = "\n".join(session["conv_history"][-5:])  # Use last 5 exchanges for context
    
    prompt = f"""
    Let's have a fun and engaging conversation! Be playful, witty, and genuinely interested.
    Ask thoughtful questions and make the chat feel warm and effortless.

    Here's our conversation so far:
    {context}

    AI:
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([prompt])
        
        if hasattr(response, 'text') and response.text.strip():
            bot_response = response.text.strip()
        else:
            raise ValueError("Invalid or empty response from Gemini API")
            
        logger.info(f"Successfully generated response: {bot_response[:50]}...")

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        bot_response = "Oops! I'm having some technical difficulties. Let's try that again!"

    session["conv_history"].append(f"AI: {bot_response}")
    
    return jsonify({"response": bot_response, "status": "success"})

@app.route("/stats", methods=["POST"])
def generate_stats():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in user_sessions:
        return jsonify({"error": "Invalid or missing session_id", "status": "error"}), 400
    
    session = user_sessions[session_id]
    user_text = "\n".join(session["user_messages"])
    
    stats_prompt = f"""
    Analyze the following conversation **ONLY based on the user's messages**.
    Provide insights in the following format:

    Flirt Score: X%
    Chat Analysis: Brief summary
    Stronger Areas: Bullet points of strengths
    Flaws & Areas for Improvement: Bullet points of weaknesses
    Tips for Next Date: Numbered practical tips

    Here are the user's messages:
    {user_text}

    Respond with the analysis in the exact format shown above.
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([stats_prompt])

        if hasattr(response, 'text') and response.text.strip():
            raw_response = response.text.strip()
        else:
            raise ValueError("Invalid or empty response from Gemini API")

        # Process response into structured data
        stats_data = {}
        lines = raw_response.split("\n")
        
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                stats_data[key.strip()] = value.strip()

        # Convert to structured JSON
        formatted_stats = {
            "Flirt Score": stats_data.get("Flirt Score", "N/A"),
            "Chat Analysis": stats_data.get("Chat Analysis", "N/A"),
            "Stronger Areas": stats_data.get("Stronger Areas", "N/A"),
            "Flaws & Areas for Improvement": stats_data.get("Flaws & Areas for Improvement", "N/A"),
            "Tips for Next Date": stats_data.get("Tips for Next Date", "N/A")
        }

    except Exception as e:
        logger.error(f"Stats API Error: {str(e)}")
        formatted_stats = {"error": "Failed to generate statistics", "details": str(e), "raw_output": raw_response if 'raw_response' in locals() else "N/A"}

    return jsonify({"stats": formatted_stats, "status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
