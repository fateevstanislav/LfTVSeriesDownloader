#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as bs
import subprocess
import os

headers = {'User-Agent': 'Chrome/54.0.2840.99'}
# c=242&s=2.00&e=05
# serial_params = {'c' : '225', 's' : '3',  'e' : '08'}
serial_params = {'c': '242', 's': '2.00',  'e': '05'}
cookies = {'uid': 'uid', 'pass': 'pass'}

serials = requests.post("http://www.lostfilm.tv/nrdr.php", headers=headers, params=serial_params, cookies=cookies)
serials.encoding = 'cp1251'

with open("content1.html", "w", encoding='utf-8') as f:
    f.write(serials.text)

soup = bs(serials.text)

# print(serials.encoding)

trs = soup.findAll('tr')
links = []
descriptions = []
for tr in trs:
    if tr.find('a') is not None:
        links.append(tr.find('a')['href'])
        descriptions.append(tr.find('span').contents[0])

data = list(zip(descriptions, links))

for d in data:
    print(d)

filename = 'Cat'+serial_params['c']+'S'+serial_params['s']+'Ep'+serial_params['e']+'.torrent'
print('\n'+data[0][1])
r = requests.get(data[0][1], stream=True)
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=1024):
        fd.write(chunk)

# add .torrent file to uTorrent (Windows)
directory = 'C:\\Users\\Стас\\Downloads'
uTorrent = os.getenv('APPDATA') + '\\uTorrent\\uTorrent.exe'
filename = os.path.abspath(filename)
subprocess.call([uTorrent, '/DIRECTORY', directory, filename])
os.remove(filename)