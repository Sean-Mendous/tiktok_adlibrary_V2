import os
import cloudinary
import cloudinary.uploader

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

def video_to_cloudinary(local_video_path):
    try: 
        result = cloudinary.uploader.upload_large(
            local_video_path,
            resource_type="video"
        )
        return result['secure_url']
    except Exception as e:
        raise Exception(f"Error to upload video to cloudinary: {e}")

if __name__ == "__main__":
    url = video_to_cloudinary("app/analysing/video/7488950762450599952_cleaned.mp4")
    print(url)

"""
python -m app.db.cloudinary_setting
"""