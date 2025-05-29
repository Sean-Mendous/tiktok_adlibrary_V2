import base64
from app.llm.gemini_setting import gemini_20_flash_with_video, upload_video
from utilities.logger import logger

prompt_path = "app/analysing/video/prompt/video_analyse_gemini.md"

def encode_video(video_path):
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
        if not video_bytes:
            raise RuntimeError(f"Failed to read video file")
        video_b64 = base64.b64encode(video_bytes).decode("utf-8")
        if not video_b64:
            raise RuntimeError(f"Failed to encode video")
        return video_b64

def ask(video_path, prompt_path=prompt_path):
    # try:
    #     logger.info(f" >Encoding video..")
    #     encoded_video = encode_video(video_path)
    #     if not encoded_video:
    #         raise RuntimeError(f"Failed to encode video")
    #     logger.info(f" >Successfully encoded video")
    # except Exception as e:
    #     raise RuntimeError(f"Failed to encode video: {e}") from e

    try:
        logger.info(f" >Uploading video..")
        uploaded_file = upload_video(video_path) #need to change DNS. add "8.8.8.8", "8.8.4.4"
        if not uploaded_file:
            raise RuntimeError(f"Failed to upload video")
        logger.info(f" >Successfully uploaded video")
    except Exception as e:
        raise RuntimeError(f"Failed to upload video: {e}") from e

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
    
    return response

if __name__ == "__main__":
    response = ask("app/analysing/video/temp_output/7479428489223077906.mp4")
    print(response)


"""
python -m app.analysing.video.ask
"""

