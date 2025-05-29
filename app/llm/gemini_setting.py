import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from utilities.logger import logger
 

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def gemini_20_flash_lite(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(prompt)
    return response.text

def gemini_20_flash_with_video(prompt, uploaded_file):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(
        contents=[
            {
                "parts": [
                    {
                        "file_data": {
                            "file_uri": uploaded_file.uri,
                            "mime_type": "video/mp4"
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response.text

def upload_video(video_path: str, timeout_count=10) -> genai.types.File:
    uploaded_file = genai.upload_file(video_path, mime_type="video/mp4")
    file_id = uploaded_file.name

    wait_interval = 3
    for i in range(timeout_count):
        file = genai.get_file(file_id)
        if file.state.name == "ACTIVE":
            return file
        elif file.state.name == "FAILED":
            logger.warning(f" - file failed to upload. ({i}/{timeout_count})")
        else:
            logger.error(f" - unknown file status: {file.state.name}")
        time.sleep(wait_interval)

    raise TimeoutError(f"File {file_id} did not become ACTIVE within {timeout_count} times.")

if __name__ == "__main__":
    # prompt = "Tell me about this company.\nhttps://samurai-style.tokyo/"
    # response = gemini_20_flash_lite(prompt)

    video_path = "app/analysing/video/temp_output/7172374071391453186.mp4"
    uploaded_file = upload_video(video_path)
    prompt = "この動画について教えて"
    response = gemini_20_flash_with_video(prompt, uploaded_file)
    print(response)

"""
python -m app.analysing.gemini_setting
"""


