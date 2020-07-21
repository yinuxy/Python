import urllib3
from bs4 import BeautifulSoup
import certifi

file = open('../data/word', "w+")
http = urllib3.PoolManager(
     cert_reqs='CERT_REQUIRED',
     ca_certs=certifi.where())

url = 'https://www.oxfordlearnersdictionaries.com/wordlist/english/oxford3000/'
r = http.request('GET', url)

soup = BeautifulSoup(r.data, 'html.parser')

category = soup.find('ul', class_="hide_phone")

content = soup.find('ul', class_="wordlist-oxford3000")

# for link in content.find_all('a'):
#     file.write(link.get_text()+'\n')

pages = soup.find('ul', class_="paging_links")

for cat in category.find_all('a'):
    # get the former category of data
    while pages.find('a', text=">"):
        next = pages.find('a', text=">")
        r = http.request('GET', next.get('href'))
        soup = BeautifulSoup(r.data, 'html.parser')
        pages = soup.find('ul', class_="paging_links")

        # get the former page of data
        for link in content.find_all('a'):
            if link.get_text() != 'o’clock':
                file.write(link.get_text()+'\n')
        # update the content
        content = soup.find('ul', class_="wordlist-oxford3000")
    # get the last page of content
    for link in content.find_all('a'):
        file.write(link.get_text()+'\n')

    r = http.request('GET', cat.get('href'))
    soup = BeautifulSoup(r.data, 'html.parser')

    content = soup.find('ul', class_="wordlist-oxford3000")
    pages = soup.find('ul', class_="paging_links")

# get the last category of data
while pages.find('a', text=">"):
    next = pages.find('a', text=">")
    r = http.request('GET', next.get('href'))
    soup = BeautifulSoup(r.data, 'html.parser')
    pages = soup.find('ul', class_="paging_links")

    # get the former page of data
    for link in content.find_all('a'):
        file.write(link.get_text()+'\n')
    # update the content
    content = soup.find('ul', class_="wordlist-oxford3000")
# get the last page of content
for link in content.find_all('a'):
    file.write(link.get_text()+'\n')






