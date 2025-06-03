import re
import json
from app.llm.chatgpt_setting import chatgpt_4omini

#input
"""
{
 "target_info": {
   "age": “”,
   "gender": "",
   "why": "",
   "issue": ""
 },
 "product_info": {
   "category": "",
   "strength": "",
   "competition": "",
   "ideal": ""
 }
 "marketing_info": {
   "cost": "",
   "campaing": "",
   "apeals": ""
 }
}
"""

#output
"""
{
  "persona": {
    "name": "", // 想定ターゲットにリアリティを持たせるための仮名
    "age": "", // 年齢ゾーンではなく具体的な数値
    "gender": "", // プロダクト利用者想定に応じて
    "residence": "", // 都市名や地域性に基づく生活傾向を想定
    "lifestyle": "", // 生活スタイルや優先する価値観
  },
  "insight": {
    "target_issue": [
        // ペルソナの生活・経験からくる悩みや不安（感情・行動両面）
    ],
    "product_solve": [
        // 商品・サービスの特徴によってどうそれが解決されるか
    ]
    "other_points":[
        // 今後このペルソナを念頭に企画を進めていく中で、注意するべき点や推していくべき点など
    ]
    "product": {
      "name": "", //プロダクトの名前
      "strength": "", //プロダクトの強みや特徴
      "competition": "", //プロダクトの競合との差別化
      "ideal": "" //プロダクト使用後のイメージ像
    }
    "marketing_info": {
      "cost": "", //価格
      "campaing": "", //開催中のキャンペーン
      "apeals": "" //訴求ポイント
    }
  }
}
"""

def run_flow(input: str):
    try:
        prompt = create_prompt(input)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    try:
        result = chatgpt_4omini(prompt)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    try:
        converted_result = convert_to_dict(result)
    except Exception as e:
        raise Exception(f"Error to convert: {e}")
    
    return converted_result
    
def create_prompt(input: str):
    try:
        with open("app/api/persona/prompt.md", "r") as f:
            base_prompt = f.read()
        overall_prompt = f"{base_prompt}{input}"
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