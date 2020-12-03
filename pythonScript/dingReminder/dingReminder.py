# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:46:08 2020

@author: YINUXY
"""


from datetime import datetime, date, time, timezone
import requests
import pyweathercn

def getWeather(city):
    w = pyweathercn.Weather(city)
    context = '''今天是'''+w.today(True)['date']+'\n'+w.data['city']+'''市今天的天气为'''+w.today(True)['type']+'''\n温度变化为'''+w.today(True)['temp']+'\n'+w.tip()
    return context

def sendQQ(wcontext):
    key = '*****************************'
    morning = '08:30:00'
    night = '17:30:00'
    nowtime = datetime.now().strftime('%H:%M:%S')
    if nowtime < morning:
        greeting = "早上好主人ヾ(✿ﾟ▽ﾟ)ノ\n美好的搬砖生活开始啦！(<ゝω・)☆\n快点打开手机钉钉进行上班打卡把！！！!!!(～￣▽￣)～ \n不然就要迟到啦∑(ﾟДﾟノ)ノ\n"
        context = greeting + wcontext
    elif nowtime > night:
        greeting = "晚上好主人ヾ(✿ﾟ▽ﾟ)ノ\n辛苦的搬砖生活终于结束啦！(<ゝω・)☆\n不要忘记了晚间下班打卡哟( • ̀ω•́ )✧\n"
        context = greeting
    else:
        context = "现在还没到上/下班签到时间哦\n"
    url = 'https://qmsg.zendee.cn/send/' + key + '?msg='+context
    requests.post(url)

def sendWechat(wcontext):
    key = '******************************************'
    title = ''
    morning = '08:30:00'
    night = '17:30:00'
    nowtime = datetime.now().strftime('%H:%M:%S')
    if nowtime < morning:
        title = '''上班打卡啦ヾ(✿ﾟ▽ﾟ)ノ'''
        greeting = '''>     早上好主人ヾ(✿ﾟ▽ﾟ)ノ\n美好的搬砖生活开始啦！(<ゝω・)☆\n>     快点打开手机钉钉进行上班打卡把！！！!!!(～￣▽￣)～ \n不然就要迟到啦∑(ﾟДﾟノ)ノ\n'''
        context = greeting + wcontext
    elif nowtime > night:
        title = '''下班打卡啦ヾ(✿ﾟ▽ﾟ)ノ'''
        greeting = '''>     晚上好主人ヾ(✿ﾟ▽ﾟ)ノ\n>     辛苦的搬砖生活终于结束啦！(<ゝω・)☆\n>     不要忘记了晚间下班打卡哟( • ̀ω•́ )✧'''
        context = greeting
    else:
        title = '''上班时间请勿开小差！(〝▼皿▼)'''
        context = '''现在还没到上/下班签到时间哦\n''' + wcontext + wcontext
    url = "http://sc.ftqq.com/" + key + ".send?text=" + title + "&desp=" + context
    requests.post(url)

if __name__ == '__main__':
    city = '杭州'
    w = getWeather(city)
    sendQQ(w)
    sendWechat(w)
    print(sendQQ(w))
