import os
import json

#讀取asus手機機型字典 (trello上 欣倫的字典檔)
with open('asus.txt','r',encoding='utf-8-sig',) as f:
    content = f.readlines()

#因為字典檔裡面有重複的型號，所以先建立一個python集合的特性用來過濾重複型號
no_extra_list = set()

#用迴圈跑每個型號
for line in content:
    line = line.strip()
    no_extra_list.add(line)

#去掉重複後把所有型號轉回list格式
all_models = list(no_extra_list)

# print(all_models)

#因為這樣型號還是很難配對到，所以我們先把 ASUS去掉 (都已經在asus版留言了,很少人會再寫asus在型號前面八，而且不影響判斷)
all_models = [i.replace('ASUS','').strip() for i in all_models]

#ZenFone 如果後面只有接一個字母的話 似乎有留下ZenFone的必要， 但像是 ZenFone Max Pro M2 這種，或許就不需要前面的Zenphone了，不過我先不處理這些，先跑一次看看結果如何

#另外我也想到大小寫的問題，已經確認過含有中文的字串用 .lower() 方法不會出錯，所以就用這個方法 在每次判斷前將內文轉換成 lower 再用 型號名.lower() 去判斷是否含有關鍵字

#把本地目錄所有asus檔案(一個檔案代表一篇文章)存到list內
file_list = os.listdir('C:/Users/NIHILI/Desktop/rawdata/mobile01_data/Asus')

#建立空字串
related_text = ''

for model in all_models:
    modelname = model.lower()
    for file in file_list:
        #檢查運行進度
        print(  all_models.index(model)+1 , '/' , len(all_models) , '----' , file_list.index(file)+1 ,'/', len(file_list) )

        with open('C:/Users/NIHILI/Desktop/rawdata/mobile01_data/Asus/{}'.format(file),'r',encoding='utf-8-sig') as f:
            article = json.load(f)
            title = article['標題'].lower()
            page = article['內文'].lower()
            comments = article['留言']

            if modelname in title:
                related_text += title
                related_text += page
            elif modelname in page:
                related_text += page
            else:
                pass
            for comment in comments:
                if modelname in comment.lower():
                    related_text += comment
                else:
                    pass
        # print(related_text)
        # break
    with open('C:/Users/NIHILI/Desktop/answer/{}.json'.format(model.replace(' ','_')),'w+',encoding='utf-8-sig') as f:
        json.dump({model:related_text},f)
        # print(related_text)
        print('寫入成功')
        #寫完檔案重置related_text
        related_text = ''