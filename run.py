# run.py
from services.llm_service import llm_service
from services.image_service import image_service
#from services.tts_service import tts_service

if __name__ == "__main__":
    story = "少年在雨夜捡到一只受伤的白猫，带回家悉心照料，第二天猫咪消失，窗台留下一片银色羽毛。"
    result = llm_service.generate_short_script(story)

    print("短剧标题：", result.title)
    print("人物设定：", result.character_setting)

    for shot in result.shots:
        print(f"\n===== 镜头{shot.shot_id} =====")
        # 生成图片
        image_service.generate_image(
            shot_id=shot.shot_id,
            scene_desc=shot.scene_desc,
            style_prompt=shot.style_prompt,
            character_setting=result.character_setting
        )
        # 生成台词音频
        #tts_service.generate_audio(shot.shot_id, shot.dialogue)