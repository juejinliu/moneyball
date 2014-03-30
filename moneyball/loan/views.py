from django.shortcuts import render,render_to_response
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render_to_response('loanindex.html')


