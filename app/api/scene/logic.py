import re
import json
import os
from app.llm.chatgpt_setting import chatgpt_4o

#input
"""
"input": {
    "video_content_structure": [
        {
            "start_sec": "0",
            "end_sec": "1",
            "structure": "hook",
            "summary": "動画の冒頭では、女性が夜食を食べた影響で顔のコンディションが悪いと訴えており、この状況に視聴者が共感しやすいようなフックを設定しています。初めの数秒での表情や言葉がインパクトを持ち、視聴者の注意を引きつける役割を果たしています。",
            "what": [
                "顔のコンディションが悪い",
                "夜食の影響",
                "共感を誘う表情"
            ],
            "how": [
                "自撮り映像を使用",
                "鏡の前での動作",
                "感情的なセリフ"
            ]
        },
        {
            "start_sec": "2",
            "end_sec": "2",
            "structure": "problem",
            "summary": "女性が顔の悩みを抱える姿を見せた後、そんな時の対処法があることを提示しています。視聴者に「これは自分の悩みでもある」と感じさせることで、共感をさらに深め、問題提起の段階に進んでいます。",
            "what": [
                "顔のコンディション",
                "悩みの存在",
                "対処法の提示"
            ],
            "how": [
                "商品を映し出す",
                "視覚的なインパクト",
                "ナレーションで解決策の存在を示唆"
            ]
        },
        {
            "start_sec": "3",
            "end_sec": "14",
            "structure": "solve",
            "summary": "YA-MANの美顔器と美容液のセットが紹介され、具体的な商品の機能と効果が説明されます。視聴者に対して「この商品を使うことであなたの悩みが解決できる」とシンプルに伝え、信頼を高める内容になっています。",
            "what": [
                "YA-MANの美顔器",
                "美容液",
                "効果的なスキンケア"
            ],
            "how": [
                "商品の詳細を示す映像",
                "使用方法やビフォーアフターを提示",
                "体験談のような語り口"
            ]
        },
        {
            "start_sec": "15",
            "end_sec": "30",
            "structure": "cta",
            "summary": "最後に、軽快な口調で美顔器の使い方とその効果を紹介し、視聴者に対して試すことを促します。特に「肌がうるおったこと」や「メイクのりが良い」と具体的な効果を示すことで、行動を促す強いメッセージを伝えています。",
            "what": [
                "美顔器の使用方法",
                "メイクのりの向上",
                "試すことの推奨"
            ],
            "how": [
                "感情を高める言葉の使用",
                "具体的な効果を示す",
                "視聴者に行動を促す"
            ]
        }
    ],
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
    video_content_structure = json.dumps(input["video_content_structure"], indent=4, ensure_ascii=False)
    client_input = json.dumps(input["client_input"], indent=4, ensure_ascii=False)

    try:
        prompt = create_prompt(video_content_structure, client_input)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    # print(prompt)
    
    try:
        result = chatgpt_4o(prompt)
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