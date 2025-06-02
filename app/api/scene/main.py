import os
import re
import json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.llm.chatgpt_setting import chatgpt_4omini

app = FastAPI(root_path="/api")

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#input {sample_analyse}
"""
{
    "video_content_scene": [
        {
        "sec": 0,
        "structure": "hook",
        "summary": "角栓が大量に詰まった鼻のアップ",
        "audio_script": "角栓出しても無限に出てくる人、ごめんなさい。",
        "visual_caption": "角栓出しても無限に出てくる人",
        "visual_info": "鼻の毛穴に角栓が大量に詰まっている。ピンセットのようなもので角栓を取り除いている。",
        "visual_movement": "ピンセットで角栓を取り除く",
        "visual_background": "人物の顔",
        "visual_method": "マクロ撮影",
        "visual_prompt": "Macro shot of a nose with clogged pores, white sebum visibly protruding, tweezers removing the sebum, skin texture visible"
        },
        {
        "sec": 3,
        "structure": "hook",
        "summary": "角栓が大量に詰まった鼻のアップ",
        "audio_script": "ごめんなさい",
        "visual_caption": "ごめんなさい",
        "visual_info": "黒背景に白い文字で「ごめんなさい」と表示",
        "visual_movement": "なし",
        "visual_background": "黒背景",
        "visual_method": "テキスト表示",
        "visual_prompt": "Black background with white text apologizing: \"ごめんなさい\"."
        },
        {
        "sec": 4,
        "structure": "problem",
        "summary": "角栓が固まった状態",
        "audio_script": "角栓が固まった状態なので",
        "visual_caption": "角栓が固まった状態なので",
        "visual_info": "鼻の毛穴に角栓が詰まっている様子がアップで映し出される。",
        "visual_movement": "なし",
        "visual_background": "顔",
        "visual_method": "マクロ撮影",
        "visual_prompt": "Close-up of a nose with enlarged pores clogged with blackheads, uneven skin texture visible"
        },
        ...
    ]
}
"""

#input {client_info}
"""
{
 "persona": {
   "name": "",
   "age": "",
   "gender": "",
   "residence": "",
   "lifestyle": "",
 },
 "insight": {
   "target_issue": [
	“”,
	“”,
	“”
   ],
   "product_solve": [
	“”,
	“”,
	“”
   ]
   "other_points":[
	“”,
	“”,
	“”
   ]
 }
}
"""

#output
"""

"""

class PromptRequest(BaseModel):
    input: dict

@app.post("/scene")
def scene_api(req: PromptRequest):
    try:
        result = run_flow(req.input)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={"success": True, "data": result})

def run_flow(input: str):
    video_content_structure = json.dumps(input["video_content_structure"], indent=4, ensure_ascii=False)
    client_input = json.dumps(input["client_input"], indent=4, ensure_ascii=False)

    try:
        prompt = create_prompt(video_content_structure, client_input)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    # print(prompt)
    
    try:
        result = chatgpt_4omini(prompt)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    try:
        converted_result = convert_to_dict(result)
    except Exception as e:
        raise Exception(f"Error to convert: {e}")
    
    return converted_result

def create_prompt(video_content_structure, client_input):
    try:
        with open("app/api/scene/prompt.md", "r") as f:
            base_prompt = f.read()
        overall_prompt = f"{base_prompt}\n# video_content_structure\n{video_content_structure}\n\n\n# client_input\n{client_input}"
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
python -m app.api.scene.main
"""

#activate fastapi
"""
uvicorn app.api.scene.main:app --host 0.0.0.0 --port 8000
"""