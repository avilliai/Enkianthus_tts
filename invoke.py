import modelscope_tts

Cookie="你的Cookie"                   #设置cookie
ms=modelscope_tts.TTS(Cookie)        #创建对象
print(ms.listSpeakers())             #查看所有可用的角色

#语音合成是ms的tts方法，支持三个参数,text、speaker、path
ms.tts("你好")                        #只传text
ms.tts(text="你好",speaker="阿梓")     #使用 阿梓 合成语音
ms.tts("你好","阿梓","./data/tb.wav")  #额外传递路径变量(相对)
