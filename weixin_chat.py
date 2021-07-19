# -*- coding: utf-8 -*-

import requests
import itchat
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
schema = Schema(question=TEXT(stored=True, analyzer=analyzer), answer=TEXT(stored=True, analyzer=analyzer))
ix = open_dir("index")
searcher = ix.searcher()

KEY = '9c21856644214047a3df749146e48c04'


def get_response(msg):
    # 这里实现与图灵机器人的交互
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


# 这里实现微信消息的获取
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 这里设置一个默认回复
    print(u'客户：' + msg['Text'])
    defaultReply = 'I received: ' + msg['Text'] + '您的这个问题我还需要研究'
    results = searcher.find("question", msg['Text'])
    for hit in results:
        reply = hit['answer']
        print(u'回复: ' + reply)
        return reply
    return defaultReply


# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
