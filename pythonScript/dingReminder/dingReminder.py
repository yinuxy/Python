# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:46:04 2020

@author: YINUXY
"""


import dingtalkchatbot.chatbot as cb
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=2174abe57b7e6874d0143ba18351ed77c59c2b7f25ad476b82bcf4a449007025'
robot = cb.DingtalkChatbot(webhook)
robot.send_markdown(title='首屏会话透出的展示内容', 
text="# 这是支持markdown的文本 \n## 标题2  \n* 列表1 \n ![alt 啊](https://gw.alipayobjects.com/zos/skylark-tools/public/files/b424a1af2f0766f39d4a7df52ebe0083.png)")