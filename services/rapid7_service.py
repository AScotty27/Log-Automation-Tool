import json
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config
from urllib3 import PoolManager

class Rapid7Service:
    
    BASE_URL = "https://us.api.insight.rapid7.com"  # Base URL for the Rapid7 API
    
    def __init__(self):
        self.api_key = config('RAPID7_KEY')
        self.data_storage_region = 'US'  # Data storage region
        self.session = Session()
        self.session.mount(
            f'https://{self.data_storage_region}.rest.logs.insight.rapid7.com',
            HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]))
        )

    def list_all_logsets(self):
        # Fetch all log sets from Rapid7
        response = self.session.get(
            f"https://{self.data_storage_region}.rest.logs.insight.rapid7.com/management/logsets",
            headers={'x-api-key': self.api_key}
        )
        
        if response.status_code == 200:
            logsets_data = response.json()
            if "logsets" in logsets_data and len(logsets_data["logsets"]) > 0:
                return {"logsets": logsets_data["logsets"]}
            else:
                return {"error": "No log sets found."}
        else:
            return {"error": "Failed to fetch log sets."}

    def http_request(self, method, url, headers=None, body=None):
        # Utility function to make HTTP requests
        http = PoolManager()
        response = http.request(method, url, headers=headers, body=body)
        return response

    def get_logs(self, log_set):
        # Fetches log IDs based on predefined log names, enter the log name and get the log
        url = f"{self.BASE_URL}/management/logs/"
        headers = {"x-api-key": self.api_key}
        response = self.http_request("GET", url, headers=headers)
    
        if response.status == 200:
            json_object = json.loads(response.data)
            for log in json_object['logs']:
                if log['name'] == log_set:
                    return log['id']
        return None

    def run_query(self, url):
        # Executes a LEQL query and handles pagination if necessary
        headers = {"x-api-key": self.api_key}
        response = self.http_request("GET", url, headers=headers)
    
        if response.status == 202:
            json_object = json.loads(response.data)
            continue_url = json_object['links'][0]['href']
            return self.run_query(continue_url)
        elif response.status == 200:
            return json.loads(response.data)
        else:
            return {"error": f"Error: {response.status}, {response.data}"}

    def search_logs(self, log_set, time_range, leql):
        # Searches logs using the specified parameters
        log_id = self.get_logs(log_set)
        if log_id:
            query_url = f"{self.BASE_URL}/query/logs/{log_id}?time_range={time_range}&query={leql}"
            return self.run_query(query_url)
        else:
            return {"error": "Log ID not found"}
