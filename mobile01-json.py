import requests
from bs4 import BeautifulSoup
import os
import csv
from multiprocessing import Pool
import multiprocessing
import time #紀錄總共運行時間
import json


#我最後會把爬蟲做成一個大function，只要這個function吃一組字典，吃進去的字典長得像這樣 {'品牌討論版面的網址':'品牌討論版面的名稱(也就是品牌)'}
def getonecategoryarticles(i):

    #先設定global讓這個function可以吃到我在外面設定的流水號變數 serial_number
    global serial_number

    #設定 headers
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    
    #把字典內的品牌討論網址 存到pageurl變數  (品牌討論網址其實也就是該版面的第一頁)
    pageurl, = i

    #把該品牌的名字存到name
    name, = i.values()
#===================================================================================================================
#把含有非法字元或中文的品牌名稱改成英文
    if name == 'Sony / SE':
        name = 'SonySE'
    
    elif name == '其他作業系統':
        name = 'otherOS'
    
    elif name == '其他智慧型手機':
        name = 'otherPhone'
    else:
        pass
#===================================================================================================================

    #設定一個叫articles的空list，後面我要把這個討論版面的所有文章url都丟進這個list裡面
    articles = []

    #開始爬這個版面的第一頁，也就是我們從字典分隔出的品牌討論版網址
    res = requests.get(pageurl,headers=headers)

    #做成soup物件才能用select選取
    soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')

    #在第一頁下方會有顯示不同頁碼，我們透過這個就可以抓到這個版面總共有多少頁，把這個多少頁的資訊存進pages變數內
    try:
        pages = int(soup.select('a.c-pagination')[-1].text)
    
    #如果出錯就print出來讓我知道一下
    except:
        print('pass :{} cus lake of pages'.format(name))

    #先再當前目錄建立一個用name(版名)命名的directory
    try:
        os.mkdir('./{}'.format(name))

    #建立失敗就印出來提醒我一下
    except:
        print('mkdir error')

    #把所有文章網址變成完整的網址並存到我們先前建的articles內
    articles.extend([ 'https://www.mobile01.com/'+i.get('href') for i in soup.select('div.c-listTableTd__title a.c-link.u-ellipsis')])
    
    #開始判斷這個版面是否有第二頁或以上頁面 ，(透過page參數判斷)
    # 如果該版有超過兩頁，則如下寫入
    if pages >= 2:

        #把所有的article links文章連結丟到articles這個list裡面(如果只有一頁則不會需要下面for迴圈)
        for page in range(2,pages+1):
            print('getting all article links')
            url = pageurl + '&p={}'.format(page)
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')
            articles.extend([ 'https://www.mobile01.com/'+i.get('href') for i in soup.select('div.c-listTableTd__title a.c-link.u-ellipsis')])

        #開始爬取所有articles裡面的文章連結
        for articlelink in articles:
            print('before get_articles function')
            #這裡會執行我自訂的get_articles函數，該函數會抓取articlelink文章連結內所有我需要的資訊，並回傳一個字典檔包含 id,標題,時間,內文,留言 這五個key
            #看到這裡可以先去看下面的get_articles() 是怎麼寫的
            newjson = get_articles(articlelink)
            try:
                filename = newjson['id']
                #有些get_articles失敗會導致標題進入except變成None，這種缺失的資料我不拿
                if 'None' in filename:
                    continue
                else:
                    pass
            except:
                print('boradname = newjson["id"] error')
                # serial_number += 1
                continue
            print('start writing json file')
            #寫入檔案，由於上面我們已經建立過當前版面的目錄(name)，所以我們直接把json檔存在該版面目錄下方，並以filename命名
            with open('./{}/{}.json'.format(name,filename),'a+',newline='',encoding='utf-8-sig') as jsonfile:
                try:
                    print()
                    json.dump(newjson,jsonfile)
                except:
                    print('json-writing error')
                    pass
                #寫入完成後把流水號+=1 , 這樣下一篇文章就會依序命名了
                serial_number += 1
            print('writing json file complete!')
            
        
        print(name,'已下載完成')
    
    
    else:
        #我們在上面就已經把討論版第一頁的所有網址加到articles這個list裡面了
        #所以如果該版沒有兩頁以上，則直接開始爬取所有articles內的文章連結
        for articlelink in articles:
            print('before get_articles fumction 2')
            #這裡會執行我自訂的get_articles函數，該函數會抓取articlelink文章連結內所有我需要的資訊，並回傳一個字典檔包含 id,標題,時間,內文,留言 這五個key
            #看到這裡可以先去看下面的get_articles() 是怎麼寫的
            newjson = get_articles(articlelink)
            try:
                filename = newjson['id']

                #有些get_articles失敗會導致標題進入except變成None，這種缺失的資料我不拿
                if 'None' in filename:
                    continue
                else:
                    pass
            except:
                print('boradname = newjson["id"] error')
                # serial_number += 1
                continue
            
            print('start writing json file2')
            with open('./{}/{}.json'.format(name,filename),'a+',newline='',encoding='utf-8-sig') as jsonfile:
                try:
                    json.dump(newjson,jsonfile)
                except:
                    print('json-writing error')
                    pass
                serial_number += 1
        
        print(name,'已下載完成')


def get_articles(alink):
    try:
        print('in get_article function')
        global serial_number
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        replylist = []
        res = requests.get(alink,headers=headers)
        print('article頁面成功爬取')
        soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')

        try:
            filename = soup.select('li.c-breadCrumb__item a.c-link')[-1].text.strip()
            filename = 'mobile01_{}_{}'.format(filename,serial_number)
#============================================================================================
#處理中文與非法字元轉換成英文作為json檔名
            if 'Sony / SE' in filename:
                filename = filename.replace('Sony / SE','SonySE')
                print('改過filename :',filename)

            elif '其他作業系統' in filename:
                filename = filename.replace('其他作業系統','otherOS')
                print('改過filename :',filename)

            elif '其他智慧型手機' in filename:
                filename = filename.replace('其他智慧型手機','otherPhone')
                print('改過filename :',filename)
            else:
                pass
#=============================================================================================
            print(filename)
        except:
            filename = 'None'
        try:
            title = soup.select('.t2')[0].text.strip()
            print(title)
        except:
            title = 'None'
        try:
            posttime = soup.select('li.l-toolBar__item span.o-fNotes.o-fSubMini')[0].text
            print(posttime)
        except:
            posttime = 'None'
        try:
            content = soup.select('article.l-publishArea.topic_article div')[0].text.strip()
        except:
            content = 'None'
        #把第一頁的評論加到replylist內,並且計算還有多少頁留言
        try:
            replylist.extend([i.text.strip() for i in soup.select('article.u-gapBottom--max.c-articleLimit')])
        except:
            pass


        #把留言共多少頁抓到page內
        page = len(soup.select('.c-pagination'))

        #有時候留言部分會超過兩頁以上
        #這個判斷就是要把其他頁的留言也加入replylist
        if page >= 2:
            for time in range(page):
                replylink = alink + '&p=' + str(time)
                res = requests.get(replylink,headers=headers)
                soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')
                replylist.extend([i.text.strip() for i in soup.select('article.u-gapBottom--max.c-articleLimit')])
            #加入完畢後就回傳這篇文章的資訊(以字典格式回傳)
            return {
                'id':filename,
                '標題':title,
                '日期':posttime,
                '內文':content,
                '留言':replylist
                }
        else:
            #如果沒有其他頁留言就直接回傳這篇文章的資訊(以字典格式回傳)
            return {
                'id':filename,
                '標題':title,
                '日期':posttime,
                '內文':content,
                '留言':replylist
                }
    except:
        print('article_function error occur')
        pass

#上面是定義兩個函式，這裡開始運行程式
if __name__ == "__main__":

    #記錄開始執行程式的時間
    starttime = time.time()
    

    #這裡就是在撈所有的 {'討論版網址':'討論版名稱'}
    original_link = 'https://www.mobile01.com/forumlist.php?f=16'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    res = requests.get(original_link,headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')
    
    #設定流水號的初始值
    serial_number = 1
    
    #把所有的{'討論版網址':'討論版名稱'}都放到一個list內
    linksandnames = [ {'https://www.mobile01.com/'+i.get('href'):i.text} for i in soup.select('div.c-listTableTd__title a.c-link')]

    # #檢查用:  如有需要查找，則用此for迴圈列印index對應表單
    # for num , dic in enumerate(linksandnames):
    #     print(num,dic)

    #把我這次要的分類看板都放進list內 以下是我要抓的版面
    download_list = [linksandnames[1],linksandnames[6],linksandnames[11],linksandnames[12],linksandnames[14],linksandnames[43],linksandnames[44]]


    #開始下載download_list
    for dic in download_list:
        #每次抓一整個版面的所有文章寫入json檔
        getonecategoryarticles(dic)
        #一個版抓完之後，把流水號重新設定從一開始，這樣下一個版的檔案名稱流水號才會再從1開始命名
        serial_number = 1

    
    # #檢查用:  確認一下最終要下載的清單是否有錯
    # print(download_list)

    #運行結束後告訴我總共運行了多久時間
    print('Total time: {} 分鐘'.format( (time.time()-starttime)/60 ) )