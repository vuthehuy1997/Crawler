# Reference this link to setup and run selenium
# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25#:~:text=The%20combination%20of%20Beautiful%20Soup,be%20extracted%20by%20Beautiful%20Soup.

#Som time downloader can fail, when you want re download 1 name, you need delete this txt and folder for this name in save_root

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import random
# from multiprocessing import Process
import urllib.request

import io

from PIL import Image  # https://pillow.readthedocs.io/en/4.3.x/
import requests  # http://docs.python-requests.org/en/master/

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.convert('RGB').save(image_file_path)

def random_sleep(start, end):
    time_sleep = random.uniform(start, end)
    time.sleep(time_sleep)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
# driver = webdriver.Chrome("./chromedriver_linux64/chromedriver", options=options)

import time
import csv
save_root = './don_thuoc/raw'
save_links_root = './don_thuoc/link_images'
if not os.path.exists(save_root):
    os.mkdir(save_root)
if not os.path.exists(save_links_root):
    os.mkdir(save_links_root)

# url_list = ['https://www.facebook.com/groups/490875888472866/media']
# url_list = ['https://www.facebook.com/groups/ototai/media']
url_list = ['https://www.facebook.com/groups/googledonthuoc/media']

total_name = len(url_list)
line_count = 0
for idx, url in enumerate(url_list):
    name = 'don_thuoc'
    print('name: ',name)
    # print(' {} ; {}; {}; {} '.format(row[0], row[1], row[2], row[3]))
    save_path = os.path.join(save_root, name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_links_path = os.path.join(save_links_root, name)
    if not os.path.exists(save_links_path):
        os.makedirs(save_links_path)
    
    out_put = os.path.join(save_links_path, name +'.txt')
    if os.path.exists(out_put):
        print('exists {}'.format(out_put))
        continue
    driver = webdriver.Chrome(executable_path=r'chromedriver_linux64/chromedriver', options=options)
    index = 2
    driver.get(url)
    random_sleep(1, 3)
    items = driver.find_elements_by_tag_name("img")
    actions = ActionChains(driver)
    list_file = []
    while True:
        if index > 10000:
            break
        print('{} / {} name {}, index: {}'.format(idx+1, total_name, name, index))
        print('len(items): ',len(items))
        fail = False
        if len(items) < index+1:
            count=0
            while True:
                if count > 10:
                    fail = True
                    break
                print('error: idx', count)
                # driver.get(url)
                actions.send_keys(Keys.END)
                actions.perform()
                actions.send_keys(Keys.END)
                actions.perform()
                actions.send_keys(Keys.END)
                actions.perform()
                random_sleep(1, 3)
                items = driver.find_elements_by_tag_name("img")
                random_sleep(1, 3)
                if len(items) >= index+1:
                    break
                count+=1
            # continue
        # items[index].click()
        if fail:
            break
        driver.execute_script("arguments[0].click();", items[index])
        random_sleep(2, 3)
        
        print('current_url: ',driver.current_url)
        page_source = driver.page_source
        # print('page_source: ',page_source)
        soup = BeautifulSoup(page_source, 'lxml')
        reviews = []

        window = soup.find_all('div', role='main')

        print('window len: ',len(window))
        if len(window) == 0:
            continue
        if len(window) <3:
            reviews_selector = window[0]
            print('reviews_selector len: ',len(reviews_selector))
            file_url = reviews_selector.find_all('img')[0]['src']
        else:
            reviews_selector = window[1]
            print('reviews_selector len: ',len(reviews_selector))
            file_url = reviews_selector.find_all('img')[0]['src']
        print(file_url)
        # exit()
        # f.write(file_url + '\n')
        list_file.append(file_url)
        try:
            # urllib.request.urlretrieve(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            print('save path: ', os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            download_image(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
        
        except:
            print('cannot download')
        index += 1
        driver.back()
        random_sleep(1, 3)
    driver.close()

    file_name = open(out_put, 'w')
    for i in list_file:
        file_name.write(i+'\n')
    file_name.close
    print('Number: ',count)
