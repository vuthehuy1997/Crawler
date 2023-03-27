from selenium import webdriver
from bs4 import BeautifulSoup
import os
from multiprocessing import Process
import urllib.request

import io

from PIL import Image  # https://pillow.readthedocs.io/en/4.3.x/
import requests  # http://docs.python-requests.org/en/master/

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

import time

my_file = open('key.txt','r')
list_name = my_file.readlines()
list_name_celeb = [line.replace('\n','') for line in list_name]
save_root = './img_url'
if not os.path.exists(save_root):
    os.mkdir(save_root)

for name in list_name_celeb:
# def get_file_url(name):
    save_path = os.path.join(save_root, name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_root, name) + '.txt'
    if os.path.exists(save_file):
        continue
    f = open(save_file, 'w')
    driver = webdriver.Chrome("./chromedriver_linux64/chromedriver", options=options)
    url = 'https://www.google.com/search?q='+name.replace(' ', '+')+'&client=ubuntu&hl=en&source=lnms&tbm=isch&sa=X'
    # url = 'https://www.google.com/search?q=miu+lê&client=ubuntu&hl=en&source=lnms&tbm=isch&sa=X'
    index = 0
    driver.get(url)
    items = driver.find_elements_by_class_name("rg_i")
    while True:
        if index > 1000:
            break
        print('index: ',index)
        print('len(items): ',len(items))
        if len(items) < index+1:
            driver.switch_to_window(driver.window_handles[-1])
            url = driver.current_url
            driver.get(url)
            time.sleep(1.5)
            items = driver.find_elements_by_class_name("rg_i")
            time.sleep(0.5)
            print('index: ',index)
            print('len(items): ',len(items))
            if len(items) < index+1:
                break
        # if items[index].is_displayed():
        try:
            driver.execute_script("arguments[0].click();", items[index])
        except:
            driver.switch_to_window(driver.window_handles[-1])
            url = driver.current_url
            driver.get(url)
            time.sleep(1.5)
            items = driver.find_elements_by_class_name("rg_i")
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", items[index])
            # continue
        # items[index].click()
        time.sleep(1.5)
        
        print('url: ',url)
        page_source = driver.page_source
        # print('page_source: ',page_source)
        soup = BeautifulSoup(page_source, 'lxml')
        reviews = []
        
        reviews_selector = soup.find_all('div', class_='WaWKOe')
        print('len of reviews_selector: ', len(reviews_selector))
        
        reviews_selector = reviews_selector[0].find_all('img', class_='n3VNCb')
        print('reviews_selector len: ',len(reviews_selector))
        if len(reviews_selector) == 0:
            continue
        if len(reviews_selector) <3:
            file_url = reviews_selector[0]['src']
            # print(reviews_selector[0]['src'])
            # f.write(reviews_selector[0]['src'] + '\n')
        else:
            file_url = reviews_selector[1]['src']
        print(file_url)
        f.write(file_url + '\n')
        try:
            # urllib.request.urlretrieve(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            download_image(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            print('')
        except:
            print('cannot download')
        index += 1
    f.write('Done\n')
    f.close()
    exit()
