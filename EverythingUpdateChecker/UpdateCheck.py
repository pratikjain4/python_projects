import requests
from bs4 import BeautifulSoup
import os.path
import urllib.request
import ctypes
import subprocess
import sys


def create_directory():
    try:
        os.mkdir('downloaded_files/')
    except OSError:
        # in case directory already exists, nothing to do !
        pass


def retrieve_html_content():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    base_url = 'https://www.voidtools.com'
    page_url = base_url + "/forum/viewtopic.php?t=9787"

    try:
        req = requests.get(page_url, headers)
    except requests.ConnectionError:
        error_msg = "Error connecting to Everything website over the internet ! "
        print(error_msg)
        ctypes.windll.user32.MessageBoxW(0, error_msg, "Everything", 0)
        sys.exit(1)

    soup = BeautifulSoup(req.content, 'html.parser')

    all_links = soup.find_all('a', href=True)
    download_links = [url['href'] for url in all_links if 'exe' in url['href']]
    if not download_links:
        print("Not able to access the Everything Alpha update forums page ! ")
        sys.exit(1)

    required_link = download_links[0]
    return base_url + required_link


def check_and_download_file(exe_link):
    print("Latest build : " + exe_link)
    filename = exe_link.split('/')[-1]
    file_exists = os.path.isfile('downloaded_files/' + filename)

    if file_exists:
        ctypes.windll.user32.MessageBoxW(0, "Everything is up to date!", "Everything", 0)
        subprocess.Popen("explorer /select," + 'downloaded_files\\' + filename)
    else:
        ctypes.windll.user32.MessageBoxW(0, "New version of Everything found!  Downloading....!", "Everything", 0)
        urllib.request.urlretrieve(exe_link, 'downloaded_files/' + filename)
        subprocess.Popen("explorer /select," + 'downloaded_files\\' + filename)

    # Display Latest file
    print("Latest file   : " + filename)

    # Checking if file exists
    print("File exists?  : " + str(file_exists))


def main():
    create_directory()
    exe_link = retrieve_html_content()
    check_and_download_file(exe_link)


if __name__ == "__main__":
    main()
