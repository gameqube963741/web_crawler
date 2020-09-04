from bs4 import BeautifulSoup
import random
import ssl
import pandas as pd
import requests
import re
import json
from lxml import etree
from numpy import save
import os

def save(id, title, article_date, article_content, reply_all):
    df = pd.DataFrame(
        data=[{
            'id': id,
            'title': title,
            'date': article_date,
            'content': article_content,
            'comment': reply_all
        }],
        columns=['id', 'title', 'date', 'content', 'comment'])
    return df
page = 2
url = 'https://forum.gamer.com.tw/B.php?page={}&bsn=60559'.format(page)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
each_article = soup.select("div[class='b-list__tile']")

Joblist = pd.DataFrame()

count = 1
x=0
while True:
    try:
        print(page)

        # 抓列表所有文章
        for article in each_article:
            try:
                snB = []
                reply_all = ''
                Link = 'https://forum.gamer.com.tw/' + article('p')[0]['href']
                title = article('p')[0].text  # 抓取文章標題
                print(Link)
                print(title)

                article_res = requests.get(Link)
                article_res.encoding = 'utf-8'  # 編碼
                article_soup = BeautifulSoup(article_res.text, 'html.parser')
                article_time = article_soup.select("div[class='c-post__header__info']")[0]('a')[0]['data-mtime']
                article_date = article_time.split(' ')[0]


                content = article_soup.select("div[class='c-article__content']")  # 抓內文的標籤
                article_content = content[0].text  # 內文
                print(article_content)
                reply = []  # 儲存留言
                # print(article)
                for article_main in content:

                    if article_main.text in article_content:  # 爬取留言先前內文一樣就pass先前爬過了
                        pass
                    else:
                        reply.append(article_main.text)  # 儲存留言
                json_all = article_soup.select("div[class='old-reply']")

                for json_No in json_all:  # 抓json留言
                    string = str(str(json_No.a['onclick']).split(',')[1])
                    string = (string[:-2]).strip()
                    snB.append(string)

                for i in range(len(snB)):
                    json_Link = 'https://forum.gamer.com.tw/ajax/moreCommend.php?bsn=60559&snB={}&returnHtml=1'.format(
                        snB[i])
                    json_res = requests.get(json_Link)
                    js = (json.loads(str(json_res.text)))['html']
                    for js_soup in js:
                        js_soup = BeautifulSoup(js_soup, 'html.parser')
                        reply_each = js_soup.select("article[class='reply-content__article c-article']")
                        reply.append(reply_each[0].text)  # 抓完json留言
                for i in range(len(reply)):  # 儲存json留言
                    reply_all += reply[i]
                # print(reply_all)

                # 如果要存CSV要以下這兩段
                df = save('baha_{}'.format(count), title, article_date, article_content, reply_all)  # 儲存到表格
                Joblist=Joblist.append(df)

                count += 1  # 計算爬的文章數
            except:
                pass
        page += 1  # 頁數自動＋1
        url = 'https://forum.gamer.com.tw/B.php?page={}&bsn=60559'.format(page)  # 翻頁
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        each_article = soup.select("div[class='b-list__tile']")
    except:
        break

    x+=1
    # time.sleep(3)

# 存成csv
Joblist.to_csv('./baha.csv',encoding='utf-8-sig',index=0)
Joblist=pd.DataFrame()
