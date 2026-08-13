import os
from openai import OpenAI
from config.settings import settings

os.makedirs("audio", exist_ok=True)

class TTSService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.VOLC_ARK_API_KEY,
            base_url=settings.VOLC_BASE_URL
        )
        self.model_ep = settings.VOLC_TTS_EP

    def generate_audio(self, shot_id: int, text: str):
        response = self.client.audio.speech.create(
            model=self.model_ep,
            voice="zh_female_wanwan",  # 音色名根据方舟支持的音色修改
            input=text
        )
        save_path = f"audio/shot_{shot_id}.mp3"
        response.stream_to_file(save_path)
        print(f"✅ 镜头{shot_id}音频已保存：{save_path}")

tts_service = TTSService()