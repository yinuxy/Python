import json
import argparse
import time
import re
import requests
import pymongo
import numpy as np
import pandas as pd
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt

DB = "cellphone"

def fix_url(string):
    if re.match(r"http://", string):
        return string
    if re.match(r"//", string):
        return "http:" + string

def get_page_num():
    url = "https://list.jd.com/list.html?cat=9987,653,655"
    r = requests.get(url, verify=False)
    content = r.content
    root = etree.HTML(content)
    page_nodes = root.xpath('.//span[@class="p-num"]/a')
    for node in page_nodes:
        if node.attrib["class"] == "":
            page_num = int(node.text)
            return page_num

def get_price(skuid):
    url = "https://c0.3.cn/stock?skuId=" + str(skuid) + "&area=1_72_4137_0&venderId=1000004123&cat=9987,653,655&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}&ch=1&fqsp=0&pduid=15379228074621272760279&pdpin=&detailedAdd=null&callback=jQuery3285040"
    r = requests.get(url, verify=False)
    content = r.content.decode('GBK')
    matched = re.search(r'jQuery\d+\((.*)\)', content, re.M)
    if matched:
        data = json.loads(matched.group(1))
        price = float(data["stock"]["jdPrice"]["p"])
        return price
    return 0

def get_item(skuid, url):
    price = get_price(skuid)
    r = requests.get(url, verify=False)
    content = r.content
    root = etree.HTML(content)
    nodes = root.xpath('.//div[@class="Ptable"]/div[@class="Ptable-item"]')
    params = {"price": price, "skuid": skuid}
    for node in nodes:
        text_nodes = node.xpath('./dl')[0]
        k = ""
        v = ""
        for text_node in text_nodes:
            if text_node.tag == "dt":
                k = text_node.text
            elif text_node.tag == "dd" and "class" not in text_node.attrib:
                v = text_node.text
                params[k] = v
    return params

def get_cellphone(page):
    url = "https://list.jd.com/list.html?cat=9987,653,655&page={}&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=4#J_main".format(page)
    r = requests.get(url, verify=False)
    content = r.content.decode("utf-8")
    root = etree.HTML(content)
    cell_nodes = root.xpath('.//div[@class="p-img"]/a')
    client = pymongo.MongoClient()
    db = client[DB]
    for node in cell_nodes:
        item_url = fix_url(node.attrib["href"])
        matched = re.search('item.jd.com/(\d+)\.html', item_url)
        skuid = int(matched.group(1))
        saved = db.items.find({"skuid": skuid}).count()
        if saved > 0:
            print(saved)
            continue
        item = get_item(skuid, item_url)
        db.items.insert(item)

def norm_weight(weight_str):
    matched = re.search(r'(\d+)', weight_str)
    weight = 0
    if matched:
        weight = matched.group(1)
    return weight

def norm_screen_size(screen_size_str):
    matched = re.search(r'(\d+\.\d+)', screen_size_str)
    screen_size = 0
    if matched:
        screen_size = float(matched.group(1))
    return screen_size

def norm_rom(rom_str):
    rom = 0
    matched = re.search(r'(\d+)MB', rom_str)
    if matched:
        rom = float(matched.group(1)) / 1024
    matched = re.search(r'(\d+)TB', rom_str)
    if matched:
        rom = float(matched.group(1)) * 1024
    matched = re.search(r'(\d+)GB', rom_str)
    if matched:
        rom = float(matched.group(1))
    return rom

def norm_ram(ram_str):
    ram = 0
    matched = re.search(r'(\d+)MB', ram_str)
    if matched:
        ram = float(matched.group(1)) / 1024
    matched = re.search(r'(\d+)GB', ram_str)
    if matched:
        ram = float(matched.group(1))
    return ram

def norm_screen_res(screen_res_str):
    width = 0
    height = 0
    matched = re.search(r'(\d+)[x*](\d+)', screen_res_str)
    if matched:
        width = matched.group(2)
        height = matched.group(1)
    return (width, height)

def norm_battery_cap(battery_cap_str):
    items = re.findall(r'(\d+)', battery_cap_str)
    items = list(map(lambda x: int(x), items))
    if len(items) == 0:
        return 0
    return max(items)

def norm_front_cam(front_cam_str):
    pass

def norm_back_cam(back_cam_str):
    pass

def norm_dual_sim(dual_sim_str):
    if dual_sim_str is None:
        return False

    dual_sim = False
    matched = re.search(r'双卡双待', dual_sim_str)
    if matched:
        dual_sim = True
    return dual_sim

def preprocess(items):
    result = []
    for item in items:
        if '品牌' not in item:
            continue

        weight_str = item.get('机身重量（g）', '')
        weight = norm_weight(weight_str)
        screen_size_str = item.get('主屏幕尺寸（英寸）', '')
        screen_size = norm_screen_size(screen_size_str)
        rom_str = item.get('ROM', '')
        rom = norm_rom(rom_str)
        ram_str = item.get('RAM', '')
        ram = norm_ram(ram_str)
        screen_res_str = item.get('分辨率', '')
        screen_res_width, screen_res_height = norm_screen_res(screen_res_str)
        battery_cap_str = item.get('电池容量（mAh）', '')
        battery_cap = norm_battery_cap(battery_cap_str)
        front_cam_str = item.get('前置摄像头', '')
        front_cam = norm_front_cam(front_cam_str)
        back_cam_str = item.get('后置摄像头')
        back_cam = norm_back_cam(back_cam_str)
        dual_sim_str = item.get('双卡机类型')
        dual_sim = norm_dual_sim(dual_sim_str)

        cellphone = {
            "brand": item.get('品牌'),
            "model": item.get('型号'),
            "color": item.get('机身颜色'),
            "weight": weight,
            "material": item.get('机身材质分类'),
            "cpu_brand": item.get('CPU品牌'),
            "cpu_freq": item.get('CPU频率'),
            "cpu_core": item.get('CPU核数'),
            "cpu_model": item.get('CPU型号'),
            "gpu_model": item.get('GPU型号'),
            "dual_sim": dual_sim,
            "network_4g": item.get('4G网络'),
            "rom": rom,
            "ram": ram,
            "screen_size": screen_size,
            "screen_res_width": screen_res_width,
            "screen_res_height": screen_res_height,
            "screen_mat": item.get('屏幕材质类型'),
            "battery_cap": battery_cap,
            "front_cam": item.get('前置摄像头'),
            "back_cam": item.get('后置摄像头'),
            "price": item.get('price'),
        }
        result.append(cellphone)
    return result

def query():
    client = pymongo.MongoClient()
    db = client[DB]
    items = db.items.find({})
    result = preprocess(items)
    df = pd.DataFrame(result)
    #df.drop_duplicates(subset=["brand", "model", "rom", "ram"], inplace=True)
    df_res = df[df.cpu_brand=="骁龙（Snapdragon)"][df.battery_cap >= 3000][df.rom >= 64][df.ram >= 6][df.dual_sim == True][df.price<=1500][df.brand=="小米（MI）"]
    print(df_res[["brand", "model", "color", "cpu_brand", "cpu_freq", "cpu_core", "cpu_model", "rom", "ram", "battery_cap", "price"]].sort_values(by=["price", "battery_cap"], ascending=[True, False]).to_csv("cellPhone.csv", encoding="GBK"))
    return df_res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", help="save data from web", action="store_true", dest="save")
    parser.add_argument("--query", help="query data from DB", action="store_true", dest="query")
    args = parser.parse_args()

    if args.save:
        page_num = get_page_num()
        for i in range(page_num):
            get_cellphone(i)
    elif args.query:
        query()
