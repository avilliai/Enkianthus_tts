import asyncio

import modelscope_tts

Cookie="你的Cookie"                   #设置cookie
ms=modelscope_tts.TTS(Cookie)        #创建对象
print(ms.listSpeakers())             #查看所有可用的角色



#支持异步处理方式
asyncio.run(ms.tts("你好",speaker="宫子（泳装）"))