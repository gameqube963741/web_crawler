import requests
from bs4 import BeautifulSoup
import os
import json

#建立一個檔案供檔案讀取
resource_path = r'./pttphone'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0' #設定header

headers = {'User-Agent': user_agent} #設定header

cookies = {'over18': '1' }#建立cookies

url = 'https://www.ptt.cc/bbs/MobileComm/index.html'#爬ptt手機板
#進入手機板內標題頁，page讀取xx第幾頁
# 也可參考爬蟲老師04_pttMovieEveryPageArticle的方式讀取page_number = 8296while page_number >= 8293:
page_number = 6509
while page_number >= 0:
    print(url)#列出網址以便清楚步驟
    print('============')#我是分隔號
    print(page_number)
    res = requests.get(url,headers = headers,cookies = cookies)

    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select('div[class="title"] a')

    for u,each_article in enumerate(title):
        try:
            #print(t)
            title_name = each_article.text#套件text可以了解網站標題名稱
            title_url = 'https://www.ptt.cc' + each_article['href']
            #article_url = 'https://www.ptt.cc' + each_article.a['href']
            res_article = requests.get(title_url, headers = headers,cookies = cookies)
            soup_article = BeautifulSoup(res_article.text,'html.parser')
            article_content = soup_article.select('div[id="main-content"]')#讀取網站內容
            #print(article_content)#若不清楚再檢視時可列出來讓自己清楚步驟
            all_article = article_content[0].text#網站內容(去除tag)
            with open(r'%s/phone%s_%s.json' % (resource_path, page_number,u), 'w', encoding='utf-8') as w:
                json.dump(str(all_article), w)
            # with open(r'C:/Users/Big data/Desktop/123.json', 'w', encoding='utf-8-sig') as f:
            #     json.dump(title, f)
            # print(title_name)
            print(title_url)
            print("over")
            #time.sleep(random.randint(2,4))#讓爬蟲隨機睡個2~10秒
        except TypeError  as e:
            print('==========')
            print(title_url)
            print(e.args)
            print('==========')
        except IndexError as e:
            print('==========')
            print(title_url)
            print(e.args)
            print('==========')
        except FileNotFoundError as e:
            print('==========')
            print(title_url)
            print(e.args)
            print('==========')
        except OSError as e:
            print('==========')
            print(title_url)
            print(e.args)
            print('==========')
    page_number -= 1
    last_page_url = soup.select('a[class="btn wide"]')
    print(last_page_url)
    new_url = 'https://www.ptt.cc' +last_page_url[1]['href']
    url = new_url
    print('https://www.ptt.cc' +last_page_url[1]['href'])