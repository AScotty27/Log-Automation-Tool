from django.shortcuts import render

# Create your views here.

def search_app(requests):
    return render(requests, "search_app.html",{"name":"search_app"})