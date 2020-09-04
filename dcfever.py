import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import time
import json
import re

url = 'https://www.dcfever.com/phones/userreviews.php?page=1'
user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
headers={'User-Agent': user_agent}


x=0
for p in range(200):
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.select('div[class="review_entry clear"]')

    for a in article:
        x+=1
        # title
        title = a.select('h2')[0].text
        print(title)

        # author
        author = a.select('div[class="review_info clear"] a')[0].text

        # date
        date = a.select('div[class="line_one"]')[0].text.split('於 ')[1]

        # content
        content = a.select('div[class="review_text"]')[0].text
        a = re.search('優點:', content, flags=0)
        b = re.search('缺點:', content, flags=0)
        c = re.search('意見:', content, flags=0)

        if a is None and b is None and c is None:
            like = ''
            dislike = ''
            comments = ''
        elif a is None and b is None:
            like = ''
            dislike = ''
            comments = content.split('意見:')[1]
        elif a is None and c is None:
            like = ''
            dislike = content.split('缺點:')[1]
            comments = ''
        elif b is None and c is None:
            like = content.split('優點:')[1]
            dislike = ''
            comments = ''
        elif a is None:
            like = ''
            dislike = content.split('缺點:')[1].split('意見:')[0]
            comments = content.split('意見:')[1]
        elif b is None:
            like = content.split('優點:')[1].split('意見:')[0]
            dislike = ''
            comments = content.split('意見:')[1]
        elif c is None:
            like = content.split('優點:')[1].split('缺點:')[0]
            dislike = content.split('缺點:')[1]
            comments = ''
        else:
            like = content.split('優點:')[1].split('缺點:')[0]
            dislike = content.split('缺點:')[1].split('意見:')[0]
            comments =content.split('意見:')[1]

        # dictionary
        dic = {}
        dic['id'] = 'dcfever_userreviews_' + str(x)
        dic['Title'] = title
        dic['Author'] = author
        dic['Date'] = date
        dic['Like'] = like
        dic['Dislike'] = dislike
        dic['Comments'] = comments


        # save to json
        with open(r'C:/Users/Big data/PycharmProjects/project/dcfever/dcfever_userreviews_%s.json' % x, 'w', encoding='utf-8') as json_file:
            json.dump(dic, json_file)
        #time.sleep(3)


    url = 'https://www.dcfever.com/phones/userreviews.php?page=' + str(p+2)
