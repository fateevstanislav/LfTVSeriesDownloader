#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as bs
import subprocess
import os
import json
import sys


def get_link_torrentfile(cat_num, season, episode, quality):
    headers = {'User-Agent': 'Chrome/54.0.2840.99'}
    serial_params = {'c': cat_num, 's': season,  'e': episode}
    # you should get cookies from web-browser and manually write it here
    cookies = {'uid': 'uid', 'pass': 'pass'}
    serial = requests.post("http://www.lostfilm.tv/nrdr.php", headers=headers, params=serial_params, cookies=cookies)
    serial.encoding = 'cp1251'
    soup = bs(serial.text, "html.parser")
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


def exists_new_episode(cat_num, season, episode):
    headers = {'User-Agent': 'Chrome/54.0.2840.99'}
    serial_params = {'cat': cat_num}
    cookies = {'uid': 'uid', 'pass': 'pass'}
    serials = requests.post("http://www.lostfilm.tv/browse.php", headers=headers, params=serial_params, cookies=cookies)
    soup = bs(serials.text, 'html5lib')
    soup = soup.find('div', {'class': 'mid'})
    # content[0] contains info about serial and seasons starts from content[1]
    cur_season = soup.findAll('div', {'class': 'content'})[1].div.h2.text.split()[0]
    # if users season less then current season on the site, it's obvious there are new series
    if season < cur_season:
        return True
    else:
        cur_episode = soup.find('td', {'class': 't_episode_num'}).text.split()[0]
        return int(cur_episode) > int(episode)


if __name__ == '__main__':
    # now json file should be written manually
    with open('config.json') as f:
        config = json.load(f)

    serial = config['TVseries'][0]

    if sys.platform == 'win32':
        for serial in config['TVseries']:
            link = get_link_torrentfile(serial['cat_num'], serial['season'], serial['episode'], serial['quality'])
            download(link, serial['directory'])
    elif sys.platform == 'linux':
        pass