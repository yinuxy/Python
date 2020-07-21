import bs4
import rom as rom

rom bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import csv
import time
import os

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)  # 设置等待时间


# 提取公众号文章信息
def get_info(url):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    data = []      # 用来储存文章信息
    for i in range(0, 10):
        titles = soup.select('#sogou_vr_11002601_title_{}'.format(i))
        introductions = soup.select('#sogou_vr_11002601_summary_{}'.format(i))
        dates = soup.select('#sogou_vr_11002601_box_{} div.txt-box div span'.format(i))
        for ti, intr, da in zip(titles, introductions, dates):
            info = {}
            title = ti.get_text()
            info['文章标题'] = title
            link = str(re.compile('data-share="(.*?)"').findall(str(titles))).replace('amp;', '')[2:-2]
            info['文章链接'] = link
            introduction = intr.get_text()
            info['文章简介'] = introduction
            date = str(da.get_text()).split(')')[-1]
            info['发文日期'] = date
            data.append(info)
    return data


def mkdir():      # 创建储存内容的文件夹
    isExists = os.path.exists('D:\\Python\\spider\\wecArticle')
    if not isExists:
        print('创建目录')
        os.makedirs('D:\\Python\\spider\\wecArticle')   # 创建目录
        os.chdir('D:\\Python\\spider\\wecArticle')    # 切换到创建的文件夹
        return True
    else:
        print('目录已存在,即将保存！')
        os.chdir('D:\\Python\\spider\\wecArticle')  # 切换到创建的文件夹
        return False


def write2csv(url, kw):    # 写入文件，以 csv 文件形式储存
    mkdir()
    print('正在写入文件')
    with open('{}.csv'.format(kw), 'a', newline='', encoding='utf-8') as f:
        # 追加内容用 a
        fieldnames = ['文章标题', '文章链接', '文章简介', '发文日期']  # 控制列的顺序
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = get_info(url)
        writer.writerows(data)
        print("写入成功")


if __name__ == '__main__':
    kw = input('请输入你的关键字：\n')
    for j in range(1, 11):
        url = 'http://weixin.sogou.com/weixin?query={}&type=2&page={}'.format(kw, j)
        write2csv(url, kw)
        time.sleep(1)

