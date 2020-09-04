import time
from urllib import request
import requests
from bs4 import BeautifulSoup
import os
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

brand = {'HUAWEI': 4546, 'OPPO': 4693, 'Samsung': 4523, 'SONY': 4551, 'Apple': 4544, 'ASUS': 4543}   #建立品牌

for each_brand in brand:
    path = "D:/eprice_json1/{}".format(each_brand)
    if not os.path.isdir(path):
        os.mkdir(path)

for each_brand in brand:

    url = 'https://www.eprice.com.tw/mobile/talk/{}/0/1/'.format(brand[each_brand])
    try:
        res = requests.get(url, headers=headers)
    except:
        res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    max_page = int(soup.select('div[class="pagelink"]')[0].select('a')[-2]['data-value'])  # 最終還是要取最大頁數www
    change_page = soup.select('div[class="pagelink"]')[0].select('a')  # [-1]['herf'])

    n = 0
    for page in range(1, max_page + 1):

        page_url = "https://www.eprice.com.tw/mobile/talk/{}/0/{}/".format(brand[each_brand], page)  # 前面的{}是品牌號碼，後面的是頁碼
        # print(page_url)
        try:
            page_res = requests.get(page_url, headers=headers)
        except:
            try:
                page_res = requests.get(page_url, headers=headers)
            except:
                time.sleep(5)
                page_res = requests.get(page_url, headers=headers)
        page_res.encoding = 'utf-8'
        page_soup = BeautifulSoup(page_res.text, 'html.parser')
        # change_page = page_soup.select('div[class="pagelink"]')[0].select('a')
        title_url = page_soup.select('a[class="title text-wrap"]')  # 在外面取文章標題
        print("第{}頁".format(page))

        for each_url in title_url:  # 文章網頁

            article_dict = {}
            new_url = 'https://www.eprice.com.tw/' + each_url['href']
            try:
                new_res = requests.get(new_url, headers=headers)
            except:
                new_res = requests.get(new_url, headers=headers)

            new_res.encoding = 'utf-8'
            new_soup = BeautifulSoup(new_res.text, 'html.parser')
            try:
                comment_max_page = int(new_soup.select('div[class="pagelink"]')[0].select('a')[-2]['data-value'])
            except:
                comment_max_page = 1
                print('留言頁數只有一頁')

            title = new_soup.select('h1[class="title"]')[0].text
            content = new_soup.select('div[class="user-comment-block"]')[0].text  # 文章
            date = new_soup.select('span[class="date"]')[0].text.split(' ')[1]
            n += 1

            # print(max_page)
            # print(content)
            print(date)
            print(title)
            print()
            article_dict['id'] = 'eprice_{}_{}'.format(each_brand, n)  # 前面大括號設品牌名稱，後面的設編號
            article_dict['標題'] = title
            article_dict['日期'] = date
            article_dict['內文'] = content

            comment = []
            for comment_page in range(1, comment_max_page + 1):  # 留言網頁

                comment_url = new_url[0:-2] + '{}/'.format(comment_page)  # 先去掉url中最後面的兩個字，再補上頁數
                try:
                    comment_res = requests.get(comment_url, headers=headers)
                except:
                    comment_res = requests.get(comment_url, headers=headers)

                comment_res.encoding = 'utf-8'
                comment_soup = BeautifulSoup(comment_res.text, 'html.parser')
                try:
                    first_comment = comment_soup.select('div[class="user-comment-block"]')[1].text.replace('\n','')  # 第一則留言
                    # comment.append({'{}'.format(0):first_comment })
                    comment.append(first_comment)
                except:
                    print('留言錯誤')
                all_comment = comment_soup.select('div[class="comment"]')

                for each_comment in all_comment:  # 第二則以後的留言

                    other_comment = each_comment.text.replace('\n', '').replace('\t', '').replace('\r', '')
                    # comment.append({'{}'.format(i):each_comment.text})
                    comment.append(each_comment.text)

            article_dict['留言'] = comment
            # print(article_dict)

            with open('D:/eprice_json1/{}/{}.json'.format(each_brand, article_dict['id']), 'a', newline='',encoding='utf-8-sig') as jsonfile:
                json.dump(article_dict, jsonfile, ensure_ascii=False)

