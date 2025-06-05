import re
import json
import os
import time
import requests
from app.llm.chatgpt_setting import chatgpt_4o
from app.llm.gemini_setting import upload_video, gemini_20_flash_with_video

#input
"""
"input": {
    "video_url": ""
    "client_input": {
        "basic": {
            "target_info": {
                "age": "20",
                "gender": "女性",
                "why": "日々のストレスや不安を少しでも和らげたいと感じている。自宅で気軽にリラックスできる手段を探している。",
                "issue": "忙しい毎日で気持ちが落ち着かない。寝つきも悪く、気持ちを切り替えるのが難しい。"
            },
            "product_info": {
                "category": "アロマミスト",
                "name": "スフェンガミカクス・ランバン種シリーズ",
                "strength": "100%天然精油使用で、香りによるリラックス効果が高い。持ち運びやすいコンパクトサイズ。",
                "competition": "多くのアロマ系商品は合成香料を使用しており、香りが強すぎたり持続性に欠けたりする。",
                "ideal": "自然な香りで気分を整えたい人にとって、無理なく生活に取り入れられるプロダクト。"
            },
            "marketing_info": {
                "cost": "1,800円（税込）",
                "campaing": "初回購入限定30%オフ＋ミニサイズサンプル付きキャンペーン",
                "apeals": "“香りで、心を整える” をキャッチコピーに、SNSでの使用シーン動画を展開"
            }
        },
        "insight": {
            "target_issue": [
                "自宅でリラックスできる時間が少ない",
                "ストレスがたまりやすく、切り替えが難しい",
                "ナチュラルな香りが好みだけど、合成香料が多くて選びにくい"
            ],
            "product_solve": [
                "天然アロマで自宅でも自然に気持ちを切り替えられる",
                "寝る前や作業中にも使いやすいやさしい香り",
                "シンプルなデザインで空間に溶け込む"
            ],
            "other_points": [
                "化粧ポーチにも入るミニサイズで持ち運び便利",
                "スプレータイプで使いやすい",
                "インテリアに馴染むニュアンスカラーのパッケージ"
            ]
        }
    }
}
"""

#output
"""
{
  "generated_content": [
    {
      "scene": 1
      "start_sec": 0,
      "end_sec": 0,
      "structure": "",
      "audio_script": "",
      "visual_caption": "",
      "visual_info": "",
      "visual_movement": "",
      "visual_method": "",
      "visual_prompt": "",
      "proof": ""
    },
    ...
  ]
}
"""

def run_flow(input: str):
    video_url = input["input"]["video_url"]
    client_input = input["input"]["client_input"]

    try:
        prompt_01 = create_prompt_01(client_input)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    try:
        video_path = request_video(video_url, "app/api/scene/video.mp4")
    except Exception as e:
        raise Exception(f"Error downloading video: {e}")

    # video_path = "app/api/scene/video.mp4"
    
    try:
        uploaded_file = upload_video(video_path)
    except Exception as e:
        raise Exception(f"Error to upload video: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
    
    try:
        free_format_responce = gemini_20_flash_with_video(prompt_01, uploaded_file)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    print(free_format_responce)
    
    try:
        prompt_02 = create_prompt_02(free_format_responce)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    try:
        json_format_responce = chatgpt_4o(prompt_02)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    print(json_format_responce)
    
    try:
        converted_result = convert_to_dict(json_format_responce)
    except Exception as e:
        raise Exception(f"Error to convert: {e}")
    
    return converted_result

def create_prompt_01(client_input):
    try:
        with open("app/api/scene/01_prompt.md", "r") as f:
            base_prompt = f.read()
        overall_prompt = f"{base_prompt}{client_input}"
        return overall_prompt
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
def create_prompt_02(free_input):
    try:
        with open("app/api/scene/02_prompt.md", "r") as f:
            base_prompt = f.read()
        overall_prompt = f"{base_prompt}{free_input}"
        return overall_prompt
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")

def convert_to_dict(response):
    try:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = response.strip()
        if not json_str:
            raise ValueError("Empty JSON content after cleanup.")
        return json.loads(json_str)
    except Exception as e:
        raise Exception(f"Error to convert to dict: {e}")

def request_video(url, output_path):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        return output_path
    else:
        return None

if __name__ == "__main__":
    input_path = "app/api/scene/test/input.json"
    with open(input_path, 'r', encoding='utf-8') as f:
        input = json.load(f)

    result = run_flow(input)

    output_path = "app/api/scene/test/output.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print('All Done!')

"""
python -m app.api.scene.logic
"""