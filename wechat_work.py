# -*- coding: utf-8 -*-

import requests
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
schema = Schema(question=TEXT(stored=True, analyzer=analyzer), answer=TEXT(stored=True, analyzer=analyzer))
ix = open_dir("index")
searcher = ix.searcher()


def reply():
    # 这里设置一个默认回复
    print(u'客户：' + msg['Text'])
    defaultReply = 'I received: ' + msg['Text'] + '您的这个问题我还需要研究'
    results = searcher.find("question", msg['Text'])
    for hit in results:
        reply = hit['answer']
        print(u'回复: ' + reply)
        return reply
    return defaultReply