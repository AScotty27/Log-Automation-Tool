# query_app/views.py
from django.shortcuts import render
from services.rapid7_service import Rapid7Service

RAPID7_SERVICE = Rapid7Service()

def query_app(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_app.html", information)

def list_all_logsets(request):
    logsets = RAPID7_SERVICE.list_all_logsets()
    return render(request, 'list_all_logsets.html', {'logsets': logsets})

def simple_log_query(request):
    query_url = None  # Initialize query_url to None

    log_set = 'Auth0-officeally-production'  # Default value
    time_range = 'last 1 day'  # Default value
    leql = 'calculate(count)'  # Default value

    if request.method == 'POST':  # Form gets submitted
        log_set = request.POST.get('log_set', log_set)
        time_range = request.POST.get('time_range', time_range)
        leql = request.POST.get('leql', leql)

        logset_id = RAPID7_SERVICE.get_logset_by_name(log_set)
        print("====================logset_id from ===================")
        print(log_set, logset_id)

        if logset_id:
            query_url = RAPID7_SERVICE.create_query_url(logset_id, time_range, leql)
        else:
            query_url = "Log ID not found"

        print(query_url)

    return render(request, 'simple_log_query.html', {"urlquery": query_url})
