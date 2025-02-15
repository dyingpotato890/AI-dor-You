from dotenv import load_dotenv
import os
from google import genai
import logging


# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API Client
client = genai.Client(api_key=gemini_api_key)

conv_history = []
user_messages = []

def generateResponse(user_input):
    global conv_history, user_messages
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    conv_history.append(f"User: {user_input}")
    user_messages.append(user_input)

    context = "\n".join(conv_history[-5:])

    prompt = f"""
    Let's have a fun and engaging conversation! Be playful, witty, and genuinely interested
    in getting to know me. Ask thoughtful questions about my passions and dreams.
    Make the conversation feel effortless, warm, and engaging and more importantly, human like.

    Here's our conversation so far:
    {context}

    AI:
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        # Validate response
        if not hasattr(response, "text") or not response.text.strip():
            logger.warning("Received empty or invalid response from API")
            bot_response = "Hmm, I'm having trouble thinking of a response. Let's try that again!"
        else:
            bot_response = response.text.strip()
            logger.info(f"Successfully generated response: {bot_response[:50]}...")

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        bot_response = "Oops! I'm having some technical difficulties. Let's try that again!"


    conv_history.append(f"AI: {bot_response}")
    return bot_response

def generateStats():
    global user_messages

    user_text = "\n".join(user_messages)

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

    do not give any introductry messages to the response
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=stats_prompt
        )

        if hasattr(response, "text"):
            stats = response.text.strip()
        else:
            stats = "No valid analysis received."

    except Exception as e:
        stats = f"An error occurred: {str(e)}"

    print("\n=== Conversation Stats ===")
    print(stats)
    print("=========================\n")

# Conversation Start
print("AI: Hey there! I'm Gemini. Let's chat! (Type 'exit' to quit)")

while True:
    user_input = input("You: ")
    print()
    if user_input.lower() == "exit":
        print("AI: Goodbye! It was great talking to you! 😊")
        generateStats()
        break

    response = generateResponse(user_input)
    print(f"AI: {response}\n")
