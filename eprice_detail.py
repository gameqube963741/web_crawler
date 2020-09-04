import requests
from bs4 import BeautifulSoup
import lxml
import xml.etree.ElementTree as ET
import json
import os
import time
import random

#設定所有我們想要爬取的手機品牌
brand_list = ['Apple','ASUS','HUAWEI','OPPO','Samsung','SONY']


#把所有程式做成一個function，只需要丟入一個包含所有我們想爬品牌的字典，就可以自動爬取所有資訊
def get_all_jsons(brand_list):

    #brand_list內是所有我們要的品牌，每個品牌分別往下去跑迴圈
    for brand in brand_list:

        #初始網址，要先用session物件進去得取所需cookies
        url = 'https://www.eprice.com.tw/mobile/compare/'

        #設定headers
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

        #建立一個requests.sesison物件，用session的方式爬網
        session = requests.session()

        #抓首頁cookies
        res = session.get(url,headers=headers)

        #進到真正會丟出清單的請求網址 (複寫原本url)
        url = 'https://www.eprice.com.tw/ajax/compare/get_prod_of_manu.php'

        #傳送data={'lib':'mobile','manu':'品牌'} , 讓它回傳所有該品牌手機型號的html標籤網址,從中可以提取出我們要的id號碼 (複寫res)
        res = session.post(url,data={'lib':'mobile','manu':'{}'.format(brand)})
        # print('品牌sessionq爬取完成')#debug用

        #做成soup可以用select選擇標籤，以res.content.decode('utf-8-sig')的方式轉換編碼避免中文亂碼
        soup = BeautifulSoup(res.content.decode('utf-8-sig'),'html.parser')

        #選擇標籤
        id_list = soup.select("a[data-value]")

        #清洗每個標籤，只取我要的id號碼
        id_list = [i.get('data-value') for i in id_list]

        #得到新的網址，這個網址會根據我們傳送的id回傳產品細節資料
        url = 'https://www.eprice.com.tw/ajax/compare/mobile/get_prod_detail.php'

        #建立品牌目錄
        try:
            os.mkdir('./{}'.format(brand))
            # print('建立品牌目錄完成')#debug用

        except:
            pass
        
        #把我們抓到的所有該品牌旗下的所有手機id都丟進去跑迴圈，每個迴圈最後會直接寫出該手機規格的json檔存進品牌目錄中
        for id in id_list:

            #用上面的請求網址丟入id,取得該id手機的詳細資料xml網頁編碼
            res = session.post(url,data={'lib':'mobile','prod_id':'{}'.format(id)})
            #print('session設定完成')#debug用

            #把抓下來的xml網頁文字檔存成編碼正確的string
            detail_xml = res.content.decode('utf-8-sig')

            #把string轉換成element 的root物件，該物件可以用類似list中的list的方式去查找每個元素
            root = ET.fromstring(detail_xml)

            #第一個元素是用xml格式內嵌釀html標籤來表示，所以我將該標籤再丟入bs4的物件並使用html.parser讓我直接選出裡面的title
            name = BeautifulSoup(root[2][0].text,'html.parser')

            #如上所述，把title存進name內
            try:
                name = name.select('a')[0].get('title')
            except:
                name = 'None'
            
            #建立一個空字典準備存取
            my_json = dict()

            #把剛剛的名子跟其他剩餘的詳細資料寫進去my_json字典內
            for child in root[2][1:]:
                # print('寫入字典')#debug用
                my_json['name'] = name
                my_json[child.attrib['id']] = child.text

            #開始把my_json寫入json檔內，而且把命名做好
            with open('./{}/eprice_{}_{}.json'.format(brand,brand,id),'a+',encoding='utf-8-sig') as f:
                json.dump(my_json,f)
            # print('寫入json')#debug用

            #抓完之後重設url，把新的型號id帶入下一次迴圈
            url = 'https://www.eprice.com.tw/ajax/compare/mobile/get_prod_detail.php'

            #怕爬太快被擋ip，所以保守一點每次爬完一個json檔sleep個1-5秒

            # time.sleep(random.randint(1,5))

#開始運行程式
get_all_jsons(brand_list)