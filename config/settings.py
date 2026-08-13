import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    VOLC_ARK_API_KEY = os.getenv("VOLC_ARK_API_KEY")
    VOLC_LLM_EP = os.getenv("VOLC_LLM_EP")
    VOLC_IMAGE_EP = os.getenv("VOLC_IMAGE_EP")
    VOLC_TTS_EP = os.getenv("VOLC_TTS_EP")
    VOLC_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

settings = Settings()