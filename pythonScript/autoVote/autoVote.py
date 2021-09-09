import time
import random
import requests
import getCookie
from lxml import etree

def geySkey(cookie):
    arrcookie = cookie.split("; ")
    for i in range(len(arrcookie)):
        arr = arrcookie[i].split("=")
        if(arr[0] == 'skey'):
            print(arr[1])
            return arr[1]

def getGTK(skey):
    skey=geySkey(skey)
    hash = 5381
    for i in range(len(skey)):
        hash = hash + (hash << 5) + int(ord(skey[i]))
    return (hash & 0x7fffffff)

def dailyTaskAutuComiit(header_dict, vote_url, comment_url, signInurl):
    base_url = "https://cloud.tencent.com/developer/ask?q=timeline"
    header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "cloud.tencent.com",
        "Referer": "https://cloud.tencent.com/developer/ask",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    r1 = requests.get(url=base_url, headers=header)
    r1.encoding = r1.apparent_encoding
    html = etree.HTML(r1.content)
    id = {}
    data  = html.xpath('//div/div[2]/div[3]/a/@href')
    for item in data:
        idstr = str(item).replace("/developer/ask/","")
        idlist = idstr.split('/answer/')
        if(len(idlist)>1):
            id[idlist[0]] = idlist[1]
    votepayloadList = []
    commentpayloadList = []
    for key,value in id.items():
        votepayload = "{\r\n  \"action\": \"VoteAnswer\",\r\n  \"payload\": {\r\n    \"questionId\": %s,\r\n    \"answerId\": %s,\r\n    \"vote\": 1\r\n  }\r\n}"%(key, value)
        commentpayload = "{\r\n  \"action\": \"CommentAnswer\",\r\n  \"payload\": {\r\n    \"questionId\": %s,\r\n    \"answerId\": %s,\r\n    \"content\": \"%s\"\r\n  }\r\n}"%(key, value, '666')
        votepayloadList.append(votepayload)
        commentpayloadList.append(commentpayload)
    index = random.sample(range(1,20),5)
    index.sort()
    for i in index:
        r1 = requests.request("POST", vote_url, headers=header_dict, data=votepayloadList[i])
        print("第{}篇文章已点赞，返回代码：".format(i),r1.text)
        time.sleep(random.randint(5,10))
        # r2 = requests.request("POST", comment_url, headers=header_dict, data=commentpayloadList[i])
        # print("第{}篇文章已评论，返回代码：".format(i),r2.text)
        # time.sleep(random.randint(5,10))

def getComment():
    commentsList = [
        "专业的回答，感谢分享",
        "不错不错",
        "大佬讲的太好啦，受益匪浅",
        "学习了，感谢分享经验",
        "太强了",
        "厉害哦",
        "不错啊",
        "很好",
        "学到了",
        "谢谢分享，学习了",
        "专业的回答",
        "666",
        "yyds",
        "11111111"
    ]
    return random.choice(commentsList)


if __name__ == '__main__':
    getCookie.init()
    getCookie.login()
    time.sleep(10)
    with open("cookie.txt", "r", encoding="utf-8") as f:
        cookie = f.read()
    csrfCode = getGTK(cookie)
    signInurl = "https://cloud.tencent.com/developer/services/ajax/grocery-stall?action=SignIn&uin=100004697298&csrfCode=%s"%(csrfCode)
    vote_url = "https://cloud.tencent.com/developer/services/ajax/ask/answer?action=VoteAnswer&uin=100004697298&csrfCode=%s"%(csrfCode)
    comment_url = "https://cloud.tencent.com/developer/services/ajax/ask/answer?action=CommentAnswer&uin=100004697298&csrfCode=%s"%(csrfCode)
    header_dict = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': f"{cookie}",
        'origin': 'https://cloud.tencent.com',
        'referer': 'https://cloud.tencent.com/developer/ask',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    dailyTaskAutuComiit(header_dict, vote_url, comment_url, signInurl)
    # print(geySkey(cookie))


