import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait



url = 'https://cloud.tencent.com/developer'

# 初始化
def init():
    # 定义为全局变量，方便其他模块使用
    global browser, wait
    # 实例化一个chrome浏览器
    option = webdriver.ChromeOptions()
    # option.add_argument("--user-data-dir=" + r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")
    # proxy = get_ip()['HTTP']
    # option.add_argument("--proxy-server=http://54.255.66.81:80")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(chrome_options=option)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)
    # 设置等待超时
    wait = WebDriverWait(browser, 20)

# 登录
def login():
    # 打开登录页面
    browser.get(url)
    # # 获取用户名输入框
    browser.find_element_by_xpath('//*[@id="react-root"]/div[1]/div[1]/div/div[2]/div[2]/div[3]/a[1]').click()
    browser.find_element_by_class_name('clg-icon-qq').click()
    time.sleep(10)

    # 获取cookie
    get_cookies_js = "return document.cookie"
    cookie = browser.execute_script(get_cookies_js)
    print(cookie)

    with open("./cookie.txt", "w", encoding="utf-8") as f:
        f.write(cookie)
    # page_source = browser.page_source
    # with open("page.html","w",encoding="utf-8") as f:
    #     f.write(page_source)


if __name__ == '__main__':
    init()
    login()
