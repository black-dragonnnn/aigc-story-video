import json5
from typing import List
from openai import OpenAI
from openai import APIError
from pydantic import BaseModel
from config.settings import settings

# 数据模型保持不动
class Shot(BaseModel):
    shot_id: int
    scene_desc: str
    dialogue: str
    character: str
    style_prompt: str

class ScriptResult(BaseModel):
    title: str
    character_setting: str
    shots: List[Shot]

client = OpenAI(
    api_key=settings.VOLC_ARK_API_KEY,
    base_url=settings.VOLC_BASE_URL
)

class LLMService:
    def __init__(self):
        self.endpoint_id = settings.VOLC_LLM_EP

    def _clean_json_text(self, text: str) -> str:
        if "```json" in text:
            text = text.split("```json")[-1]
        if "```" in text:
            text = text.split("```")[0]
        return text.strip()

    def generate_short_script(self, story_content: str) -> ScriptResult:
        prompt = f"""
你是专业短剧编剧。根据用户提供的故事梗概，拆分成竖屏短剧分镜脚本。
严格遵守规则：
1. 只输出纯净JSON，不要任何多余解释、前言、总结；
2. JSON结构严格按照下面模板，不能增减字段；
3. scene_desc画面描述详细，适合直接用于AI绘图；
4. character_setting描述所有角色外貌、服装、特征，保证画面人物统一；
5. 生成5~8个镜头。

模板：
{{
    "title": "短剧标题",
    "character_setting": "人物整体外貌设定",
    "shots": [
        {{
            "shot_id":1,
            "scene_desc":"画面详细描述",
            "dialogue":"角色台词",
            "character":"角色名字",
            "style_prompt":"画风描述，光影、色调、质感"
        }}
    ]
}}

故事梗概：
{story_content}
"""
        try:
            resp = client.chat.completions.create(
                model=self.endpoint_id,
                messages=[{"role": "user",
                           "content": prompt
                           }],
                temperature=0.7
            )
        except APIError as e:
            raise Exception(f"火山方舟LLM调用异常：{e}")

        raw_content = resp.choices[0].message.content
        clean_text = self._clean_json_text(raw_content)
        raw_data = json5.loads(clean_text)
        script = ScriptResult(**raw_data)
        return script

llm_service = LLMService()