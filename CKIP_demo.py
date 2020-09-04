import pandas as pd
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
# import jieba

path = "C:/Users/Big data/PycharmProjects/ckiptagger/ptt_iphone6_content.csv"

x = pd.read_csv(path, encoding = 'ANSI')
print(x)

for n, i in enumerate(x.Content):
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")
    text = "x"
    ws_results = ws([i])

    po_results = pos([text])
    # ner_results = ner([text],pos_results)

    print(n)
    print(ws_results)
    # print(pos_results)
    # print(ner_results)
    # save as different .text
    f = open(r'./words/ptt_iphone6_%s.text' %n, 'w', encoding='utf-8-sig')
    f.write(str(ws_results))
    f.close()