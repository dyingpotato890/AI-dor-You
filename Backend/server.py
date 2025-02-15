from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging
import re

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
    Provide insights **strictly** in the following format:

    **Flirt Score:** X%
    **Chat Analysis:** (Brief summary)
    **Stronger Areas:**  
    - Bullet points  
    - Bullet points  

    **Flaws & Areas for Improvement:**  
    - Bullet points  
    - Bullet points  

    **Tips for Next Date:**  
    1. Numbered tip  
    2. Numbered tip  

    Here are the user's messages:
    {user_text}

    Ensure the response follows this format exactly.
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([stats_prompt])

        if hasattr(response, 'text') and response.text.strip():
            raw_response = response.text.strip()
        else:
            raise ValueError("Invalid or empty response from Gemini API")

        # Extract structured data using regex
        stats_data = {}
        patterns = {
            "Flirt Score": r"\*\*Flirt Score:\*\s*(\d+%)",
            "Chat Analysis": r"\*\*Chat Analysis:\*\s*(.*?)\n",
            "Stronger Areas": r"\*\*Stronger Areas:\*\s*((?:- .+\n?)+)",
            "Flaws & Areas for Improvement": r"\*\*Flaws & Areas for Improvement:\*\s*((?:- .+\n?)+)",
            "Tips for Next Date": r"\*\*Tips for Next Date:\*\s*((?:\d+\. .+\n?)+)"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, raw_response, re.DOTALL)
            stats_data[key] = match.group(1).strip() if match else "N/A"

        # Convert to structured JSON
        formatted_stats = {
            "Flirt Score": stats_data["Flirt Score"],
            "Chat Analysis": stats_data["Chat Analysis"],
            "Stronger Areas": stats_data["Stronger Areas"].split("\n") if stats_data["Stronger Areas"] != "N/A" else [],
            "Flaws & Areas for Improvement": stats_data["Flaws & Areas for Improvement"].split("\n") if stats_data["Flaws & Areas for Improvement"] != "N/A" else [],
            "Tips for Next Date": stats_data["Tips for Next Date"].split("\n") if stats_data["Tips for Next Date"] != "N/A" else []
        }

    except Exception as e:
        logger.error(f"Stats API Error: {str(e)}")
        formatted_stats = {"error": "Failed to generate statistics", "details": str(e), "raw_output": raw_response if 'raw_response' in locals() else "N/A"}

    return jsonify({"stats": formatted_stats, "status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
