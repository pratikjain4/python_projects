import requests
from bs4 import BeautifulSoup
import os.path
import urllib.request
import ctypes
import subprocess

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

try:
    os.mkdir('downloaded_files/')
except OSError:
    pass

base_url = 'https://www.voidtools.com'
page_url = base_url + "/forum/viewtopic.php?t=9787"
req = requests.get(page_url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

all_links = soup.find_all('a', href=True)
download_links = [url['href'] for url in all_links if 'exe' in url['href']]
required_link = download_links[0]
filename = str(required_link).replace('/', '')
file_exists = os.path.isfile('downloaded_files/' + filename)

if file_exists:
    ctypes.windll.user32.MessageBoxW(0, "Everything is up to date!", "Everything", 0)
    subprocess.Popen("explorer /select," + 'downloaded_files\\' + filename)
else:
    ctypes.windll.user32.MessageBoxW(0, "New version of Everything found!  Downloading....!", "Everything", 0)
    urllib.request.urlretrieve(base_url + required_link, 'downloaded_files/' + filename)
    subprocess.Popen("explorer /select," + 'downloaded_files\\' + filename)

# Display Latest file
print("Latest file   : " + filename)

# Checking if file exists
print("File exists?  : " + str(file_exists))
