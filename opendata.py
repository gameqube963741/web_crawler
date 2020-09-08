import urllib.request as request
import json
with request.urlopen('https://data.taipei/api/v1/dataset/296acfa2-5d93-4706-ad58-e83cc951863c?scope=resourceAquire') as response:
    data = json.load(response) 
print(data)

# 將公司資料列表出來
clist = data['result']['results']
with open ('data.txt','w',encoding='utf-8-sig') as file:
    for company in clist:
        file.write(company['公司名稱']+'\n')