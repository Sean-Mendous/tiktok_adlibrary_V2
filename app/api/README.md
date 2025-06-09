# Basic Settings

## Base Url
https://1f0f-133-125-60-141.ngrok-free.app/

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
        "issue": ""
    },
    "product_info": {
        "name": "",
        "category": "",
        "functional": "",
        "emotional": "",
        "cost": "",
        "marketing": ""
    }
}
```

### OUTPUT
```Json
{
    "persona": {
        "age": "", // 年齢ゾーンではなく具体的な数値
        "gender": "", // プロダクト利用者想定に応じて
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
            "functional": "", //プロダクトの強みや特徴
            "emotional": "", //プロダクトの強みや特徴
            "cost": "", //プロダクトの価格
            "marketing": "" //プロダクトのマーケティング手法（開催中のキャンペーン等）
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
            "persona": {
                "age": "", // 年齢ゾーンではなく具体的な数値
                "gender": "", // プロダクト利用者想定に応じて
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
                    "functional": "", //プロダクトの強みや特徴
                    "emotional": "", //プロダクトの強みや特徴
                    "cost": "", //プロダクトの価格
                    "marketing": "" //プロダクトのマーケティング手法（開催中のキャンペーン等）
                }
            }
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
            "caption": "「仕事でヘトヘト…もう癒やされたい」",
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


