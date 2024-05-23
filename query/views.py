from django.shortcuts import render, redirect
from decouple import config, Csv
from django.http import HttpResponse
import requests
from django.conf import settings
# Create your views here.

def query(request):
    SECRET_POTATO = config('SECRET_POTATO')
    print('views secret potato is: ', SECRET_POTATO)
    information = {"name":"query","secret_potato":SECRET_POTATO}
    print("information is: ",information)
    return render(request, "query.html", information)
