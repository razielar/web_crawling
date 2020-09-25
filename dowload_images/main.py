import os
import json
import requests
from bs4 import BeautifulSoup


google_image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

SAVE_FOLDER= "images"

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()

def download_images():
    data = input('What are you looking for? ')
    n_images = int(input('How many images do you want download? '))

    print('Start searching...')
    searchurl = google_image + 'q=' + data
    response = requests.get(searchurl, headers=usr_agent)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'}, limit=n_images)
    print(results)


    











if __name__ == "__main__":
    main()