# -*- coding: UTF-8 -*-
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
filename_list=[]
ID_list = []

schema = Schema(question=TEXT(stored=True, analyzer=analyzer), answer=TEXT(stored=True, analyzer=analyzer))
ix = open_dir("index")
searcher = ix.searcher()
results = searcher.find("question", u"学校的宿舍环境")
print (results.__len__() )
for hit in results:
    print(hit.score)
    print(hit['answer'])
    # if hit.score > 0:
    #     print(hit['content'])
searcher.close()

