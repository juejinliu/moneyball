# -*- coding: utf-8 -*-
from moneyball.loan.models import *
from moneyball.common.utilfun import *
from django.db.models import Sum
import decimal
import datetime
from datetime import timedelta
from platform import platform

class loancalc(object):
    def __init__(self,user):
        self.user = user
        self.loan_notreturnstatus = Returnstatus.objects.get(status = 0)    #未回款状态
        self.loan_returnedstatus = Returnstatus.objects.get(status = 1)     #已回款状态
        self.loandtllist = Loandetail.objects.filter(user=self.user) 
        self.loanlist = Loan.objects.filter(user=self.user)
        
           
    
# 待收本金
    def getdueallown(self):
        ret_data = self.loandtllist.filter(status=self.loan_notreturnstatus).aggregate(Sum('ownamt'))['ownamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data

# 待收利息
    def getdueallins(self):
        ret_data = self.loandtllist.filter(status=self.loan_notreturnstatus).aggregate(Sum('insamt'))['insamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data

# 总本金
    def getallown(self):
        ret_data = self.loandtllist.aggregate(Sum('ownamt'))['ownamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data

# 总利息
    def getallins(self):
        ret_data = self.loandtllist.filter(status=self.loan_returnedstatus).aggregate(Sum('insamt'))['insamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data

# 总手管理费
    def getallfee(self):
        ret_data = self.loandtllist.filter(status=self.loan_returnedstatus).aggregate(Sum('feeamt'))['feeamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data

# 总奖励
    def getallaward(self):
        ret_data = float(0.00)
        if self.loanlist.count() > 0:
            ret_data += float(self.loanlist.aggregate(Sum('awardamt'))['awardamt__sum'])
            ret_data += float(self.loanlist.aggregate(Sum('continuedamt'))['continuedamt__sum'])
            ret_data += float(self.loanlist.aggregate(Sum('offlineamt'))['offlineamt__sum'])
        return ret_data

# 当月已收利息
    def getcurrmonthins(self):
        now = datetime.datetime.now()
        ret_data = self.loandtllist.filter(status=self.loan_returnedstatus,returndate__year=now.year,returndate__month=now.month).aggregate(Sum('insamt'))['insamt__sum']
        if not ret_data:
            ret_data = 0.00
        return ret_data
        
# 当月奖励
    def getcurrmonthaward(self):
        ret_data = float(0.00)
        now = datetime.datetime.now()
        if self.loanlist.count() > 0:
            if self.loanlist.filter(loandate__year=now.year,loandate__month=now.month).count()>0:
                ret_data += float(self.loanlist.filter(loandate__year=now.year,loandate__month=now.month).aggregate(Sum('awardamt'))['awardamt__sum'])
            ret_data += float(self.loanlist.aggregate(Sum('continuedamt'))['continuedamt__sum'])
            ret_data += float(self.loanlist.aggregate(Sum('offlineamt'))['offlineamt__sum'])
        return ret_data
    
# 得到平台统计数据
    def getpfsummary(self):
        ret_data = {}
        pf_names = []
        pf_dueownamt = []   #待收本金
        pf_dueinsamt = []   #待收利息
        pf_insamt = []      #已赚利息
        pf_awardamt = []    #已赚奖励
        pf_ownamt = []      #本金
        pf_feeamt = []      #已付管理费
        pf_duefeeamt = []   #待付管理费
        pf_dueallamt = []   #待收总额
        pf_incomeamt = []   #总收益
        pf_allamt = []      #已回收总金额
        pf_loan_amt = self.loanlist.values('platform').annotate(sumamt=Sum('amount'),sumaward=Sum('awardamt')).order_by('platform')
        for pf in pf_loan_amt:
            pf_id = pf['platform']
            pf_name = Platform.objects.get(id=pf_id)
            pf_names.append(pf_name)
            pf_awardamt.append(pf['sumaward'])
            pf_dtlamt = self.loandtllist.filter(platform=pf_id).values('status').annotate(suminsamt=Sum('insamt'),sumfeeamt=Sum('feeamt'),sumownamt=Sum('ownamt'))
            for pf_status_record in pf_dtlamt:  #这个地方只循环两次，如果有坏账就循环3次
                if pf_status_record['status'] == self.loan_notreturnstatus.id:
                    pf_dueinsamt.append(pf_status_record['suminsamt'])
                    pf_dueownamt.append(pf_status_record['sumownamt'])
                    pf_duefeeamt.append(pf_status_record['sumfeeamt'])
                    pf_dueallamt.append(pf_status_record['suminsamt'] + pf_status_record['sumownamt'] - pf_status_record['sumfeeamt'])  #待收总额
                elif pf_status_record['status'] == self.loan_returnedstatus.id:
                    pf_insamt.append(pf_status_record['suminsamt'])
                    pf_ownamt.append(pf_status_record['sumownamt'])
                    pf_feeamt.append(pf_status_record['sumfeeamt'])
                    pf_incomeamt.append(pf_status_record['suminsamt'] + pf['sumaward'] - pf_status_record['sumfeeamt'])    #已收总额
                    pf_allamt.append(float(pf['sumaward']) + float(pf_status_record['suminsamt']) + float(pf_status_record['sumownamt']) - float(pf_status_record['sumfeeamt']))    #已收总额
                 
        ret_data['pfdueinsamt'] = pf_dueinsamt
        ret_data['pfdueownamt'] = pf_dueownamt
        ret_data['pfduefeeamt'] = pf_duefeeamt
        ret_data['pfnames'] = pf_names
        ret_data['pfawardamt'] = pf_awardamt
        ret_data['pfinsamt'] = pf_insamt
        ret_data['pfownamt'] = pf_ownamt
        ret_data['pffeeamt'] = pf_feeamt
        ret_data['pfdueallamt'] = pf_dueallamt
        ret_data['pfincomeamt'] = pf_incomeamt
        ret_data['pfallamt'] = pf_allamt
#         pf_amt = self.loandtllist.values('platform').annotate(sumamt=Sum('amount'),sumaward=Sum('awardamt')).order_by('platform')
#         ret_data = pf_amt
        return ret_data


# 得到月份统计数据
    def getmonthsummary(self):
        ret_data = {}
        m_months = []
        m_amount = []      #投标总额
        m_insamt = []      #已赚利息
        m_awardamt = []    #已赚奖励
        m_incomeamt = []   #当月收益
        now = datetime.datetime.now()
        for m in range(0,-12,-1):
            targetmonth = monthdelta(now,m)
            m_loan_amt = float(0.00)
            m_loandtl_insamt = float(0.00)
            m_loan_awardamt = float(0.00)
            m_loandtl_incomeamt = float(0.00)
            if self.loanlist.filter(loandate__year=targetmonth.year,loandate__month=targetmonth.month).count() > 0:
                m_loan_amt = float(self.loanlist.filter(loandate__year=targetmonth.year,loandate__month=targetmonth.month).aggregate(Sum('amount'))['amount__sum'])
                m_loan_awardamt = float(self.loanlist.filter(loandate__year=targetmonth.year,loandate__month=targetmonth.month).aggregate(Sum('awardamt'))['awardamt__sum'])
                m_loan_awardamt += float(self.loanlist.filter(loandate__year=targetmonth.year,loandate__month=targetmonth.month).aggregate(Sum('continuedamt'))['continuedamt__sum'])
                m_loan_awardamt += float(self.loanlist.filter(loandate__year=targetmonth.year,loandate__month=targetmonth.month).aggregate(Sum('offlineamt'))['offlineamt__sum'])
            if self.loandtllist.filter(returndate__year=targetmonth.year,returndate__month=targetmonth.month,status=self.loan_returnedstatus).count() > 0:
                m_loandtl_insamt = float(self.loandtllist.filter(returndate__year=targetmonth.year,returndate__month=targetmonth.month,status=self.loan_returnedstatus).aggregate(Sum('insamt'))['insamt__sum'])
                m_loandtl_feeamt = float(self.loandtllist.filter(returndate__year=targetmonth.year,returndate__month=targetmonth.month,status=self.loan_returnedstatus).aggregate(Sum('feeamt'))['feeamt__sum'])
                m_loandtl_insamt -= float(m_loandtl_feeamt)
                m_loandtl_incomeamt = float(m_loan_awardamt) + float(m_loandtl_insamt)
            m_months.append(targetmonth.strftime("%Y-%m"))
            m_amount.append(m_loan_amt)
            m_insamt.append(m_loandtl_insamt)
            m_awardamt.append(m_loan_awardamt)
            m_incomeamt.append(m_loandtl_incomeamt)
        ret_data['m_months'] = m_months
        ret_data['m_amount'] = m_amount
        ret_data['m_insamt'] = m_insamt
        ret_data['m_awardamt'] = m_awardamt
        ret_data['m_incomeamt'] = m_incomeamt
        return ret_data


# 得到今天待收明细及未来30天待收数据，用于显示welcome.html中数据
    def getmonthdue(self):
        ret_data = {}
        d_days = []
        d_amount = []      #待收总额
        now = datetime.datetime.now()
        fromdate = datetime.date(now.year,now.month,now.day);
        enddate = now + timedelta(days=30)
# 当日待收明细
        today_due_list = self.loandtllist.filter(expiredate__lte=fromdate,status=self.loan_notreturnstatus).order_by('-expiredate')
        insamt_sum = 0.00
        feeamt_sum = 0.00
        ownamt_sum = 0.00
        amount_sum = 0.00
        if today_due_list and today_due_list.count() > 0:
            insamt_sum = today_due_list.aggregate(Sum('insamt'))['insamt__sum']
            ownamt_sum = today_due_list.aggregate(Sum('ownamt'))['ownamt__sum']
            feeamt_sum = today_due_list.aggregate(Sum('feeamt'))['feeamt__sum']
            amount_sum = float(ownamt_sum) + float(insamt_sum) - float(feeamt_sum)
# 未来30天待收明细，用于生成柱状图        
        dtl_list = self.loandtllist.filter(expiredate__range=(fromdate,enddate),status=self.loan_notreturnstatus).values('expiredate').annotate(sumownamt=Sum('ownamt'),suminsamt=Sum('insamt'),sumfeeamt=Sum('feeamt')).order_by('-expiredate')
        for m in range(0,30):
            targetday = now + datetime.timedelta(days=m)
            d_days.append(targetday.strftime("%d"))
            targetvalue = dtl_list.filter(expiredate=targetday)
            tmp_amount = 0.00
            if targetvalue:
                for n in targetvalue:
                    tmp_amount += float(n['sumownamt']) + float(n['suminsamt']) - float(n['sumfeeamt'])
            d_amount.append(tmp_amount)
        ret_data['d_days'] = d_days
        ret_data['d_amount'] = d_amount
        ret_data['today_due_list'] = today_due_list
        ret_data['insamt_sum'] = insamt_sum
        ret_data['feeamt_sum'] = feeamt_sum
        ret_data['ownamt_sum'] = ownamt_sum
        ret_data['amount_sum'] = amount_sum
        return ret_data
    
