import json
import os
import re
import time
from utilities.logger import logger

from app.analysing.video.ask import ask
from app.analysing.video.download import download

def run_flow(url):
    output_path = "app/analysing/video/temp_output"

    try:
        output_path = download(url, output_path)
        if not output_path:
            raise Exception("Failed to download video")
        logger.info(f"Video downloaded successfully")
    except Exception as e:
        raise Exception(f"Error to download video: {e}")
    
    time.sleep(5)

    try:
        response_json = ask(output_path)
        if not response_json:
            raise Exception("Failed to ask")
        logger.info(f"Asked successfully")
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
            logger.info(f"Video file removed successfully")

    try:
        def convert_to_dict(response):
            match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
            if match:
                json_str = match.group(1).strip()
            else:
                json_str = response.strip()
            if not json_str:
                raise ValueError("Empty JSON content after cleanup.")
            return json.loads(json_str)
        responce_dict = convert_to_dict(response_json)
        if not responce_dict:
            raise Exception("Failed to load json")
        logger.info(f"Json loaded successfully")
    except Exception as e:
        raise Exception(f"Error to load json: {e}")

    try:
        def convert_data(dict):
            converted_data = dict | {"system_status": "video_analysis"}
            return converted_data
        converted_data = convert_data(responce_dict)
        if not converted_data:
            raise Exception("Failed to convert data")
        logger.info(f"Data converted successfully")
    except Exception as e:
        raise Exception(f"Error to convert data: {e}")
    
    return converted_data


if __name__ == "__main__":
    url = "https://ads.tiktok.com/business/creativecenter/topads/7250421174954475522/pc/ja?rid=jzvb27itbai"
    response = run_flow(url)
    print(response)

"""
python -m app.analysing.video.logic
"""




