import os
import requests
import json
from config.settings import settings

os.makedirs("pic", exist_ok=True)

class ImageService:
    def __init__(self):
        self.api_key = settings.VOLC_ARK_API_KEY
        self.model_ep = settings.VOLC_IMAGE_EP
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

    def generate_image(self, shot_id: int, scene_desc: str, character_setting: str, style_prompt: str):
        prompt = f"{character_setting} {scene_desc}, {style_prompt}, 竖屏画面，电影质感，高清细节"

        # Seedream 方舟国内接口标准参数
        payload = {
            "model": self.model_ep,
            "prompt": prompt,
            "width": 1080,
            "height": 1920,
            "n": 1
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        resp = requests.post(self.base_url, headers=headers, json=payload)
        print("响应原始数据：", resp.text)
        resp.raise_for_status()
        data = resp.json()

        # 适配方舟Seedream返回结构
        image_url = data["data"][0]["url"]
        img_data = requests.get(image_url).content
        save_path = f"pic/shot_{shot_id}.png"
        with open(save_path, "wb") as f:
            f.write(img_data)
        print(f"✅ 镜头{shot_id}图片已保存：{save_path}")

image_service = ImageService()