from django.shortcuts import render
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config
import json  # Import the json module

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
            first_log = logsets_data["logsets"][0]
            print("================================================================")
            print(json.dumps(first_log, indent=4))  # Print the first log set with pretty formatting
            print("================================================================")
            logsets = {"logsets": logsets_data["logsets"]}
        else:
            logsets = {"error": "No log sets found."}
    else:
        logsets = {"error": "Failed to fetch log sets."}

    return render(request, 'alllogsets.html', {'logsets': logsets})

def query(request):
    SECRET_POTATO = config('SECRET_POTATO')
    print('views secret potato is: ', SECRET_POTATO)
    information = {"name": "query", "secret_potato": SECRET_POTATO}
    print("information is: ", information)
    return render(request, "query.html", information)
