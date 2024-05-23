from django.shortcuts import render
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config

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
        logsets_data = response.json()
        if "logsets" in logsets_data and len(logsets_data["logsets"]) > 0:
            first_log = logsets_data["logsets"][0]
            print("================================================================")
            print(json.dumps(first_log, indent=4))
            print("================================================================")
            logsets = {"logsets": logsets_data["logsets"]}
        else:
            logsets = {"error": "No log sets found."}
    else:
        logsets = {"error": "Failed to fetch log sets."}

    return render(request, 'alllogsets.html', {'logsets': logsets})

def query_home(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_home.html", information)

def find_logset_by_id(request):
    logset_name = None
    error = None

    if request.method == 'POST':
        logset_id = request.POST.get('logset_id')
        if logset_id:
            API_KEY = config('RAPID7_KEY')
            DATA_STORAGE_REGION = 'US'

            session = Session()
            session.mount(
                f'https://{DATA_STORAGE_REGION}.rest.logs.insight.rapid7.com',
                HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]))
            )

            response = session.get(f"https://{DATA_STORAGE_REGION}.rest.logs.insight.rapid7.com/management/logsets/{logset_id}",
                                   headers={'x-api-key': API_KEY})

            if response.status_code == 200:
                logset_data = response.json()
                logset_name = logset_data.get('name')
            else:
                error = "Failed to fetch the log set."

    return render(request, 'find_logset.html', {'logset_name': logset_name, 'error': error})
