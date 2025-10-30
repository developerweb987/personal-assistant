# ai_client.py
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text(prompt: str, model: str = "gemini-1.5-flash"):
    """
    Generates response text using Gemini model.
    """
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
