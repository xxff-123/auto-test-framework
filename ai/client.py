import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("AI_API_KEY")
BASE_URL = "https://ws-pbyjggxxpl6znfpl.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"



def chat(prompt, json_mode=False):
    payload = {
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": prompt}],
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    resp = requests.post(
        BASE_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
