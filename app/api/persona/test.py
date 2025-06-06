import requests

url = "https://7223-133-125-60-141.ngrok-free.app/persona"

payload = {
    "input": {
        "target_info": {
            "age": ["20代", "30代"],
            "gender": "女性",
            "why": "マスク生活が終わってから、肌のくすみや毛穴が気になるようになり、透明感を取り戻したいと思っている。ビタミンC系のアイテムに注目が集まっているため、効果が期待できそうと感じている。",
            "issue": "以前試したビタミンC美容液は肌に刺激が強く、乾燥したり赤みが出たりした。また、効果を実感する前に使用をやめてしまったこともあり、継続のハードルが高いと感じている。"
        },
        "product_info": {
            "name": "バイタミンスカイビタミンC美容液",
            "category": "ビタミンC美容液（スキンケアアイテム）",
            "strength": "安定型ビタミンC誘導体を高濃度配合しつつ、敏感肌でも使える処方。肌にやさしく、毎日のスキンケアに無理なく取り入れられる。実感の早さと継続性が支持されている。",
            "competition": "高濃度なのに低刺激で、乾燥しにくい独自処方を実現。べたつかず、朝も夜も使いやすいテクスチャー。パッケージもシンプルでSNSに映える。",
            "ideal": "肌のくすみが改善され、毛穴も引き締まり、すっぴんに自信が持てるようになる。肌に透明感が出ることで、メイクが映える・気分が上がるなど日常の満足度が高まる。"
        },
        "marketing_info": {
            "cost": "2500円",
            "campaing": "今なら10%割引",
            "apeals": "満足度No.1",
        }
    }
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())