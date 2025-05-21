import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def gemini_20_flash_lite(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    prompt = "Tell me about this company.\nhttps://samurai-style.tokyo/"
    response = gemini_20_flash_lite(prompt)
    print(response)


