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
    response = None  # Initialize response to None

    log_set_name = 'Auth0-officeally-production'  # Default value
    time_range = 'last 1 day'  # Default value
    leql = 'calculate(count)'  # Default value

    if request.method == 'POST':  # Form gets submitted
        log_set_name = request.POST.get('log_set', log_set_name)
        time_range = request.POST.get('time_range', time_range)
        leql = request.POST.get('leql', leql)

        logset_id_response = RAPID7_SERVICE.get_log_set_by_name(log_set_name)

        if "id" in logset_id_response:
            query_url = RAPID7_SERVICE.create_query_url(logset_id_response["id"], time_range, leql)

            response = RAPID7_SERVICE.run_query(query_url)
        else:
            response = {"error": logset_id_response["error"]}

    return render(request, 'simple_log_query.html', {"urlquery": response})
