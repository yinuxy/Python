#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Ryan time:2018/11/20

from pyecharts import Style
from pyecharts import Geo
import json
from pyecharts import Bar
from collections import Counter


#数据可视化

def gender():
    cities = []
    with open('E:/spiderproject/maoyanMovies_comments/comments.txt','r',encoding='utf-8')as f:
        rows = f.readlines()
        try:
            for row in rows:
                city = row.split(',')[1]
                if city != '':
                    cities.append(city)
                #print(city)
        except Exception as e:
            print(e)

    handle(cities)
    data = Counter(cities).most_common()
    style = Style(
        title_color='#fff',
        title_pos='center',
        width=1200,
        height=600,
        background_color='#404a59'
    )
    geo = Geo('《毒液》观众位置分布', '数据来源：猫眼-Ryan采集', **style.init_style)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 1000],
            visual_text_color='#fff', symbol_size=15,
            is_visualmap=True, is_piecewise=False, visual_split_number=10)
    geo.render('观众位置分布-地理坐标图.html')

    data_top20 = Counter(cities).most_common(20)
    bar = Bar('《毒液》观众来源排行TOP20', '数据来源：猫眼-Ryan采集', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render('观众来源排行-柱状图.html')

def handle(cities):
    # print(len(cities), len(set(cities)))

    # 获取坐标文件中所有地名
    data = None
    with open('C:/Users/purple.guo/AppData/Local/Continuum/anaconda3/Lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(
            'C:/Users/purple.guo/AppData/Local/Continuum/anaconda3/Lib/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))

if __name__ == '__main__':
    gender()