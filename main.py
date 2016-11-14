#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as bs

headers = {'User-Agent': 'Chrome/54.0.2840.99'}
serial_params = {'c' : '225', 's' : '3',  'e' : '08'}
cookies = {'uid' : 'uid', 'pass' : 'pass'}

serials = requests.post("http://www.lostfilm.tv/nrdr.php", headers=headers, params=serial_params, cookies=cookies)
serials.encoding = 'cp1251'

with open("content.html", "w", encoding='utf-8') as f:
    f.write(serials.text)

soup = bs(serials.text)
# downloads = soup.findAll('a', {'class' : 'a_download'})
# last_serie = downloads[0]['onclick']
# functions = last_serie.split(';')for i in serial_params.items():
#    print(i)
# target_func = functions[-3]
# print(target_func)

# rsspage = requests.get('http://www.lostfilm.tv/rssdd.xml', headers=headers)
# soup = bs(rsspage.text)
# with open("/home/webserver/LfTVSeriesDownloader/rss_content1.xml", "w", encoding=rsspage.encoding) as f:
# # with open("/home/webserver/LfTVSeriesDownloader/rss_content1.xml", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

print(serials.encoding)

trs = soup.findAll('tr')
links = []
descriptions = []
for tr in trs:
    if tr.find('a') != None:
        links.append(tr.find('a')['href'])
        descriptions.append(tr.find('span').contents[0])

data = list(zip(descriptions, links))

for d in data:
    print (d)

filename = 'Cat'+serial_params['c']+'S'+serial_params['s']+'Ep'+serial_params['e']+'.torrent'
print ('\n'+data[0][1])
r = requests.get(data[0][1], stream=True)
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=1024):
        fd.write(chunk)
