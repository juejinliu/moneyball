# coding=utf-8
import hashlib
import xml.etree.ElementTree as ET
import urllib2
from moneyball.wx.models import Wxautoreply
from moneyball.loan.views import loan_detail_return_core
from moneyball.loan.models import *
from moneyball.user.models import *
import copy
from datetime import timedelta
# import requests
import json
import datetime
from locale import str
from test.test_iterlen import len
from django.http.response import HttpResponse
from moneyball.loan.loancalc import *
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
    echostr = '出错了'
    # 判断MsgType内容，如果是一条“subscribe”的event，表明是一个新关注用户
    # 和电影海报组成的图文信息
    if msg["MsgType"] == "event":
        try:
            content = Wxautoreply.objects.get(code='command').content
        except Wxautoreply.DoesNotExist:
            content = u'请发送命令至本微信号查询待收明细等'
        echostr = WX_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),content)
        return echostr
    if msg["MsgType"] == "text":
        receive_content =msg["Content"]
        receive_content_code = copy.copy(receive_content[0:2])
        if receive_content_code.lower() == 'bd':     #绑定微信号
            echostr = wxbindreply(msg)
        elif receive_content_code.lower() == 'jb':     #解绑微信号
            echostr = wxunbindreply(msg)
        elif receive_content_code.lower() == 'ds':     #查询当日待收
            echostr = wxquerydue(msg)
        elif receive_content.lower() == 'hkall':     #回款当天所有
            echostr = wxloanreturn(msg)
        elif receive_content_code.lower() == 'hk':     #回款特定记录
            dtlid= copy.copy(receive_content[2:len(receive_content)])
            if len(receive_content) <= 2:
                echostr = WX_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),u'请输入待收编号')
            elif not dtlid.isdigit():
                echostr = WX_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),u'请输入正确待收编号')
            else:
                echostr = wxloanreturn(msg,receive_content[2:len(receive_content)])
        elif receive_content_code.lower() == 'hz':     #汇总
            echostr = wxloansummary(msg)
        else:
            try:
                content = Wxautoreply.objects.get(code='command').content
            except Wxautoreply.DoesNotExist:
                content = u'未知错误，请发送截图给本微信号'
            echostr = WX_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),content)
    if echostr == 'NONE_WEIXINID':            #如果没有绑定微信号
        echostr = wxbindreply(msg)
    return echostr

# 查询当前用户汇总信息
def wxloansummary(msg):
    try:
        myusers = MyUser.objects.filter(wxid=msg['FromUserName'])
    except MyUser.DoesNotExist:
        return 'NONE_WEIXINID'
    if not myusers or myusers.count()==0:
        return 'NONE_WEIXINID'
    rtntxt = ''
    for myuser in myusers:
        lc = loancalc(myuser.user)
        dueallown = lc.getdueallown()
        dueallins = lc.getdueallins()
        dueallamt = float(dueallown) + float(dueallins)
        allins = lc.getallins()
        allfee = lc.getallfee()
        allaward = lc.getallaward()
        allincome = float(allins) - float(allfee) + float(allaward)

        currmonthins = lc.getcurrmonthins()
        currmonthaward = lc.getcurrmonthaward()
        currincome = float(currmonthins) + float(currmonthaward)
        rtntxt += u"您用户名为" + myuser.user.username + u"的汇总账务信息如下：\n"
        rtntxt += u"当月收益   :"+ str(currincome) +"\n"
        rtntxt += u"当月利息   :"+ str(currmonthins) +"\n"
        rtntxt += u"当月奖励   :"+ str(currmonthaward) +"\n"
        rtntxt += u"总收益   :"+ str(allincome) +"\n"
        rtntxt += u"当月收益   :"+ str(allins) +"\n"
        rtntxt += u"总利息   :"+ str(currincome) +"\n"
        rtntxt += u"总奖励   :"+ str(allaward) +"\n"
        rtntxt += u"管理费   :"+ str(allfee) +"\n"
        rtntxt += u"待收本金   :"+ str(dueallown) +"\n"
        rtntxt += u"待收利息   :"+ str(dueallins) +"\n"
        rtntxt += u"待收总额   :"+ str(dueallamt) +"\n"
    result = WX_TXT_RSP % ( msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),rtntxt)
    return result

# 设置当日待收全部回款
def wxloanreturn(msg,loandtlid = None):
    try:
        myusers = MyUser.objects.filter(wxid=msg['FromUserName']).values_list('user', flat=True)
    except MyUser.DoesNotExist:
        return 'NONE_WEIXINID'
    if not myusers or myusers.count()==0:
        return 'NONE_WEIXINID'
    if loandtlid:
        rtn = loan_detail_return_core(loandtlid)
        rtntxt = "编号为" + loandtlid + "待收回款成功";
    else:
        now = datetime.datetime.now()
        loan_notreturnstatus = Returnstatus.objects.get(status = 0)
        loandtllist = Loandetail.objects.filter(user__in=myusers,expiredate__lte=now,status=loan_notreturnstatus).order_by('expiredate')
        for loandtl in loandtllist:
            rtn = loan_detail_return_core(loandtl.id)
        rtntxt = "当天"+ str(loandtllist.count()) +"笔待收全部回款成功";
    result = WX_TXT_RSP % ( msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),rtntxt)
    return result

# 查询当日明天待收明细
def wxquerydue(msg):
    try:
        myusers = MyUser.objects.filter(wxid=msg['FromUserName']).values_list('user', flat=True)
    except MyUser.DoesNotExist:
        return 'NONE_WEIXINID'
    if not myusers or myusers.count()==0:
        return 'NONE_WEIXINID'
    rtntxt = u"""您今天待收明细:
        ------------------------------------\n"""
#     myusersname = myusers.user.username
    now = datetime.datetime.now()
    tommorow = now + timedelta(days=1)
    
    loan_notreturnstatus = Returnstatus.objects.get(status = 0)
#     当天明细
    loandtllist = Loandetail.objects.filter(user__in=myusers,expiredate__lte=now,status=loan_notreturnstatus).order_by('expiredate')
    if loandtllist and loandtllist.count()>0:
        sumamt = 0
        for loandtl in loandtllist:
            sumamt += loandtl.ownamt + loandtl.insamt - loandtl.feeamt
            rtntxt += str(loandtl.id) 
            rtntxt += '   ' + loandtl.platform.name 
            rtntxt += '   ' + str(loandtl.ownamt + loandtl.insamt - loandtl.feeamt) + '\n'
        rtntxt += "------------------------------------\n"
        rtntxt += u"共[" + str(loandtllist.count()) + u"]笔,总金额:" + str(sumamt) +"\n"
    else:
        rtntxt += u"没有明细\n"
# 明天待收    
    rtntxt += u"\n您明天待收明细:\n";
    rtntxt += "------------------------------------\n";
    loandtllist = Loandetail.objects.filter(user__in=myusers,expiredate=tommorow,status=loan_notreturnstatus)
    if loandtllist and loandtllist.count()>0:
        sumamt = 0
        for loandtl in loandtllist:
            sumamt += loandtl.ownamt + loandtl.insamt - loandtl.feeamt
            rtntxt += str(loandtl.id) + '   ' + loandtl.platform.name + '   ' + str(loandtl.ownamt + loandtl.insamt - loandtl.feeamt)
        rtntxt += "------------------------------------\n"
        rtntxt = rtntxt + u"共["+ str(loandtllist.count()) + u"]笔,总金额:" + str(sumamt) +"\n"
    else:
        rtntxt += u"没有明细\n"
    result = WX_TXT_RSP % ( msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),rtntxt)
    return result

def wxbindreply(msg):
    try:
        bindURL = Wxautoreply.objects.get(code='bindURL').content + msg['FromUserName']
    except Wxautoreply.DoesNotExist:
        bindURL = 'http://moneyball.com.cn/bindWeixinID?wx_id=' + msg['FromUserName']
        
    try:
        picURL = Wxautoreply.objects.get(code='PicUrl').content
    except Wxautoreply.DoesNotExist:
        picURL = 'http://moneyball.com.cn/common/static/images/mb06.png'
    rtntxt = WX_PIC_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),
                             u'您未绑定微信号，点击绑定',u'点击输入用户名密码，验证成功则将微信号与账户绑定。点击绑定',
                             picURL , bindURL)
    return rtntxt

def wxunbindreply(msg):
    try:
        unbindURL = Wxautoreply.objects.get(code='unBindURL').content + msg['FromUserName']
    except Wxautoreply.DoesNotExist:
        unbindURL = 'http://moneyball.com.cn/unBindWeixinID?wx_id=' + msg['FromUserName']
        
    try:
        picURL = Wxautoreply.objects.get(code='PicUrl').content
    except Wxautoreply.DoesNotExist:
        picURL = 'http://moneyball.com.cn/common/static/images/mb06.png'

    rtntxt = WX_PIC_TXT_RSP % (msg['FromUserName'], msg['ToUserName'], datetime.datetime.now(),
                             u'您确定要解除账户绑定吗？',u'点击输入用户名密码，验证成功则解除微信号与账户的绑定。点击解绑',
                             picURL , unbindURL)
    return rtntxt


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
 
 

 
