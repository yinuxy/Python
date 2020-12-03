import os
import requests
from lxml import etree
import img2pdf
 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
url = input('请输入云展网图集网址：')
splurl = url.split('/')            #分割网址，准备下面判断
if 'index.html' not in splurl:                #判断是那一种链接
    res = requests.get(url , headers=headers)  #获取源码
    res.encoding = res.apparent_encoding
    xml = etree.HTML(res.text).xpath('//div[@class="show-book-title"]/a/@href')[0].split('/')  #取得book.yunzhan365.con网址进行分割
    purl = xml[2] + '/' + xml[3] + '/' + xml[4] + '/files/' + 'mobile/'                            #构造图片下载网址前缀
    pathname = etree.HTML(res.text).xpath('//div[@class="show-book-title"]/a/text()')      #获取名称
else:
    res = requests.get(url , headers=headers)  #获取源码    
    res.encoding = res.apparent_encoding
    pathname = etree.HTML(res.text).xpath('/html/head/title/text()')      #获取名称
    purl = splurl[2] + '/' + splurl[3] + '/' + splurl[4] + '/files/' + 'mobile/'    #构造图片前缀
 
path = './'                               #存储路径
if not os.path.exists(path):               
    os.makedirs(path)                       #如果路径不存在就创建 
m = 0      #定义图片名称变量
imgs = []       #准备空列表放置图片内容
with open(path + '/' + str(pathname[0]) + '.pdf' , 'wb') as f:       #创建并打开一个pdf文件，准备写入
    while True:         #死循环获取并写入图片
        m += 1      #名称变量
        surl1 = 'http://' + purl + str(m) +'.jpg'          #构造图片链接
        picurl = requests.get(surl1)       #获取图片内容
        if picurl.status_code == 200:       #判断下 如果图片存在就写入列表
            imgs.append(picurl.content)
        else:  
            f.write(img2pdf.convert(imgs))         #把列表中所有的图片内容 写入pdf
            print(f'采集完毕！一共采集了{m -1}张,生成的pdf是{path}目录下【{pathname[0]}.pdf】') 
            break       #中止循环！