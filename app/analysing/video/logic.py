import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from utilities.logger import logger
from app.analysing.video.ask import gemini_20_flash_video, chatgpt_4o_mini_text
from app.analysing.video.download import download
from app.db.cloudinary_setting import video_to_cloudinary
from app.llm.gemini_setting import upload_video

def run_flow(url, id, erase=True):
    output_path = "app/analysing/video"

    try:
        logger.info(f"Downloading video...")
        start = time.time()
        video_path = download(url, output_path)
        if not video_path:
            raise Exception("Failed to download video")
        end = time.time()
        logger.info(f"Video downloaded successfully ({end - start:.2f} seconds)")
    except Exception as e:
        raise Exception(f"Error to download video: {e}")
    
    time.sleep(5)

    if id:
        try:
            logger.info(f"Renaming folder...")
            dir_path = os.path.dirname(video_path)
            new_path = os.path.join(dir_path, f"{id}.mp4")
            os.rename(video_path, new_path)
            logger.info(f"Folder renamed successfully")
        except Exception as e:
            raise Exception(f"Error renaming folder: {e}")

        def upload_tasks(new_path=new_path):
            try:
                with ThreadPoolExecutor(max_workers=2) as executor:
                    task1 = executor.submit(upload_video_to_cloudinary, new_path)
                    task2 = executor.submit(upload_video_to_gemini, new_path)
                    video_url = task1.result()
                    uploaded_file = task2.result()
                    return video_url, uploaded_file
            except Exception as e:
                raise Exception(f"Error to upload video: {e}")
            
        try:
            video_url, uploaded_file = upload_tasks()
        except Exception as e:
            raise Exception(f"Error to upload video: {e}")
    else:    
        try:
            new_path = video_path
            video_url = None
            uploaded_file = upload_video_to_gemini(new_path)
            if not uploaded_file:
                raise Exception("Failed to upload video")
            logger.info(f"Video uploaded to gemini successfully")
        except Exception as e:
            raise Exception(f"Error to upload video: {e}")
        
    print(uploaded_file)

    try:
        second_responce_dict, structure_responce_dict = basic_flow(uploaded_file)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")

    try:
        logger.info(f"Converting data...")
        all_respoinces = second_responce_dict | structure_responce_dict
        def convert_data(dict):
            converted_data = dict | {"system_status": "video_analysis", "video_url": video_url}
            return converted_data
        converted_data = convert_data(all_respoinces)
        if not converted_data:
            raise Exception("Failed to convert data")
        logger.info(f"Data converted successfully")
    except Exception as e:
        raise Exception(f"Error to convert data: {e}")
    
    return converted_data

def basic_flow(uploaded_file):
    # try:
    #     logger.info('Asking by video.. (basic)')
    #     prompt_path = "app/analysing/video/prompt/basic_prompt.md"
    #     basic_responce_dict = gemini_20_flash_video(prompt_path, uploaded_file)
    #     if not basic_responce_dict:
    #         raise Exception("Failed to ask")
    #     logger.info(f"Asked successfully")
    # except Exception as e:
    #     raise Exception(f"Error to ask: {e}")
    
    # print(json.dumps(basic_responce_dict, indent=4, ensure_ascii=False))

    try:
        logger.info('Asking by video.. (second)')
        prompt_path = "app/analysing/video/prompt/second_prompt.md"
        second_responce_dict = gemini_20_flash_video(prompt_path, uploaded_file)
        if not second_responce_dict:
            raise Exception("Failed to ask")
        logger.info(f"Asked successfully")
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    print(json.dumps(second_responce_dict, indent=4, ensure_ascii=False))

    # try:
    #     logger.info('Asking by text.. (scene)')
    #     prompt_path = "app/analysing/video/prompt/scene_prompt.md"
    #     second_responce_json = json.dumps(second_responce_dict, indent=4, ensure_ascii=False)
    #     scene_responce_dict = chatgpt_4o_mini_text(prompt_path, other_input=second_responce_json)
    #     if not scene_responce_dict:
    #         raise Exception("Failed to ask")
    #     logger.info(f"Asked successfully")
    # except Exception as e:
    #     raise Exception(f"Error to ask: {e}")
    
    try:
        logger.info('Asking by text.. (structure)')
        prompt_path = "app/analysing/video/prompt/structure_prompt.md"
        second_responce_json = json.dumps(second_responce_dict, indent=4, ensure_ascii=False)
        structure_responce_dict = chatgpt_4o_mini_text(prompt_path, other_input=second_responce_json)
        if not structure_responce_dict:
            raise Exception("Failed to ask")
        logger.info(f"Asked successfully")
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    print(json.dumps(structure_responce_dict, indent=4, ensure_ascii=False))

    return second_responce_dict, structure_responce_dict

def upload_video_to_cloudinary(video_path):
    try:
        logger.info(f"Uploading video to cloudinary...")
        start = time.time()
        video_url = video_to_cloudinary(video_path)
        if not video_url:
            logger.error(f"Failed to upload video to cloudinary")
        end = time.time()
        logger.info(f"Video uploaded to cloudinary successfully ({end - start:.2f} seconds)")
        return video_url
    except Exception as e:
        raise Exception(f"Error to upload video to cloudinary: {e}")

def upload_video_to_gemini(video_path):
    try:
        logger.info(f" >Uploading video to gemini..")
        start = time.time()
        uploaded_file = upload_video(video_path) #need to change DNS. add "8.8.8.8", "8.8.4.4"
        if not uploaded_file:
            raise RuntimeError(f"Failed to upload video")
        end = time.time()
        logger.info(f"Video uploaded to gemini successfully ({end - start:.2f} seconds)")
        return uploaded_file
    except Exception as e:
        raise RuntimeError(f"Failed to upload video: {e}") from e

if __name__ == "__main__":
    url = "https://ads.tiktok.com/business/creativecenter/topads/7452202783560073217/pc/ja?rid=ddllylz4xwi"
    response = run_flow(url, id=None)
    with open('app/analysing/video/output/responses.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=4, ensure_ascii=False)

#     uploaded_file = """
# genai.File({
#     'name': 'files/hyftqcle9z5r',
#     'display_name': '7488950762450599952_cleaned.mp4',
#     'mime_type': 'video/mp4',
#     'sha256_hash': 'OGMwMmJjNjU3ZTc2MGU4ZjlmZGM0N2NjMzJkMDQ3YjY3M2VjYjI1MGUwYzNhYzUyZTFkYjQ0YmM4NDBlYWViOA==',
#     'size_bytes': '7807851',
#     'state': 'ACTIVE',
#     'uri': 'https://generativelanguage.googleapis.com/v1beta/files/hyftqcle9z5r',
#     'video_metadata': {'video_duration': '47s'},
#     'create_time': '2025-06-01T01:59:18.871036Z',
#     'expiration_time': '2025-06-03T01:59:18.833884796Z',
#     'update_time': '2025-06-01T01:59:20.454374Z'
# })
# """
#     response = basic_flow(uploaded_file)
#     print(json.dumps(response, indent=4, ensure_ascii=False))

"""
python -m app.analysing.video.logic
"""




