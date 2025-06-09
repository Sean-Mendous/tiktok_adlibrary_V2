import re
import json
from app.llm.gemini_setting import gemini_20_flash_with_video
from app.llm.chatgpt_setting import chatgpt_4omini
from utilities.logger import logger

def gemini_20_flash_video(prompt_path, uploaded_file):
    try:
        logger.info(f" >Reading markdown file..")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
            if not prompt:
                raise RuntimeError(f"Failed to read markdown file")
            logger.info(f" >Successfully read markdown file")
    except Exception as e:
        raise RuntimeError(f"Failed to read markdown file: {e}") from e

    try:
        logger.info(f" >Asking the prompts..")
        response = gemini_20_flash_with_video(prompt, uploaded_file)
        if not response:
            raise RuntimeError(f"Failed to ask the prompts")
        logger.info(f" >Successfully asked the prompts")
    except Exception as e:
        raise RuntimeError(f"Failed to ask the prompts: {e}") from e
    
    try:
        logger.info(f" >Converting the response to dict..")
        response_dict = convert_to_dict(response)
        if not response_dict:
            raise RuntimeError(f"Failed to convert the response to dict")
        logger.info(f" >Successfully converted the response to dict")
    except Exception as e:
        raise RuntimeError(f"Failed to convert the response to dict: {e}") from e
    
    return response_dict

def chatgpt_4o_mini_text(prompt_path, other_input):
    try:
        logger.info(f" >Reading markdown file..")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
            if not prompt:
                raise RuntimeError(f"Failed to read markdown file")
            logger.info(f" >Successfully read markdown file")
    except Exception as e:
        raise RuntimeError(f"Failed to read markdown file: {e}") from e
    
    if other_input:
        overall_prompt = prompt + "\n" + other_input
    else:
        overall_prompt = prompt

    try:
        logger.info(f" >Asking the prompts..")
        response = chatgpt_4omini(overall_prompt)
        if not response:
            raise RuntimeError(f"Failed to ask the prompts")
        logger.info(f" >Successfully asked the prompts")
    except Exception as e:
        raise RuntimeError(f"Failed to ask the prompts: {e}") from e
    
    try:
        logger.info(f" >Converting the response to dict..")
        response_dict = convert_to_dict(response)
        if not response_dict:
            raise RuntimeError(f"Failed to convert the response to dict")
        logger.info(f" >Successfully converted the response to dict")
    except Exception as e:
        raise RuntimeError(f"Failed to convert the response to dict: {e}") from e
    
    return response_dict

def convert_to_dict(response):
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
    if match:
        json_str = match.group(1).strip()
    else:
        json_str = response.strip()
    if not json_str:
        raise ValueError("Empty JSON content after cleanup.")
    return json.loads(json_str)


"""
python -m app.analysing.video.ask
"""

