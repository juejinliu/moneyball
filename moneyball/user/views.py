from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    return render_to_response('index.html')

def registe(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/welcome")
        else:
            # Show an error page
            return render_to_response("registe.html")
    else:
        return render_to_response("registe.html")