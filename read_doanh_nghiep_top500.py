from bs4 import BeautifulSoup
import requests
import os
import json

def get_soup(url,header):
    req = requests.get(url, header)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }


count = 0
url = 'https://vnr500.com.vn/Charts/Index?chartId=2'
# while True:
items = []

soup = get_soup(url,header)
# print(soup)
# content = soup.find("div",{"class":"dataTables_wrapper"})
# print(content)
for row in soup.find_all("tr",{"class":"row_tr"}):
    print(count)
    item = {
        'ten': '',
        'ceo': '',
        'mst': '',
        'nganh': '',
        'dia_chi': '',
        'tel': '',
        'fax': '',
        'mail': '',
        'web': '',
        'nam': ''
    }
    # print(a.text)
    span = row.find("span",{"class":"name_1"})
    a = span.find("a")
    item['ten'] = a.text
    
    tmp = row.find("div",{"class":"row"})
    infors = tmp.find_all("span")
    # print('infors: ', infors)
    item['ceo'] = infors[0].find_all("span")[0].text
    item['mst'] = infors[0].find_all("span")[1].text
    item['nganh'] = infors[3].find_all("span")[0].text
    # for infor in infors:
    #     # print('infor: ', infor)
    #     content = infor.find_all("span")
    #     for i in content:
    #         print(i.text)
    # print(item)
    #read item
    item_url = 'https://vnr500.com.vn/' + a['href']
    item_soup = get_soup(item_url,header)
    rows = item_soup.find("div", {"class":"more_info"}).find_all("tr")
    # print(len(rows))
    # mst = row
    item['dia_chi'] = rows[3].find_all("td")[1].text
    item['tel'] = rows[4].find_all("td")[1].text
    item['fax'] = rows[5].find_all("td")[1].text
    item['mail'] = rows[6].find_all("td")[1].text
    item['web'] = rows[7].find_all("td")[1].text
    item['nam'] = rows[8].find_all("td")[1].text
    # file_name.write(a.text+'\n')
    # print(item)
    items.append(item)
    count+=1
    # exit()

print('Number: ',count)
list_values = {}
for key in items[0]:
    
    for row in items:
        value = ' '.join(row[key].split())
        value = value.replace('\n', '')
        if not key in list_values:
            list_values[key] = [value]
        else:
            list_values[key].append(value)

for key in list_values:
    file_name = open('top500_{}.txt'.format(key), 'w')
    for value in set(list_values[key]):
        file_name.write(value+'\n')
    file_name.close
    