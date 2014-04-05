# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from moneyball.loan.forms import *
from django.contrib.auth.decorators import login_required
from moneyball.loan.models import Loan
from django.db.models import Sum
from moneyball.loan.models import *
import json

# Create your views here.
def index(request):
    pass
#===============================================================================
# 汇总信息
#===============================================================================
@login_required
def loansummary(request):
    pass
#===============================================================================
# 借出明细
#===============================================================================
# @login_required
# def loanlist(request):
#     if request.method == 'POST':
#         pass
#     else:
#         loan_list = Loan.objects.filter(user=request.user).order_by('-loandate')
#     record_number = loan_list.count
#     amount_sum = loan_list.aggregate(Sum('amount'))['amount__sum']
#     income_sum = loan_list.aggregate(Sum('insamt'))['insamt__sum']
#     income_sum += loan_list.aggregate(Sum('awardamt'))['awardamt__sum']
#     income_sum += loan_list.aggregate(Sum('continuedamt'))['continuedamt__sum']
#     income_sum += loan_list.aggregate(Sum('offlineamt'))['offlineamt__sum']
#     feeamt_sum = loan_list.aggregate(Sum('feeamt'))['feeamt__sum']
#     #===========================================================================
#     # for loan in loan_list:
# #         if loan.loandetail_set.aggregate(Sum('feeamt'))['feeamt__sum'] is None:
# #             pass
# #         else:
# #             feeamt_sum += loan.loandetail_set.aggregate(Sum('feeamt'))['feeamt__sum']   
#     #===========================================================================
#     return render_to_response('loanlist.html', {"loan_list": loan_list,
#                                                "record_number": record_number,
#                                                "amount_sum":amount_sum,
#                                                "income_sum":income_sum,
#                                                "feeamt_sum":feeamt_sum}, RequestContext(request))
#===============================================================================
# 待收明细 
#===============================================================================
@login_required
def loandetaillist(request):
    if request.method == 'POST':
        pass
    else:
        loandetail_list = Loandetail.objects.filter(user=request.user).order_by('-expiredate')
    record_number = loandetail_list.count
    ownamt_sum = loandetail_list.aggregate(Sum('ownamt'))['ownamt__sum']
    insamt_sum = loandetail_list.aggregate(Sum('insamt'))['insamt__sum']
    feeamt_sum = loandetail_list.aggregate(Sum('feeamt'))['feeamt__sum']
    return render_to_response('loandetaillist.html', {"loandetail_list": loandetail_list,
                                               "record_number": record_number,
                                               "ownamt_sum":ownamt_sum,
                                               "insamt_sum":insamt_sum,
                                               "feeamt_sum":feeamt_sum}, RequestContext(request))

@login_required
def loan_detail_return(request):
     try:
         rtn_record = Loandetail.objects.get(id=request.GET['Loan_detail_id'])
     except Loandetail.DoesNotExist:
         return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
     tmpstatus = Returnstatus.objects.get(status = 1)
     rtn_record.status = tmpstatus
     rtn_record.save()
     inreturnstatus = Returnstatus.objects.get(status = 0)
     loandtls = rtn_record.loan.loandetail_set.filter(status = inreturnstatus)
     if not loandtls:  #如果这个借款记录关联的所有明细都还清则把这调记录标记为已还清
         rtn_record.loan.status = tmpstatus
         rtn_record.loan.save()
     previousurl = request.META['HTTP_REFERER']
#     print tmpurl
     return HttpResponseRedirect(previousurl)
#     return HttpResponseRedirect('/welcome')

@login_required
def loan_detail_no_return(request):
     try:
         rtn_record = Loandetail.objects.get(id=request.GET['Loan_detail_id'])
     except Loandetail.DoesNotExist:
         return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
     tmpstatus = Returnstatus.objects.get(status = 0)
     rtn_record.status = tmpstatus
     rtn_record.save()
     rtn_record.loan.status = tmpstatus
     rtn_record.loan.save()
     previousurl = request.META['HTTP_REFERER']
#     print tmpurl
     return HttpResponseRedirect(previousurl)
#     return HttpResponseRedirect('/welcome')


@login_required
def loan_detail_bad(request):
    try:
        rtn_record = Loandetail.objects.get(id=request.GET['Loan_detail_id'])
    except Loandetail.DoesNotExist:
        return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
    tmpstatus = Returnstatus.objects.get(status = 2)
    rtn_record.status = tmpstatus
    rtn_record.save()
    rtn_record.loan.status = tmpstatus
    rtn_record.loan.save()
    previousurl = request.META['HTTP_REFERER']
    return HttpResponseRedirect(previousurl)

#===============================================================================
# 借款记录的添加修改都在这个类里面完成
#===============================================================================
@login_required
def loaninfo(request,lnid=None):
    infomsg = u''
    if request.method == 'POST':
#         参数data应该是None，POST的数据作为args传入
        form = LoanForm(request.user,None, request.POST)
        if form.is_valid():
            #try:
            new_loan = form.save(None,lnid)
            infomsg = u'操作成功'
            #except:
                #raise Http404
#             return render_to_response("success.html",({'infomsg':u'添加成功'}), RequestContext(request))
    elif request.method == 'GET':
        try:
            if lnid:
                rtn_record = Loan.objects.get(id=lnid)
                form = LoanForm(request.user,rtn_record)
                lnid = rtn_record.id
            else:
                form = LoanForm(request.user,None)
        except LoanForm.DoesNotExist:
            return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
    results = Loan.objects.filter(user=request.user).order_by('-loandate')
    return render_to_response("loan.html", RequestContext(request,{
                                                'form': form,
                                                'lnid': lnid,
                                                'infomsg':infomsg,
                                                "loan_list": results})
                              )

#===============================================================================
# 借款记录的删除
#===============================================================================
@login_required
def loandelete(request,lnid=None):
    form = LoanForm(request.user,None)
    if request.method == 'GET':
        if lnid:
            #try:
            delete_loan = Loan.objects.get(id=lnid)
            delete_loan.delete()
            #except:
                #raise Http404
#             return render_to_response("success.html",({'infomsg':u'添加成功'}), RequestContext(request))
    results = Loan.objects.filter(user=request.user).order_by('-loandate')
    previousurl = request.META['HTTP_REFERER']
    return HttpResponseRedirect(previousurl, RequestContext(request,{
                                                'form': form,
                                                'infomsg':u'删除成功',
                                                "loan_list": results})
                              )
#     return render_to_response("loan.html", RequestContext(request,{
#                                                 'form': form,
#                                                 'infomsg':u'删除成功',
#                                                 "loan_list": results})
#                               )


#===============================================================================
# 平台的修改，隐藏，添加操作在这个类里面全部完成
#===============================================================================
@login_required
def platforminfo(request,pfid=None,status=None):
    form = PlatformForm(Platform())
    platformid = pfid
    if request.method == 'POST':
        form = PlatformForm(None,request.POST)
        if form.is_valid():
            #try:
            new_platform = form.save(request,None,pfid)
            #except:
            #    raise Http404
    elif request.method == 'GET':
        try:
            if pfid:
                rtn_record = Platform.objects.get(id=pfid)
                if status:
                    status_record = Booleancode.objects.get(code=status)
                    rtn_record.active = status_record
                    rtn_record.save()
                else:
                    form = PlatformForm(rtn_record)
                    platformid = rtn_record.id
        except Platform.DoesNotExist:
            return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
    results = Platform.objects.filter(user=request.user).order_by('id')
    return render_to_response("platform.html", RequestContext(request,{
                                                'form': form,
                                                'id': platformid,
                                                'infomsg':u'操作成功',
                                                "platform_list": results})
                                  )

@login_required
def getplatformfee(request):
    fee = 99.99
    items_dict = {'result':'0.00'}
    if request.method == 'POST':
        rtn_record = Platform.objects.get(id=request.POST['platform'])
        if rtn_record:
            #try:
             items_dict['result'] = str(rtn_record.rate)
            #except:
            #    raise Http404
    return HttpResponse(json.dumps(items_dict), content_type="application/json" )

@login_required
def loanlist(request):
    record_number = 0
    amount_sum = 0.00
    income_sum = 0.00
    feeamt_sum = 0.00
    if request.GET:
        form = LoanSearchForm(request.user,request.GET)
        if form.is_valid():
            results = form.get_result_queryset().filter(user=request.user).order_by('-loandate')
            record_number = results.count()
            if results and results.count() > 0:
                amount_sum = results.aggregate(Sum('amount'))['amount__sum']
                income_sum = results.aggregate(Sum('insamt'))['insamt__sum']
                income_sum += results.aggregate(Sum('awardamt'))['awardamt__sum']
                income_sum += results.aggregate(Sum('continuedamt'))['continuedamt__sum']
                income_sum += results.aggregate(Sum('offlineamt'))['offlineamt__sum']
                feeamt_sum = results.aggregate(Sum('feeamt'))['feeamt__sum']
            
        else:
            results = []
    else:
        form = LoanSearchForm(request.user,request.GET)
        results = []
    return render_to_response('loanlist.html', RequestContext(request,{ 
                                                'form': form,
                                                "loan_list": results,
                                                "record_number": record_number,
                                                "amount_sum":amount_sum,
                                                "income_sum":income_sum,
                                                "feeamt_sum":feeamt_sum})
                              )


@login_required
def loandetaillist(request):
    record_number = 0
    ownamt_sum = 0.00
    insamt_sum = 0.00
    feeamt_sum = 0.00
    if request.GET:
        form = LoanDtlSearchForm(request.user,request.GET)
        if form.is_valid():
            results = form.get_result_queryset().filter(user=request.user).order_by('-expiredate')
            record_number = results.count
            if results and results.count() > 0:
                ownamt_sum = results.aggregate(Sum('ownamt'))['ownamt__sum']
                insamt_sum = results.aggregate(Sum('insamt'))['insamt__sum']
                feeamt_sum = results.aggregate(Sum('feeamt'))['feeamt__sum']
            
        else:
            results = []
    else:
        form = LoanDtlSearchForm(request.user,request.GET)
        results = []
    return render_to_response('loandetaillist.html', RequestContext(request,{ 
                                                'form': form,
                                                "loandetail_list": results,
                                                "record_number": record_number,
                                                "ownamt_sum":ownamt_sum,
                                                "insamt_sum":insamt_sum,
                                                "feeamt_sum":feeamt_sum})
                              )
