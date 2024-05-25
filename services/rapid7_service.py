# services/rapid7_services.py
import json
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config
from urllib3 import PoolManager
from django.http import HttpResponse, JsonResponse
import requests

class Rapid7Service:
    
    BASE_URL = "https://us.api.insight.rapid7.com"  # Base URL for the Rapid7 API
    API_KEY = config('RAPID7_KEY')

    def delete_variable_by_id(self,variable_id):
        # Delete variable by id

        api_url = f"https://us.rest.logs.insight.rapid7.com/query/variables/{variable_id}"
        headers = {
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/json',
        }
        response = requests.delete(api_url, headers=headers)
        if response.status_code == 204:
            return JsonResponse({"status": "success", "message": "Variable deleted successfully"})
        else:
            response_data = response.json()
            return JsonResponse({
                "status": "error", 
                "message": response_data.get("message", "Failed to delete variable"),
                "response_code": response.status_code,
                "details": response_data
            })

    def view_all_variables(self):

        base_url = "https://us.rest.logs.insight.rapid7.com/query/variables"
        headers = {
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/json',
        }
        response = requests.get(base_url, headers=headers)
        variables = response.json() 
        return variables       


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
            logset_dict = {}

            if "logsets" in logsets_data and len(logsets_data["logsets"]) > 0:
                for logset in logsets_data["logsets"]:
                    for log in logset["logs_info"]:
                        log_name = log["name"]
                        log_id = log["id"]
                        logset_dict[log_name] = log_id
                return logset_dict
            else:
                return {"error": "No log sets found."}
        else:
            return {"error": "Failed to fetch log sets."}


    def http_request(self, method, url, headers=None, body=None):
        # Utility function to make HTTP requests
        http = PoolManager()
        response = http.request(method, url, headers=headers, body=body)
        return response

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

    def create_query_url(self, logset_id, time_range, leql):
        # Creates the query URL for the logs
        query_url = f"{self.BASE_URL}/log_search/query/logs/{logset_id}?time_range={time_range}&query={leql}"
        return query_url

    def get_log_set_by_name(self, log_set_name):
        # Get log set ID by name
        logsets = self.list_all_logsets()
        # this gets just the sub log_sets only 
        if "error" in logsets:
            return {"error": logsets["error"]}
        
        if log_set_name in logsets:
            return {"id": logsets[log_set_name]}
        else:
            return {"error": "ID cannot be found"}
