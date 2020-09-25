### Dowload images programatically
### Sep 25th 2020
import os
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
    data= input('What are you looking for in Google? ')
    n_images= int(input('How many images do you want download? '))

    print('Start searching...')
    searchurl= google_image + 'q=' + data
    response= requests.get(searchurl, headers=usr_agent) #without headers crash
    html= response.text
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})
        
    count= 0
    links= []
    for i in results:
        try:
            link= i['data-src'] #data-src structure
            links.append(link)
            count += 1
            if (count >= n_images): break

        except KeyError:
            continue

    print("Dowloading {0} images:".format(len(links)))

    #for i,j in enumerate(links):
        #print("{0}: {1}".format(i+1, j))
    
    print("Start dowloading...")

    for i,j in enumerate(links):
        response= requests.get(j)
        imagename= SAVE_FOLDER + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print("Done")

if __name__ == "__main__":
    main()

