import json
from urllib3 import PoolManager
from decouple import config

class Rapid7Service:
    def __init__(self):
        self.api_key = config('RAPID7_KEY')
        self.base_url = "https://us.rest.logs.insight.rapid7.com"
        self.http = PoolManager()

    def http_request(self, method, endpoint, headers=None, body=None):
        """
        Utility function to make HTTP requests.

        :param method: HTTP method as a string (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        :param endpoint: API endpoint as a string.
        :param headers: Dictionary of headers to include in the request.
        :param body: Request body as a string (default is None).
        :return: HTTP response object.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers.update({
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        })
        response = self.http.request(method, url, headers=headers, body=body)
        return response

    def create_variable(self, name, description, value):
        """
        Create a new variable.

        :param name: Name of the variable as a string.
        :param description: Description of the variable as a string.
        :param value: Value of the variable as a string.
        :return: HTTP response object.
        """
        data = {
            "variable": {
                "name": name,
                "description": description,
                "value": value
            }
        }
        body = json.dumps(data)
        response = self.http_request("POST", "query/variables", body=body)
        return response

    def delete_variable(self, variable_id):
        """
        Delete an existing variable.

        :param variable_id: ID of the variable to delete as a string.
        :return: HTTP response object.
        """
        response = self.http_request("DELETE", f"query/variables/{variable_id}")
        return response

    def find_variable_by_id(self, variable_id):
        """
        Find a variable by its ID.

        :param variable_id: ID of the variable to find as a string.
        :return: HTTP response object.
        """
        response = self.http_request("GET", f"query/variables/{variable_id}")
        return response

    def update_variable(self, variable_id, name, description, value):
        """
        Update an existing variable.

        :param variable_id: ID of the variable to update as a string.
        :param name: New name of the variable as a string.
        :param description: New description of the variable as a string.
        :param value: New value of the variable as a string.
        :return: HTTP response object.
        """
        data = {
            "variable": {
                "name": name,
                "description": description,
                "value": value
            }
        }
        body = json.dumps(data)
        response = self.http_request("PUT", f"query/variables/{variable_id}", body=body)
        return response
