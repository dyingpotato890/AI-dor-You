from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging
import spacy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Load NLP For Stats
import spacy
import subprocess

# Ensure the model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

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
    
    formatted_stats = {"Flirt Score": "N/A", "Chat Analysis": "No data available", "Stronger Areas": [], "Flaws & Areas for Improvement": [], "Tips for Next Date": []}

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([stats_prompt])
        
        if not hasattr(response, "text"):
            raise ValueError("Unexpected API response format")

        text = response.text
        doc = nlp(text)

        extracted_data = {}
        sections = ["Flirt Score", "Chat Analysis", "Stronger Areas", "Flaws & Areas for Improvement", "Tips for Next Date"]

        lines = text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            for section in sections:
                if line.startswith(f"**{section}:**"):
                    current_section = section
                    extracted_data[current_section] = []
                    inline_content = line[len(f"**{section}:**"):].strip()
                    if inline_content:
                        extracted_data[current_section].append(inline_content)
                    break
            else:
                if current_section:
                    extracted_data[current_section].append(line)

        for key in extracted_data:
            extracted_data[key] = "\n".join(extracted_data[key]).strip()

    except Exception as e:
        logger.error(f"Stats API Error: {str(e)}")
        extracted_data = {"error": str(e)}

    return jsonify({"stats": extracted_data if extracted_data else formatted_stats, "status": "success" if "error" not in extracted_data else "error"})

if __name__ == "__main__":
    app.run(debug=True)