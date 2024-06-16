modelscope unofficial api

## 从pip安装
```
pip install Enkianthus_tts
```
安装此依赖

## 运行
你可以运行下面这段代码
```python
import asyncio
import Enkianthus_tts

Cookie=None              #大部分speaker不需要cookie，直接用None即可
ms=Enkianthus_tts.TTS(Cookie)        #创建对象

print(ms.listSpeakers())             #查看所有可用的角色
#异步处理方式
asyncio.run(ms.tts(text="你好",speaker="宫子（泳装）")  )
```

```python
#(如果使用["BT","塔菲","阿梓","otto","丁真","星瞳","东雪莲","嘉然","孙笑川","亚托克斯","文静","鹿鸣","奶绿","七海","恬豆","科比"]需要获取cookie
import asyncio
import Enkianthus_tts

Cookie="你的Cookie"                   #设置cookie，参照[Manyana#issue7](https://github.com/avilliai/Manyana/issues/7) 复制你的cookie
ms=Enkianthus_tts.TTS(Cookie)        #创建对象

print(ms.listSpeakers())             #查看所有可用的角色
#异步处理方式
asyncio.run(ms.tts(text="你好",speaker="阿梓")  )
```
在异步函数中使用

```python
import asyncio
import Enkianthus_tts


async def voiceGenerater():
    ms = Enkianthus_tts.TTS(None)  # 前面我们说了，除了特定speaker需要cookie，其他的直接给TTS传None就行
    await ms.tts(text="你好", speaker="宫子（泳装）")  # 返回的是文件路径，当然，你也可以传递path参数
```
