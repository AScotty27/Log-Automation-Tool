from django.shortcuts import render
from .search_logs import get_logs, run_query  # Import the functions from the search_logs file
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config
import json


REGION = 'us'  # Swap for your region
BASE_URL = f"https://{REGION}.api.insight.rapid7.com/log_search"

def list_all_logsets(request):
    API_KEY = config('RAPID7_KEY')
    DATA_STORAGE_REGION = 'US'  # Swap for your region

    session = Session()
    session.mount(
        f'https://{DATA_STORAGE_REGION}.rest.logs.insight.rapid7.com',
        HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]))
    )

    response = session.get(f"https://{DATA_STORAGE_REGION}.rest.logs.insight.rapid7.com/management/logsets",
                           headers={'x-api-key': API_KEY})
    
    if response.status_code == 200:
        logsets_data = response.json()  # Convert the response to a Python dictionary
        if "logsets" in logsets_data and len(logsets_data["logsets"]) > 0:
            logsets = {"logsets": logsets_data["logsets"]}
        else:
            logsets = {"error": "No log sets found."}
    else:
        logsets = {"error": "Failed to fetch log sets."}

    return render(request, 'alllogsets.html', {'logsets': logsets})

def query_home(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_home.html", information)

def search_logs(request):

    logs_result = None
    error = None

    log_set = 'Auth0-officeally-production'
    time_range = 'last 1 day'
    leql = 'calculate(count)'

    if request.method == 'POST':
        log_set = request.POST.get('log_set', log_set)
        time_range = request.POST.get('time_range', time_range)
        leql = request.POST.get('leql', leql)

        log_id = get_logs(log_set)
        if log_id:
            query_url = f"{BASE_URL}/query/logs/{log_id}?time_range={time_range}&query={leql}"
            logs_result = run_query(query_url)
        else:
            error = "Log ID not found"

    return render(request, 'search_logs.html', {
        'logs_result': logs_result,
        'error': error,
        'log_set': log_set,
        'time_range': time_range,
        'leql': leql
    })
