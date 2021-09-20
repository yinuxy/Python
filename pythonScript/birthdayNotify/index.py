# -*- coding: utf-8 -*-
import json
import time
import smtplib
import datetime
import requests
from email.mime.text import MIMEText
from email.header import Header
from borax.calendars.lunardate import LunarDate

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')


def hitokoto():
    #指定 api 的接口地址并设定 url 参数
    api_url = 'https://v1.hitokoto.cn/?c=d&c=h&c=i&c=k&encode=json'
    #向网站 api 发送请求并获取返回的数据
    response = requests.get(api_url)
    #将 json 数据对象转化为字典
    res = json.loads(response.text)
    #取出一言正文和出处拼装为字符串
    a_word = res['hitokoto']+' _____'+'《'+res['from']+'》'
    #输出一言
    return a_word

def ln_date_str(month, day):
    # 月份
    lm = '正二三四五六七八九十冬腊'
    # 日份
    ld = '初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十'
    return '{}月{}'.format(lm[month-1], ld[(day-1)*2:day*2])

def sendmail(res,relationship, name):
    sender = 'cgyung@qq.com'  # 发送邮箱
    senderName = "潜龙于野"  # 发送者昵称
    password = 'qktwjlvxlyrwcagi'  # 发送方QQ邮箱授权码
    receivers = ['admin@yinuxy.com']  # 接收邮件

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # str = getRanking() + getWinners()
    message = MIMEText(res, 'plain', 'utf-8')
    message['From'] = Header(senderName, 'utf-8')  # 发送者昵称

    # 主题
    subject = '您的{}{}快要过生日啦'.format(relationship, name)
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

def birthdayNotify(path='./birthday.json'):
    data = {}
    with open(path,'r',encoding='utf8')as fp:
        data = json.load(fp)
    for value in data.values():

        birth = value['birthday']
        birth = datetime.datetime.strptime(birth, "%Y-%m-%d")

        birthyear = birth.year
        today = datetime.date.today()

        if value['isLunar']:
            thisbirth = LunarDate(today.year,birth.month,birth.day)
            solardate = thisbirth.to_solar_date()

            if (solardate-today).days < 0 :
                thisbirth = LunarDate(today.year+1,birth.month,birth.day)
                solardate = thisbirth.to_solar_date()
            age = thisbirth.year - birthyear + 1

            # res = "今天是公历 {}  \n您的 {} {} 将于 {}年{}月{}日 过生日（{}天后）\n(农历生日{})\n\n今天是他的第{}个生日，快去为他挑选一件合适的礼物吧~\n\n{}\n\n\n".format(today, value['relationship'], value['name'], solardate.year, solardate.month, solardate.day, (solardate-today).days,ln_date_str(birth.month,birth.day), age, hitokoto())
            # print(res)
            # sendmail(res,value['relationship'], value['name'])

            if (solardate-today).days<=7 and (solardate-today).days>=0:
                res = "今天是公历 {}  \n您的{}{}将于{}年{}月{}日过生日（{}天后）\n农历:{}\n\n今天是他的第{}个生日，快去为他挑选一件合适的礼物吧~\n\n{}\n\n\n".format(today, value['relationship'], value['name'], solardate.year, solardate.month, solardate.day, (solardate-today).days, ln_date_str(birth.month,birth.day), age, hitokoto())
                print(res)
                sendmail(res,value['relationship'], value['name'])
        else:
            thisbirth = LunarDate(today.year,birth.month,birth.day)
            if (thisbirth-today).days < 0 :
                thisbirth = LunarDate(today.year+1,birth.month,birth.day)
            age = thisbirth.year - birthyear + 1

            # res = "今天是公历 {}  \n您的 {} {} 将于 {}年{}月{}日 过生日（{}天后）\n\n今天是他的第{}个生日，快去为他挑选一件合适的礼物吧~\n\n{}\n\n\n".format(today, value['relationship'], value['name'], thisbirth.year, thisbirth.month, thisbirth.day, (thisbirth-today).days, age, hitokoto())
            # print(res)
            # sendmail(str(res),value['relationship'], value['name'])

            if (thisbirth-today).days<=7 and (thisbirth-today).days>=0:
                res = "今天是公历 {}  \n您的 {} {} 将于 {}年{}月{}日 过生日（{}天后）\n\n今天是他的第{}个生日，快去为他挑选一件合适的礼物吧~\n\n{}\n\n\n".format(today, value['relationship'], value['name'], thisbirth.year, thisbirth.month, thisbirth.day, (thisbirth-today).days, age, hitokoto())
                print(res)
                # sendmail(res,value['relationship'], value['name'])
        time.sleep(5)

def handler(event, context):
    birthdayNotify()

if __name__ == '__main__':
    birthdayNotify()