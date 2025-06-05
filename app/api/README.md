# Basic Settings

## Base Url
https://0719-133-125-60-141.ngrok-free.app/

--------------------

# App Settings

## Generate Persona API

### Type
POST

### Endpoint
/persona

### INPUT
```Json
{
    "target_info": {
        "age": “”,
        "gender": "",
        "why": "",
        "issue": ""
    },
    "product_info": {
        "name": "",
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
```

### OUTPUT
```Json
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
```

## Generate Scene API

### Type
POST

### Endpoint
/scene

### INPUT
```Json
"input": {
    "video_url": "" // video URL
    "client_input": { // step3 output
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
```

### OUTPUT
```Json
{
    "generated_content": [
        {
            "scene": 1,
            "sec": 0,
            "structure": "hook",
            "audio_script": "「昨日夜食食べすぎたせいで顔のコンディション悪い...」",
            "visual_caption": "「仕事でヘトヘト…もう癒やされたい」",
            "visual_info": "女性がオフィスで疲れ切った表情をしている。背景にはパソコンや書類が見える。",
            "visual_movement": "女性が肩を落とし、ため息をつく。顔をしかめたり、目を閉じたりする。",
            "visual_method": "オフィスでの日常風景を再現。手持ちカメラで撮影し、リアルな雰囲気を出す。",
            "visual_prompt": "",
            "proof": "- 基本情報分析：ターゲットの課題（忙しい毎日で気持ちが落ち着かない）"
        },
        ...
    ]
}
```


