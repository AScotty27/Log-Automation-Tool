import json
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config

class Rapid7Service:
    def __init__(self):
        self.api_key = config('RAPID7_KEY')
        self.data_storage_region = 'US'  # Swap for your region
        self.session = Session()
        self.session.mount(
            f'https://{self.data_storage_region}.rest.logs.insight.rapid7.com',
            HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]))
        )

    def list_all_logsets(self):
        """
        Fetch all log sets from Rapid7.

        :return: Dictionary with log sets data or an error message.
        """
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
