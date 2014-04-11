# coding=utf-8
import hashlib
import xml.etree.ElementTree as ET
import urllib2
# import requests
import json
import datetime
from django.http.response import HttpResponse
global WX_TXT_RSP # 纯文本格式
WX_TXT_RSP = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""
global WX_PIC_TXT_RSP # 图文格式
WX_PIC_TXT_RSP = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%s]]></Url>
                </item>
                </Articles>
                <FuncFlag>1</FuncFlag>
                </xml> """


def weixin(request):
    if request.method == "GET":
        rsptext = checkSignature(request)
        print rsptext 
        return HttpResponse(rsptext, content_type="text/plain")
    else:
        rsptext = response_msg(request)
        print rsptext 
        return HttpResponse(rsptext, content_type="text/plain")

def response_msg(request):
    """
    这里是响应微信Server的请求，并返回数据的主函数，判断Content内容，如果是一条“subscribe”的事件，就
    表明是一个新注册用户，调用纯文本格式返回，如果是其他的内容就组织数据以图文格式返回。
 
    基本思路：
    # 拿到Post过来的数据
    # 分析数据（拿到FromUserName、ToUserName、CreateTime、MsgType和content）
    # 构造回复信息（将你组织好的content返回给用户）
    """
    # 拿到并解析数据
    msg = parse_msg(request)
    # 判断MsgType内容，如果是一条“subscribe”的event，表明是一个新关注用户
    # 和电影海报组成的图文信息
    if msg["MsgType"] == "event":
        echostr = WX_TXT_RSP % (
            msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),
            u"欢迎关注！")
        return echostr
    if msg["MsgType"] == "text":
        receive_content =msg["Content"]
#         if receive_content == 'bd':
            
        Content = handle_text_msg(msg)
        echostr = WX_TXT_RSP % ( msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),Content)
#         description = query_movie_details()
#         echostr = pictextTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),
#                                 Content["subjects"][0]["title"], description,
#                                 Content["subjects"][0]["images"]["large"], Content["subjects"][0]["alt"])
        return echostr

def handle_text_msg(msg):
    content = msg["Content"]
    if content == 'bd':
        return '需要绑定'

def checkSignature(request):
    """
    这里是用来做接口验证的，从微信Server请求的URL中拿到“signature”,“timestamp”,"nonce"和“echostr”，
    然后再将token, timestamp, nonce三个排序并进行Sha1计算，并将计算结果和拿到的signature进行比较，
    如果相等，就说明验证通过。
    话说微信的这个验证做的很渣，因为只要把echostr返回去，就能通过验证，这也就造成我看到一个Blog中，
    验证那儿只返回了一个echostr，而纳闷了半天。
    附微信Server请求的Url示例：http://yoursaeappid.sinaapp.com/?signature=730e3111ed7303fef52513c8733b431a0f933c7c
    &echostr=5853059253416844429&timestamp=1362713741&nonce=1362771581
    """
    token = "moneyball"  # 你在微信公众平台上设置的TOKEN
    signature = request.GET.get('signature', None)  # 拼写不对害死人那，把signature写成singnature，直接导致怎么也认证不成功
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return echostr
    else:
        return None
 
 
def parse_msg(request):
    """
    这里是用来解析微信Server Post过来的XML数据的，取出各字段对应的值，以备后面的代码调用，也可用lxml等模块。
    """

#     recvmsg = request.body.read()  # 严重卡壳的地方，最后还是在Stack OverFlow上找到了答案
    recvmsg = request.body  # 严重卡壳的地方，最后还是在Stack OverFlow上找到了答案
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg
 

def query_due_info():
    """
    查询待收明细
    """
    return movie
 
 
def query_loan_summary():
    """
    查询汇总信息
    """
    return description
 
 

 
