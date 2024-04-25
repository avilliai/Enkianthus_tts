modelscope unofficial api
# 使用
## 从pip安装
```
pip install modelscope_tts
```
安装此依赖
## 获取cookie
参照[Manyana#issue7](https://github.com/avilliai/Manyana/issues/7) 复制你的cookie
## 运行
你可以运行下面这段代码
```
import asyncio
import modelscope_tts

Cookie="你的Cookie"                   #设置cookie
ms=modelscope_tts.TTS(Cookie)        #创建对象
print(ms.listSpeakers())             #查看所有可用的角色

#语音合成是ms的tts方法，支持三个参数,text、speaker、path
ms.tts("你好")                        #只传text
ms.tts(text="你好",speaker="阿梓")     #使用 阿梓 合成语音
ms.tts("你好","阿梓","./data/tb.wav")  #额外传递路径变量(相对)

#支持异步处理方式
asyncio.run(ms.asynctts("你好")  )
```
## 最后
喜欢项目的话可以给个star喵，给个star谢谢喵
