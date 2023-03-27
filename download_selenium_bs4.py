# Reference this link to setup and run selenium
# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25#:~:text=The%20combination%20of%20Beautiful%20Soup,be%20extracted%20by%20Beautiful%20Soup.

#Som time downloader can fail, when you want re download 1 name, you need delete this txt and folder for this name in save_root

from selenium import webdriver
from bs4 import BeautifulSoup
import os
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

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# driver = webdriver.Chrome("./chromedriver_linux64/chromedriver", options=options)

import time
import csv
save_root = './crawl/raw'
save_links_root = './crawl/link_images'
if not os.path.exists(save_root):
    os.mkdir(save_root)
if not os.path.exists(save_links_root):
    os.mkdir(save_links_root)

data_list = ['Giấy đăng ký doanh nghiệp',
            'Giấy chứng nhận doanh nghiệp',
            'Giấy chứng nhận đăng ký doanh nghiệp công ty cổ phần', 
            'Giấy chứng nhận đăng ký doanh nghiệp công ty hợp danh', 
            'Giấy chứng nhận đăng ký doanh nghiệp công ty TNHH hai thành viên trở lên', 
            'Giấy chứng nhận đăng ký doanh nghiệp công ty TNHH một thành viên',
            'Giấy chứng nhận đăng ký doanh nghiệp tư nhân']
# with open('category_son2.txt', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter=';')
#     for row in csv_reader:
#         data_list.append([row['cat1'], row['cat2'], row['cat3'], row['keyword']])

total_name = len(data_list)
line_count = 0
for idx, name in enumerate(data_list):
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
    # name = 'Ca sĩ ' + name
    driver = webdriver.Chrome(executable_path=r'chromedriver_linux64/chromedriver', options=options)
    url = 'https://www.google.com/search?q='+name.replace(' ', '+')+'&client=ubuntu&hl=en&source=lnms&tbm=isch&sa=X'
    index = 0
    driver.get(url)
    items = driver.find_elements_by_class_name("rg_i")
    list_file = []
    while True:
        if index > 2000:
            break
        print('{} / {} name {}, index: {}'.format(idx+1, total_name, name, index))
        print('len(items): ',len(items))
        fail = False
        if len(items) < index+1:
            try:
                driver.switch_to_window(driver.window_handles[-1])
                url = driver.current_url
                driver.get(url)
                time.sleep(2)
                items = driver.find_elements_by_class_name("rg_i")
                time.sleep(2)
                print('index: ',index)
                print('len(items): ',len(items))
                if len(items) < index+1:
                    fail = True
                    break
            except Exception as e:
                print('error in 1: ', e)
                fail = True
                break
        # if items[index].is_displayed():
        count=0
        while True:
            if count > 10:
                fail = True
                break
            try:
                driver.execute_script("arguments[0].click();", items[index])
                break
            except Exception as e:
                print('error: ', e)
                driver.switch_to_window(driver.window_handles[-1])
                url = driver.current_url
                driver.get(url)
                time.sleep(2)
                items = driver.find_elements_by_class_name("rg_i")
                time.sleep(2)
                # driver.execute_script("arguments[0].click();", items[index])
                count+=1
            # continue
        # items[index].click()
        if fail:
            break
        time.sleep(2)
        
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
        # f.write(file_url + '\n')
        list_file.append(file_url)
        try:
            # urllib.request.urlretrieve(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            print('save path: ', os.path.join(save_path, str(index).zfill(6)) + ".jpg")
            download_image(file_url, os.path.join(save_path, str(index).zfill(6)) + ".jpg")
        
        except:
            print('cannot download')
        index += 1
    driver.close()

    file_name = open(out_put, 'w')
    for i in list_file:
        file_name.write(i+'\n')
    file_name.close
    print('Number: ',count)
