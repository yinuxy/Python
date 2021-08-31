import os
import time
import datetime
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from faker import Factory


def get_user_agent(num):
    """
    生成不同的 user-agent
    :param num: 生成个数
    :return: list
    """
    factory = Factory.create()
    user_agent = []
    for i in range(num):
        user_agent.append({'User-Agent': factory.user_agent()})
    return user_agent


def get_proxy(pages, ua_num, target_url):
    """
    爬取代理数据，清洗整合
    :param pages: 需要爬取页数
    :param ua_num: 需要user-agent个数
    :param target_url: 爬虫的目标地址，作为验证代理池ip的有效性
    :return: list
    """
    headers = get_user_agent(ua_num)  # 请求头
    proxy_list = []  # 最后需入库保存的代理池数据
    try:
        for num in range(0, pages):
            print('Start：第 %d 页请求' % (num + 1))
            # 请求路径
            url = 'https://www.kuaidaili.com/free/inha/' + str(num + 1) + '/'

            # 随机延时（randint生成的随机数n: a <= n <= b ；random产生 0 到 1 之间的随机浮点数）
            time.sleep(random.randint(1, 2) + random.random())
            header_i = random.randint(0, len(headers) - 1)  # 随机获取1个请求头

            # BeautifulSoup 解析
            html = requests.get(url, headers=headers[header_i])
            soup = BeautifulSoup(html.text, 'lxml')

            # CSS 选择器
            ip = soup.select("td[data-title='IP']")
            port = soup.select("td[data-title='PORT']")
            degree = soup.select("td[data-title='匿名度']")
            proxy_type = soup.select("td[data-title='类型']")
            position = soup.select("td[data-title='位置']")
            speed = soup.select("td[data-title='响应速度']")
            last_time = soup.select("td[data-title='最后验证时间']")

            # 循环验证是否有效
            for i, p, dg, pt, ps, sp, lt in zip(ip, port, degree, proxy_type, position, speed, last_time):
                ip_port = str(i.get_text()) + ':' + str(p.get_text())
                # 调用验证的方法
                flag = is_useful(ip_port, headers[header_i], target_url)
                if flag:
                    # 拼装字段
                    p_ip = str(i.get_text())
                    p_port = str(p.get_text())
                    p_degree = str(dg.get_text())
                    p_type = str(pt.get_text())
                    p_position = str(ps.get_text()).rsplit(' ', 1)[0]
                    p_operator = str(ps.get_text()).rsplit(' ')[-1]
                    p_speed = str(sp.get_text())
                    p_last_time = str(lt.get_text())

                    proxy_list.append([p_ip, p_port, p_degree, p_type, p_position, p_operator, p_speed, p_last_time])
            print('End：第 %d 页结束！==========================' % (num + 1))

    except Exception as e:
        print('程序 get_proxy 发生错误，Error：', e)

    finally:
        # 调用保存的方法
        write_proxy(proxy_list)

    return proxy_list


def is_useful(ip_port, headers, target_url):
    """
    判断ip是否可用
    :param ip_port: ip+端口号
    :param headers: 随机请求头
    :param target_url: 爬虫的目标地址，作为验证代理池ip的有效性
    :return: bool
    """
    url = target_url    # 验证ip对目标地址的有效性
    proxy_ip = 'http://' + ip_port
    proxies = {'http': proxy_ip}
    flag = True
    try:
        requests.get(url=url, headers=headers, proxies=proxies, timeout=2)
        print("【可用】：" + ip_port)
    except Exception as e:
        print('程序 is_useful 发生错误，Error：', e)
        flag = False
    return flag


def write_proxy(proxy_list):
    """
    将清洗好的列表数据，保存到xlsx文件
    :param proxy_list: 代理池数据列表
    :return: bool
    """
    date_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')    # 当前时间
    flag = True    # 保存成功标志
    print('--- 开始保存 ---')
    try:
        df = pd.DataFrame(proxy_list,
                          columns=['ip', 'port', 'degree', 'type', 'position', 'operator', 'speed', 'last_time'])
        df.to_excel(date_now + '_proxy.xlsx', index=False)
        print('--- 保存成功！---')
    except Exception as e:
        print('--- 保存失败！---：', e)
        flag = False
    return flag


def read_ip():
    """
    读取代理池，返回ip:port列表
    :return: list
    """
    # 最新爬虫数据文件名（列表推导式写法）
    file_name = [f for f in os.listdir("./") if f.split('.')[-1] == 'xlsx'][-1]
    # 读取文件
    proxy_list = pd.read_excel('./' + file_name)
    proxy_list['port'] = proxy_list['port'].astype('str')   # 先将端口号的整型转为字符串
    proxy_list['ip_port'] = proxy_list['ip'].str.cat(proxy_list['port'], sep=':')   # 组合成ip+port
    return list(proxy_list['ip_port'])


def main():
    """
    主方法
    """
    pages = 10   # 定义爬取页数
    ua_num = 3  # 定义需生成user-agent个数
    target_url = 'https://everia.club/'    # 爬虫的目标地址，作为验证代理池ip的有效性
    proxy_list = get_proxy(pages, ua_num, target_url)
    print(proxy_list)


if __name__ == '__main__':
    # 1.主方法
    # main()
    # 2.读取代理池
    print(read_ip())





