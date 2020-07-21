# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:01:12 2020

@author: Yinux
"""

import json
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import time
import pymysql.cursors
#FEED_EXPORT_ENCODING = 'utf-8'

class VipSpider(object):
    def __init__(self, url, search, start_page, end_page):
       ua = random.choice(self.user_agent_list)
        self.url = url
        self.search = search
        self.start_page = start_page
        self.end_page = end_page
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        self.proxies = {
            "http:":"123.101.213.98:9999",
            "http":"114.101.42.127:65309",
            "http":"39.106.194.91:808",
            "http":"122.51.231.113:8080",
            "http":"36.248.132.250:9999",
            "http":"180.118.128.54:9000",
            "http":"113.195.224.194:9999",
            "http":"39.108.59.34:8118",
            "http":"47.94.200.124:3128",
            "http":"163.204.246.83:9999",
            "http":"113.124.94.72:9999"
        }
        self.driver = webdriver.Chrome()
        self.conn=pymysql.connect(host="127.0.0.1",
                                  user="username",
                                  passwd="pasword",
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS `vip`")
        self.cur.execute("USE vip")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cosmetics (`id` INT PRIMARY KEY AUTO_INCREMENT,`title` VARCHAR(200),`discount` VARCHAR(10),`saleprice` VARCHAR(10),`oldprice` VARCHAR(10),`shopname` VARCHAR(100),`description` VARCHAR(200),`imageurl` VARCHAR(300),`itemurl` VARCHAR(100))")


    def handle_click(self):
        self.driver.get(self.url)
        self.driver.find_elements_by_xpath("//*[@id='J_main_nav_link']/li[13]/a")[0].click()
        sleep(2)
        self.driver.find_elements_by_xpath("//*[@id='J-search']/div[1]/input")[0].send_keys(self.search)
        sleep(2)
        self.driver.find_elements_by_xpath("//*[@id='J-search']/div[1]/a/span")[0].click()
        sleep(3)
 
    def handle_url(self, page):
        Durl = self.driver.current_url  # "https://category.vip.com/suggest.php?keyword=%E7%AF%AE%E7%90%83&ff=235|12|1|1"
        index = Durl.rfind("&")
        Durl = Durl[:index]
        data = {
            "page": page
        }
        res = requests.get(url=Durl, params=data, headers=random.choice(self.headers),proxies=random.choice(self.proxies))
        newurl = res.url
        print(newurl)
        return newurl
 
    def scroll_page(self, req):
        self.driver.get(req)
        sleep(3)
        for x in range(20):
            js = "var q=document.documentElement.scrollTop=10000"
            self.driver.execute_script(js)  # 执行脚本(滚动)
            sleep(5)
        html = self.driver.page_source
 
        return html
 
    def downloadin(self, url):
        req = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(req.content,"lxml")
        GoodsList = soup.select("div.pi-title-box")
        for div in GoodsList:
            shopname = div.a.get_text()
            try:
                desc = div.select("span.goods-description-title")[0].get_text()
            except:
                desc = ''
            return shopname,desc

    def download(self, request):
        soup = BeautifulSoup(request, "lxml")
        SectionList = soup.select("section#J_searchCatList")[0]
        GoodsList = SectionList.select("div.c-goods")
        items = []
        for div in GoodsList:
            item = {}
            itemlink = div.select("h4.goods-info a")[0].get('href')
            imageslink = div.img["data-original"]
            title = div.select("h4.goods-info a")[0].get_text()
            discount = div.select("div.goods-info span")[0].get_text()
            pricewra = div.select("div.goods-info em")[0].get_text()
            marprice = div.select("div.goods-info del.goods-market-price ")[0].get_text()
            item["商品链接"] = 'http:' + itemlink
            item["图片链接"] = 'http:' + imageslink
            item["商品名称"] = title
            item["商品折扣"] = discount
            item["特卖价格"] = pricewra
            item["原始价格"] = marprice
            item["商铺名称"], item["商品描述"] = self.downloadin(item["商品链接"])
            self.process_item(item)
            items.append(item)
        
        return items
 
    def process_item(self,item):
#        self.cur = self.conn.cursor()
        try:
            itemurl = item["商品链接"]
            imageurl = item["图片链接"]
            title = item["商品名称"]
            discount = item["商品折扣"]
            saleprice = item["特卖价格"]
            oldprice = item["原始价格"]
            shopname = item["商铺名称"]
            description = item["商品描述"]
            sql = "INSERT INTO `Cosmetics` (`title`, `discount`,`saleprice`,`oldprice`,`shopname`,`description`, `imageurl`,`itemurl`) VALUES ('"+title+"','"+discount+"','"+saleprice+"','"+oldprice+"','"+shopname+"','"+description+"','"+imageurl+"','"+itemurl+"')"
            self.cur.execute(sql)
            self.conn.commit()
#            self.conn.close()
        except Exception as err:
            print(err)
            
    def startSpider(self):
        htmlList = []
        for page in range(int(self.start_page), int(self.end_page) + 1):
            print("正在抓取第"+ str(page) +"页的数据")
            start = time.time()
            if page == 1:
                self.handle_click()
                req = self.handle_url(page)
                newhtml = self.scroll_page(req)
                htmlList += self.download(newhtml)
            else:
                req = self.handle_url(page)
                newhtml = self.scroll_page(req)
                htmlList += self.download(newhtml)
            end = time.time()
            print("第"+ str(page) +"页的数据抓取完毕，用时"+ str(end-start) +"s")
        # 【数据的存储】写入json数据
        # 将列表转化成json字符串
        
        string = json.dumps(htmlList,ensure_ascii=False)
        with open("vip2.json", "w", encoding="utf-8") as fp:
            fp.write(string)
        self.conn.close()
 
 
def main():
    starts = time.time()
    url = "http://www.vip.com/"
    search = '化妆品'
#    search = input("请输入你要搜索的商品:")
    start_page = 1
#    start_page = input("请输入你要爬取的起始页:")
    end_page = 40
#    end_page = input("请输入你要爬取的结束页:")
    spider = VipSpider(url, search, start_page, end_page)
    spider.startSpider()
    ends = time.time()
    print("程序运行完毕，总用时"+ str(int(ends-starts)/60) +"分钟")
 
if __name__ == '__main__':
    main()