import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)


def call_claude_haiku(prompt: str, max_tokens=1024, temperature=0.7):
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    )
    return response.content[0].text


if __name__ == "__main__":
    prompt = "Tell me about this company.\nhttps://samurai-style.tokyo/"
    response = call_claude_haiku(prompt)
    print(response)