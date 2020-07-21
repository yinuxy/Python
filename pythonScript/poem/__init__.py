import urllib3
from bs4 import BeautifulSoup
import certifi

file = open('../data/poem.txt', "wb+")
http = urllib3.PoolManager(
     cert_reqs='CERT_REQUIRED',
     ca_certs=certifi.where())

for poemId in range(1109, 2010):
    print(poemId)
    url = 'http://www.gushiwen.org/wen_'+str(poemId)+'.aspx'
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    content = soup.find('div', class_="contson")
    file.write(content.get_text().encode('utf-8'))
