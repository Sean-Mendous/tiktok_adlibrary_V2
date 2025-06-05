import json
import requests

url = "https://7223-133-125-60-141.ngrok-free.app/scene"

payload = {
    "input": {
        "video_url": "https://res.cloudinary.com/dyyaw3qpo/video/upload/v1748605410/jhm8ktihlxnjfhgnebsc.mp4",
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
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", json.dumps(response.json(), indent=4, ensure_ascii=False))