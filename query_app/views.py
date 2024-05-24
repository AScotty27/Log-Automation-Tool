from django.shortcuts import render
from services.rapid7_service import Rapid7Service

def list_all_logsets(request):
    rapid7_service = Rapid7Service()
    logsets = rapid7_service.list_all_logsets()
    return render(request, 'list_all_logsets.html', {'logsets': logsets})

def query_app(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_app.html", information)
