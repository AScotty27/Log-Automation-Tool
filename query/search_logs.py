import json
from urllib3 import PoolManager
from decouple import config

API_KEY = config('RAPID7_KEY')
REGION = 'us'  # Swap for your region
BASE_URL = f"https://{REGION}.api.insight.rapid7.com/log_search"

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
