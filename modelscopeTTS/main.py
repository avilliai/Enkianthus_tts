import asyncio
import json
import random

import httpx

class modelscopeTTS:
    def __init__(self, Cookie):
        self.headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.modelscope.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Cookie": Cookie}
    def listSpeakers(self):
        return ["BT","塔菲","阿梓","otto","丁真","星瞳","东雪莲","嘉然","孙笑川","亚托克斯","文静","鹿鸣","奶绿","七海","恬豆","科比"]
    async def tts(self,text="",speaker="阿梓",path="./tts.wav"):
        if text == "" or text == " ":
            text = "哼哼"
        if speaker == "阿梓":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/file="
        elif speaker == "otto":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/file="
        elif speaker == "塔菲":
            speaker = "taffy"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/file="
        elif speaker == "星瞳":
            speaker = "XingTong"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/file="
        elif speaker == "丁真":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/file="
        elif speaker == "东雪莲":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/file="
        elif speaker == "嘉然":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/file="
        elif speaker == "孙笑川":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/file="
        elif speaker == "鹿鸣":
            speaker = "Lumi"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/file="
        elif speaker == "文静":
            speaker = "Wenjing"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/file="
        elif speaker == "亚托克斯":
            speaker = "Aatrox"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/file="
        elif speaker == "奶绿":
            speaker = "明前奶绿"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/file="
        elif speaker == "七海":
            speaker = "Nana7mi"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/file="
        elif speaker == "恬豆":
            speaker = "Bekki"
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/file="
        elif speaker == "科比":
            url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/run/predict"
            newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/file="
        data = {
            "data": [text, speaker, 0.5, 0.5, 0.9, 1, "auto", None, "Happy", "Text prompt", "", 0.7],
            "event_data": None,
            "fn_index": 0,
            "dataType": ["textbox", "dropdown", "slider", "slider", "slider", "slider", "dropdown", "audio", "textbox",
                         "radio", "textbox", "slider"],
            "session_hash": "xxosa6k69g"
        }

        headers = self.headers

        #print(p)

        #headers="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        async with httpx.AsyncClient(timeout=200,headers=headers) as client:
            r = await client.post(url, json=data)
            newurl = newurp + r.json().get("data")[1].get("name")

            async with httpx.AsyncClient(timeout=200) as client:
                r = await client.get(newurl)
                with open(path, "wb") as f:
                    f.write(r.content)
                return path





