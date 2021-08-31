import requests
import json

def getMedalsList(url, replaceTxt):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        # 替换多余的内容
        data = str.replace(r.text, replaceTxt + "(", "")
        data = str.replace(data, ");", "")
        # 解码json，转成字典
        medals = json.loads(data)

        return medals

    except:
        return "Failed!"

# 获取排行榜数据
def getRanking():
    url = "https://api.cntv.cn/olympic/getOlyMedals?serviceId=pcocean&itemcode=GEN-------------------------------&t=jsonp&cb=omedals1"
    medals = getMedalsList(url, "omedals1")
    # 获取数据列表
    medalList = medals['data']['medalsList']
    res = ""
    for i in range(5):
        res += "第" + medalList[i]["rank"] + "名：" + medalList[i]["countryname"] + "（" + medalList[i]["countryid"] + "）\n"
        res += "金牌/银牌/铜牌：" + medalList[i]["gold"] + "/" + medalList[i]["silver"] + "/" + medalList[i]["bronze"] + "\n\n"
    return res

# 中国奖牌获得者数据
def getWinners():
    url = "https://api.cntv.cn/Olympic/getOlyMedalList?t=jsonp&cb=OM&serviceId=pcocean&countryid=CHN"
    owners = getMedalsList(url, "OM")
    # 获取数据列表
    ownerList = owners['data']['medalList']
    gold = ""  # 金牌
    silver = ""  # 银牌
    bronze = ""  # 铜牌
    for owner in ownerList:
        medaltype = owner['medaltype']  # 奖牌类型
        startdatecn = owner['startdatecn']  # 日期CN
        item = owner['itemcodename'] + " " + owner['subitemname']  # 项目
        playname = owner['playname']  # 运动员
        if medaltype == "ME_GOLD":
            gold += "日期：" + startdatecn + "\n项目：" + item + "\n获得者：" + playname+"\n\n"
        elif medaltype == "ME_SILVER":
            silver += "日期：" + startdatecn + "\n项目：" + item + "\n获得者：" + playname+"\n\n"
        elif medaltype == "ME_BRONZE":
            bronze += "日期：" + startdatecn + "\n项目：" + item + "\n获得者：" + playname+"\n\n"

    res = "\n-------金牌：---------\n" + gold+"\n-------银牌：---------\n" + silver+"\n-------铜牌：---------\n"+ bronze
    return res

if __name__ == '__main__':
    print(getRanking())
    print(getWinners())