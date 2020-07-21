    # -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 21:22:58 2020

@author: Yinux
"""

from selenium import webdriver
import time
import datetime
chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  #chromedriver的文件位置
browser = webdriver.Chrome(executable_path = chrome_driver)
 
def login(name ,pwd):
    browser.get( 'https://account.xiaomi.com/')#登录网址
    time.sleep(2)
    browser.find_element_by_id("username").send_keys(name) #利用账号标签的ID，确定位置并send信息
    browser.find_element_by_id("pwd").send_keys(pwd) #利用密码标签的ID，确定位置并send信息
    browser.find_element_by_id("login-button").click()#利用登录按钮的ID，确定位置并点击
    #如果找不到标签ID，可以使用其他方法来确定元素位置
    time.sleep(3)
    browser.get("https://s1.mi.com/m/app/hd/index.html?id=15042")#切换到秒杀页面
    print('登录成功，正在等待秒杀···')
 
def buy_on_time():
    while True: #不断刷新时钟
        now = datetime.datetime.now()
        if now.strftime('%H:%M:%S') == '09:00:00' or now.strftime('%H:%M:%S') == '11:00:00' or now.strftime('%H:%M:%S') == '15:00:00' or now.strftime('%H:%M:%S') == '17:00:00':
#        if now.strftime('%H:%M:%S') == buytime:
            browser.find_element_by_xpath("//div[@class='content-box flex-box']/a[@data-log_code='logcode#activity_code=wjsncc49&page=activity&page_id=15042&bid=3645414.0']/div/img").click()
            browser.find_element_by_xpath("//a[@data-log_code='logcode#activity_code=1i19jyzh&page=activity&page_id=15042&bid=3645414.0']").click()
#            browser.find_element_by_xpath("//a[@data-log_code='logcode#activity_code=tudhbjjy&page=activity&page_id=15042&bid=3646017.0']").click() #购买按钮的Xpath
#            browser.find_element_by_xpath("//a[@data-log_code='logcode#activity_code=qpohzak0&page=activity&page_id=15042&bid=3646017.0']").click()
            print('当前时段已抢购完毕')
        time.sleep(0.01)#注意刷新间隔时间要尽量短
 
login('1317150488' , 'xiaomi0711')
#time.sleep(10)
#buy_on_time()#指定秒杀时间，并且开始等待秒杀
browser.find_element_by_class_name('item flex-box-item')[2].click()
#print("ending")