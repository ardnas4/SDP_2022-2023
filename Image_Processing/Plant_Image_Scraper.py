import time
from matplotlib.cbook import maxdict

import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def image_links_scraper(link, max_urls=None):
    count_urls = 0
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # initializes driver and installs chromedriver
    driver.get(link) # go to the website 

    image_links = [] # list of links to the images

    current_height = driver.execute_script("return document.body.scrollHeight") # get the starting heigh

    while True: # keep scrolling until we reach the end of the page
        driver.execute_script(f"window.scrollTo({current_height}, document.body.scrollHeight);") # scroll
        elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'cover')]")
        print("Number of elements", len(elements))

        if len(elements) >= max_urls:
            break

        time.sleep(5) # wait for page to load

        new_height = driver.execute_script("return document.body.scrollHeight") # get new height after scroll

        if current_height == new_height: # check if the height has stopped changing
            break # if so, we've maxed out and need to stop
        else:
            current_height = new_height # otherwise, we need to keep scrolling

    #elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'cover')]") # finds all elements where the 'id' tag starts with the string 'cover'
    
    for element in elements:
        s = element.get_attribute('style') # returns the text in the 'style' attribute
        start = 'width: 100%; min-height: 183px; background-size: cover; background-position: center center; background-repeat: no-repeat; background-image: url("' # first part of the useless substring
        end = '");' # second part of the useless substring
        link = s[len(start):-len(end)] # gets the URL in the string
        image_links.append(link) # add the image link to the list
    
    print("Amount of images:", len(image_links))

    return image_links

def download_images(image_links, folder_name, current):
    for link in image_links: # iterate through all the image links
        r = requests.get(link).content # retrieve the image content from URL
        file_name = f'../Dataset/{folder_name}/{current}.jpg' # generate image file name

        with open(file_name, 'wb') as f:
            f.write(r) # save the image
        
        current += 1 # update the image number for the next iteration
    return current

if __name__ == '__main__':
    # poison_oak_link = 'https://www.inaturalist.org/taxa/52083-Toxicodendron-pubescens/browse_photos?photo_license=cc0&layout=grid'
    # poison_ivy_link = 'https://www.inaturalist.org/taxa/58732-Toxicodendron-radicans/browse_photos?photo_license=cc0c&layout=grid'
    # poison_sumac_link = 'https://www.inaturalist.org/taxa/54767-Toxicodendron-vernix/browse_photos?photo_license=cc0&layout=grid'

    # max_urls = 1000
    # current = 1

    # image_links = image_links_scraper(poison_oak_link, max_urls)
    # current = download_images(image_links, "Atlantic_Poison_Oak", current)
    # print("# of images for poison oak:", current)

    # current = 1
    # image_links = image_links_scraper(poison_ivy_link, max_urls)
    # current = download_images(image_links, "Eastern_Poison_Ivy", current)
    # print("# of images for poison ivy:", current)

    # current = 1
    # image_links = image_links_scraper(poison_sumac_link, max_urls)
    # current = download_images(image_links, "Poison_Sumac", current)    
    # print("# of images for poison sumac:", current)
    
    list_link = ['https://www.inaturalist.org/taxa/47726-Acer-negundo/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/410578-Hydrangea-petiolaris/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/54764-Rhus-glabra/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/50278-Parthenocissus-quinquefolia/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/126698-Rhus-copallinum/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/867365-Rhus-trilobata/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/60580-Forsythia/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/130866-Nephrolepis-exaltata/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/291284-Coleus-scutellarioides/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/47603-Taraxacum/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/124826-Dracaena/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/56955-Helianthus/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/76465-Crassula-ovata/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/55406-Petunia/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/162845-Euphorbia-pulcherrima/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/53438-Rosa/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/322492-Chlorophytum-comosum/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/55745-Trifolium-repens/browse_photos?layout=grid',
            'https://www.inaturalist.org/taxa/50298-Fragaria-vesca/browse_photos?layout=grid']

    max_urls = 150
    folder_name = "Not"
    current = 1

    for link in list_link:
        print(link)
        image_links = image_links_scraper(link, max_urls)
        current = download_images(image_links, folder_name, current)