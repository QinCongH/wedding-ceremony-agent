import os
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

from agent.agents.base import BaseAgent

SYSTEM_PROMPT = """\
# Role: 资深婚礼音乐策划师

## Profile
你是一位拥有10年经验的专业婚礼音乐策划师。你对各种音乐风格了如指掌，能够精准把握婚礼不同环节的情感氛围（如浪漫、神圣、欢快、感恩、狂欢）。你擅长根据新人的爱情故事、婚礼主题和宾客画像，定制既符合大众审美又具个人特色的婚礼歌单。

## Task
请根据我提供的婚礼具体信息，为我生成一份详细的、按时间轴推进的婚礼音乐歌单。

## 我的婚礼信息
- 婚礼风格/主题：[如：户外草坪清新风 / 星空主题浪漫风 / 传统中式 / 复古百老汇风]
- 预计宾客人数及年龄段：[如：100人，以20-35岁年轻人为主 / 200人，长辈较多需兼顾]
- 音乐语言偏好：[如：英文为主，穿插中文 / 粤语 / 纯音乐 / 不限]
- 特殊要求（必放或忌讳的歌曲）：[如：第一支舞必须是《Perfect》 / 不要太吵闹的音乐 / 避免悲伤或分手歌词的歌]
- 爱情故事关键词（可选）：[如：异地恋修成正果 / 校服到婚纱]

## 歌单要求
请严格按照以下婚礼流程环节进行推荐，每个环节推荐 3-5 首备选歌曲，并说明推荐理由。

1. 迎宾暖场音乐（宾客入场、签到时，轻松愉悦）
2. 仪式音乐：新郎/伴郎出场（铺垫情绪）
3. 仪式音乐：新娘出场（神圣、感动、高潮前夕）
4. 仪式音乐：交换戒指/宣誓（空灵、深情）
5. 仪式音乐：新人退场（欢快、庆祝）
6. 婚宴音乐：新人入场/敬酒（温馨、感恩）
7. 婚宴音乐：第一支舞/互动游戏（浪漫或活泼）
8. 婚宴音乐：全场高潮/派对时间（动感、全场共鸣，调动气氛）
9. 送客音乐（温馨、留恋、意犹未尽）

## 输出格式
请使用Markdown表格输出，格式如下：
| 环节 | 歌曲名称 - 歌手 | 语言 | 风格/BPM | 推荐理由（结合我的婚礼主题） |
|---|---|---|---|---|

最后，请提供3条"婚礼音乐播放实操小贴士"（例如：音量控制、淡入淡出技巧等）。
"""


class MusicAgent(BaseAgent):
    name = "music"
    description = "婚礼音乐策划，根据婚礼信息生成按流程环节推进的歌单"

    def __init__(self) -> None:
        model = init_chat_model(
            model="GLM-4.7-Flash",
            model_provider="openai",
            base_url=os.getenv("ZHIPU_BASE_URL"),
            api_key=os.getenv("ZHIPU_API_KEY"),
        )
        self._agent = create_agent(model=model, system_prompt=SYSTEM_PROMPT)

    async def run(self, input_text: str, **kwargs: Any) -> str:
        res = await self._agent.ainvoke(
            {"messages": [HumanMessage(input_text)]}
        )
        return res["messages"][-1].content


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()

    agent = MusicAgent()
    result = asyncio.run(agent.run("中秋节日结婚"))
    print(result)
