import requests
import time
import os
import re
import subprocess
from bs4 import BeautifulSoup
from app.scraping.selenium_setting import open_url
from utilities.logger import logger

def scrape_video_url(url):
    browser = open_url(url, window_whosh=True)
    time.sleep(3)
    html = browser.page_source
    browser.quit()
    return html

def extract_video_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    video_url = soup.find("video")
    if video_url:
        return video_url.get("src")

def request_video(url, output_path):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        logger.info(f" - success to get response")
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        logger.info(f" - success to write entire video")
        return output_path
    else:
        logger.warning(f" - failed to get video (status: {response.status_code})")
        return None

def cleanup_videofile(video_path):
    input_path = video_path
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_cleaned{ext}"
    
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vcodec", "libx264",
        "-acodec", "aac",
        "-b:a", "128k",
        "-preset", "veryfast",
        "-movflags", "+faststart",
        output_path
    ]
    subprocess.run(cmd, check=True)

    return output_path

def get_file_size(filepath: str) -> dict:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    size_bytes = os.path.getsize(filepath)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    return {
        "bytes": size_bytes,
        "megabytes": size_mb
    }

def download(url, output_path):
    try:
        logger.info(f" >Extracting system_id from {url}..")
        match = re.search(r'/topads/(\d+)', url)
        if match:
            system_id = match.group(1)
            logger.info(f" >Successfully extracted system_id: {system_id}")
        else:
            raise RuntimeError(f"Failed to extract system_id from {url}")
    except Exception as e:
        raise RuntimeError(f"Failed to extract system_id from {url}: {e}") from e

    try:
        logger.info(f" >Creating output path..")
        output_path = f"{output_path}/{system_id}.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f" >Got the directory")
    except Exception as e:
        raise RuntimeError(f"Failed to get the directory: {e}") from e

    try:
        logger.info(f" >Scraping html..")
        html = scrape_video_url(url)
        if not html:
            raise RuntimeError(f"Failed to scrape html")
        logger.info(f" >Successfully scraped html")
    except Exception as e:
        raise RuntimeError(f"Failed to scrape html: {e}") from e

    try:
        logger.info(f" >Extracting video url..")
        video_url = extract_video_url(html)
        if not video_url:
            raise RuntimeError(f"Failed to extract video url")
        logger.info(f" >Successfully extracted video url")
    except Exception as e:
        raise RuntimeError(f"Failed to extract video url: {e}") from e

    try:
        logger.info(f" >Downloading video..")
        output_path = request_video(video_url, output_path)
        if not output_path:
            raise RuntimeError(f"Failed to download video")
        logger.info(f" >Successfully downloaded video")
    except Exception as e:
        raise RuntimeError(f"Failed to download video: {e}") from e
    
    try:
        logger.info(f" >Cleaning up video file..")
        cleaned_output_path = cleanup_videofile(output_path)
        if not cleaned_output_path:
            raise RuntimeError(f"Failed to cleanup video file")
        logger.info(f" >Successfully cleaned up video file")
    except Exception as e:
        raise RuntimeError(f"Failed to cleanup video file: {e}") from e
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
            logger.info(f"Video file removed successfully")
    
    try:
        logger.info(f" >Getting file size..")
        file_size = get_file_size(cleaned_output_path)
        logger.info(f" >Successfully got file size ({file_size['megabytes']} MB)")
        if file_size['megabytes'] > 19:
            raise RuntimeError(f"Video file size is too large (size: {file_size['megabytes']} MB)")
    except Exception as e:
        raise RuntimeError(f"Failed to get file size: {e}") from e

    return cleaned_output_path


if __name__ == "__main__":
    url = "https://ads.tiktok.com/business/creativecenter/topads/7479428489223077906"
    output_path = download_from_library(url)
    print(output_path)

    # video_url = "https://v16m-default.tiktokcdn.com/2b3134700b3ca3bbf0169ece8bae2bec/68300d02/video/tos/alisg/tos-alisg-ve-0051c001-sg/oweV9DrMIAQvDBgD6BFEsdASHQVNg8FsnsBXkf/?a=0&bti=NTU4QDM1NGA%3D&ch=0&cr=0&dr=0&lr=tiktok_business&cd=0%7C0%7C1%7C0&cv=1&br=2838&bt=1419&cs=0&ds=3&ft=cApXJCz7ThWHTYSVEGZmo0P&mime_type=video_mp4&qs=0&rc=OTVlNGllOjs0ZTVoZjlkZEBpMzNydHc5cmVveDMzODYzNEBeNmEzYi8wXjExL2E1NF5hYSNtcXItMmRzLWpgLS1kMC1zcw%3D%3D&vvpl=1&l=021747957868739fe80000000000000088723fffea4201abdb9d4&btag=e00088000"
    # output_path = f"app/analysing/video/temp_output/test.mp4"
    # request_video(video_url, output_path)

"""
python -m app.analysing.video.download_from_library
"""

