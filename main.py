#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as bs
import subprocess
import os
import json

def get_link(cat_num, season, episode, quality):
    headers = {'User-Agent': 'Chrome/54.0.2840.99'}
    serial_params = {'c': cat_num, 's': season,  'e': episode}
    # you should get cookies from web-browser and manually write it here
    cookies = {'uid': 'uid', 'pass': 'pass'}
    serials = requests.post("http://www.lostfilm.tv/nrdr.php", headers=headers, params=serial_params, cookies=cookies)
    serials.encoding = 'cp1251'
    soup = bs(serials.text, "html.parser")
    trs = soup.findAll('tr')
    links = []
    for tr in trs:
        if tr.find('a') is not None:
            links.append(tr.find('a')['href'])
    return links[int(quality)]

def download(link, directory):
    filename = 'temp_file_dwnld.torrent'
    r = requests.get(link, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    uTorrent = os.getenv('APPDATA') + '\\uTorrent\\uTorrent.exe'
    filename = os.path.abspath(filename)
    subprocess.call([uTorrent, '/DIRECTORY', directory, filename])
    os.remove(filename)

# now json file should be writed manulally
with open('config.json') as f:
    config = json.load(f)

for serial in config['TVseries']:
    link = get_link(serial['cat_num'], serial['season'], serial['episode'], serial['quality'])
    download(link, serial['directory'])