from moneyball.loan.models import *
from django.contrib import admin

# admin.site.register(Loan)
admin.site.register(Platform)
admin.site.register(Loandetail)
admin.site.register(Booleancode)
admin.site.register(Returntype)
admin.site.register(Returnstatus)


class LoanAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'platform', 'amount','insrate','status','loandate')
    search_fields = ( 'user', 'platform', 'loandate', )
    list_filter = ('user','platform')

    readonly_fields = ( 'enrollment_chart', )
#     fieldsets = [
#      ('Course', { 'fields':  [  'course_id', 'title', 'catalog_number', \
#                     'department', 'course_type', 'status', ]}), \
# 
#     ('Semester Details', { 'fields':  [  'semester_details',  ]}),\
#     ('Enrollment', { 'fields':  [  'enrollment_chart',  ]}),\
#     readonly_fields = ('enrollment_chart', )
    fieldsets = [
     ('Loan', { 'fields':  [  'user', 'platform', 'amount', \
                    'loandate', 'status',]}),\
    ('Enrollment', { 'fields':  [  'enrollment_chart',  ]}),\
                    ]
admin.site.register(Loan, LoanAdmin)