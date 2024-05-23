from django.shortcuts import render
from urllib3 import PoolManager
from decouple import config
import json

API_KEY = config('RAPID7_KEY')
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

def query_home(request):
    information = {"name": "Query Home Page"}
    return render(request, "query_home.html", information)

def http_request(method, url, headers=None, body=None):
    """Utility function to make HTTP requests."""
    http = PoolManager()
    response = http.request(method, url, headers=headers, body=body)
    return response

def get_logs(log_set):
    """Fetches log IDs based on predefined log names."""
    url = f"{BASE_URL}/management/logs/"
    headers = {"x-api-key": API_KEY}
    response = http_request("GET", url, headers=headers)
   
    if response.status == 200:
        json_object = json.loads(response.data)
        for log in json_object['logs']:
            if log['name'] == log_set:
                return log['id']
    return None

def run_query(url):
    """Executes a LEQL query and handles pagination if necessary."""
    headers = {"x-api-key": API_KEY}
    response = http_request("GET", url, headers=headers)
   
    if response.status == 202:
        json_object = json.loads(response.data)
        continue_url = json_object['links'][0]['href']
        return run_query(continue_url)
    elif response.status == 200:
        return json.loads(response.data)
    else:
        return {"error": f"Error: {response.status}, {response.data}"}

def search_logs(request):
    logs_result = None
    error = None

    if request.method == 'POST':
        log_set = request.POST.get('log_set', 'Auth0-officeally-production')
        time_range = request.POST.get('time_range', 'last 1 day')
        leql = request.POST.get('leql', 'calculate(count)')

        log_id = get_logs(log_set)
        if log_id:
            query_url = f"{BASE_URL}/query/logs/{log_id}?time_range={time_range}&query={leql}"
            logs_result = run_query(query_url)
        else:
            error = "Log ID not found"

    return render(request, 'search_logs.html', {'logs_result': logs_result, 'error': error})
