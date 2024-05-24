from django.shortcuts import render
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

    return render(request, 'list_all_logsets.html', {'logsets': logsets})

def query_home(request):
    information = {"name": "Search_app Home Page"}
    return render(request, "search_app.html", information)