from django.shortcuts import render
from services.rapid7_service import Rapid7Service

def list_all_logsets(request):
    rapid7_service = Rapid7Service()
    logsets = rapid7_service.list_all_logsets()
    return render(request, 'list_all_logsets.html', {'logsets': logsets})

def search_logs_1(request):
    logs_result = None
    error = None

    log_set = 'Auth0-officeally-production'
    time_range = 'last 1 day'
    leql = 'calculate(count)'

    if request.method == 'POST':
        log_set = request.POST.get('log_set', log_set)
        time_range = request.POST.get('time_range', time_range)
        leql = request.POST.get('leql', leql)

        rapid7_service = Rapid7Service()
        logs_result = rapid7_service.search_logs(log_set, time_range, leql)

        if 'error' in logs_result:
            error = logs_result['error']

    return render(request, 'search_logs_1.html', {
        'logs_result': logs_result,
        'error': error,
        'log_set': log_set,
        'time_range': time_range,
        'leql': leql
    })

def query_app(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_app.html", information)
