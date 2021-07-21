from django.shortcuts import render
from WXBizMsgCrypt3 import WXBizMsgCrypt
from django.http import HttpResponse
from FAQrobot import FAQrobot
import urllib.parse
import xml.etree.cElementTree as ET
import time

# Create your views here.
def weixin(request):
    sToken = "O5LwvD7RUvT3YHXL6PMyKZbYKb"
    sEncodingAESKey = "1QPbnqLUVjalDacyZCVFYJpPHJd3NjObtr3MhUN7UwE"
    sCorpId = "wwde422238e94c2a81"

    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpId)

    if request.method == 'GET':
        # sVerifyMsgSig=HttpUtils.ParseUrl("msg_signature")
        sVerifyMsgSig = request.GET.get("msg_signature")
        # ret=wxcpt.VeryfiAESKey()

        # sVerifyTimeStamp=HttpUtils.ParseUrl("timestamp")
        sVerifyTimeStamp = request.GET.get("timestamp")
        # sVerifyNonce=HttpUtils.ParseUrl("nonce")
        sVerifyNonce = request.GET.get("nonce")
        # sVerifyEchoStr=HttpUtils.ParseUrl("echostr")
        sVerifyEchoStr = request.GET.get("echostr")

        # 回调测试的回文
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)

        # print("这是sEchoStr:"+str(sEchoStr))
        # if (sEchoStr != 0):
        # print ("ERR: VerifyURL ret: " + str(ret))
        # sys.exit(1)
        return HttpResponse(sEchoStr)

    elif request.method == 'POST':

        sReqMsgSig = request.GET.get('msg_signature')
        sReqTimeStamp = request.GET.get('timestamp')
        sReqNonce = request.GET.get('nonce')

        sReqData = request.body  # 如何获取raw xml？
        # print("\n这是msg_signature：" + str(sReqMsgSig))
        # print("\n这是timestamp：" + str(sReqTimeStamp))
        # print("\n这是nonce：" + str(sReqNonce))
        # print("\n这是request.body：" + str(sReqData))

        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        # print("\n这是ret,sMsg：" + str(sMsg))  # sMsg即为xml格式的明文
        # if (ret != 0):
        #     print("ERR: DecryptMsg ret: " + str(ret))
        #     sys.exit(1)

        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text
        user_id= xml_tree.find("ToUserName").text   # 取得userId
        print(content)    # content即为用户发送的消息

        # 这里插入FAQrobot
        robot = FAQrobot('QA.txt', usedVec=False)

        # roboResponse为FAQrobot匹配的答案
        roboResponse = robot.answer(content,'simple_pos')

        #计算createtime
        createTime=time.time()

        #提问用户的userId(fromusername，来源于收到的消息的xml的toUserName)
        sRespData="<xml><ToUserName>wwde422238e94c2a81</ToUserName><FromUserName>wat</FromUserName><CreateTime>"+round(createTime)+"</CreateTime><MsgType>text</MsgType><Content>"+roboResponse+"</Content></xml>"

        ret, sEncryptMsg=wxcpt.EncryptMsg(sRespData,sReqNonce,sReqTimeStamp)

        return HttpResponse(sEncryptMsg)
