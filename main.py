import requests

headers = {'User-Agent': 'Chrome/39.0.2171.95'}

serial_params = {'cat' : '225' }

serials = requests.get("http://www.lostfilm.tv/browse.php", headers=headers, params=serial_params)

# a_download
with open("content.html", "w", encoding=serials.encoding) as f:
    f.write(serials.text)