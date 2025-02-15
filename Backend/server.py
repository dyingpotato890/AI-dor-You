from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
<<<<<<< Updated upstream
=======
import json
>>>>>>> Stashed changes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
<<<<<<< Updated upstream

# Initialize Gemini API Client
=======
>>>>>>> Stashed changes
genai.configure(api_key=gemini_api_key)

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
    
    context = "\n".join(session["conv_history"][-5:])  # Use last 5 exchanges for context
    
    prompt = f"""
    Let's have a fun and engaging conversation! Be playful, witty, and genuinely interested.
    Ask thoughtful questions and make the chat feel warm and effortless.

    Here's our conversation so far:
    {context}

    AI:
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
<<<<<<< Updated upstream
        response = model.generate_content(prompt)
=======
        response = model.generate_content([prompt])
>>>>>>> Stashed changes
        bot_response = response.text.strip() if hasattr(response, "text") else "No valid response received."
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
<<<<<<< Updated upstream
    Analyze the following conversation *ONLY based on the user's messages*.
    Provide insights in JSON format:

    {{
        "Flirt Score": "X%",
        "Chat Analysis": "Brief summary",
        "Stronger Areas": "What was good",
        "Flaws & Areas for Improvement": "Suggestions",
        "Tips for Next Date": "Practical tips"
    }}

    Here are the user's messages:
    {user_text}
=======
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
>>>>>>> Stashed changes
    """



    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
<<<<<<< Updated upstream
        response = model.generate_content(stats_prompt)

        if hasattr(response, "text"):
            stats_data = response.text.strip()
        else:
            stats_data = '{"error": "No valid analysis received."}'

    except Exception as e:
        stats_data = f'{{"error": "An error occurred: {str(e)}"}}'
    
=======
        response = model.generate_content([stats_prompt])
        
        if hasattr(response, "text"):
            raw_response = response.text.strip()

            try:
                # Parse the raw response into structured data
                stats_data = {}
                lines = raw_response.split('\n')
                
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        stats_data[key.strip()] = value.strip()
                
                # Convert to the required JSON structure
                formatted_stats = {
                    "Flirt Score": stats_data.get("Flirt Score", "N/A"),
                    "Chat Analysis": stats_data.get("Chat Analysis", "N/A"),
                    "Stronger Areas": stats_data.get("Stronger Areas", "N/A"),
                    "Flaws & Areas for Improvement": stats_data.get("Flaws & Areas for Improvement", "N/A"),
                    "Tips for Next Date": stats_data.get("Tips for Next Date", "N/A")
                }
                
                stats_data = formatted_stats
                    
            except Exception as e:
                print(f"Error processing stats: {str(e)}")
                stats_data = {
                    "error": "Failed to process statistics",
                    "details": str(e),
                    "raw_output": raw_response
                }


        else:
            stats_data = {"error": "No valid analysis received."}
    
    except Exception as e:
        print(f"Error generating stats: {str(e)}")
        stats_data = {
            "error": "Failed to generate statistics",
            "details": str(e)
        }

    
>>>>>>> Stashed changes
    return jsonify({"stats": stats_data})

if __name__ == "__main__":
    app.run(debug=True)
