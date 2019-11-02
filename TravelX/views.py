from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import Account

def home(request):
    return render(request,'Index.html')
def test(request,slug):
    return HttpResponse(slug)