# -*- coding: utf-8 -*-

import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')


def notifyText():
    nowtime = datetime.now().strftime('%H:%M:%S')
    time1 = '08:30:00'
    time2 = '17:30:00'
    time3 = '18:30:00'
    time4 = '19:00:00'
    time5 = '23:30:00'
    return "单词背完了吗，没背完要打屁屁哟！现在已经AM 08:00了，赶快去复习上午的课程把~"
    if nowtime >= time1 and nowtime <= time2:
        return "单词背完了吗，没背完要打屁屁哟！现在已经AM 08:00了，赶快去复习上午的课程把~"
    elif nowtime >= time2 and nowtime <= time3:
        return "今天的任务完成了吗，没完成的话可是要加夜班了哦！"
    elif nowtime >= time3 and nowtime <= time4:
        return "晚饭吃完了吗，赶紧去练字去！！！"
    elif nowtime >= time4 and nowtime <= time5:
        return "现在，可以以开始晚自习拉~~~"
    elif nowtime >= time5:
        return "今天的任务完成了吗，没有也请放到明天再做吧！"


def getOneNote():
    api_url = 'https://v1.hitokoto.cn/?c=k&c=d&c=h&encode=json'
    response = requests.get(api_url)
    res = json.loads(response.text)
    a_word = res['hitokoto']+' _____'+'《'+res['from']+'》'
    print(a_word)

def sendmail():
    sender = 'cgyung@qq.com'  # 发送邮箱
    senderName = "笨鸟先飞~"  # 发送者昵称
    password = 'qktwjlvxlyrwcagi'  # 发送方QQ邮箱授权码
    receivers = ['admin@yinuxy.com']  # 接收邮件

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    str = notifyText() + getOneNote()
    message = MIMEText(str, 'plain', 'utf-8')
    message['From'] = Header(senderName, 'utf-8')  # 发送者昵称

    # 主题
    subject = '叮~您有新的学习计划'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        print("连接到邮件服务器成功")

        client.login(sender, password)
        print("登录成功")

        client.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def sendQQ():
    key = '42b60c3e094bed98331a1cc5e089ff64'
    context = notifyText() + getOneNote()
    url = 'https://qmsg.zendee.cn/send/' + key + '?msg='+context
    requests.post(url)

def sendWechat():
    key = 'SCT48533TKJb962s7xJdVTdsszsuv9Dks'
    title = '叮~您有新的学习计划'
    context = notifyText() + getOneNote()
    url = "http://sc.ftqq.com/" + key + ".send?text=" + title + "&desp=" + context
    requests.post(url)

def handler():
    print(type(notifyText()))
    sendmail()
    # sendQQ()
    # sendWechat()

if __name__ == '__main__':
    handler()