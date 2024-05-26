from django.shortcuts import render, redirect
from decouple import config, Csv
from django.http import HttpResponse, JsonResponse
import requests
from django import forms
import pandas as pd
from .models import Variable
from django.http import HttpResponseNotAllowed
from services.rapid7_service import Rapid7Service

RAPID7_SERVICE = Rapid7Service()

def main_menu(request):
    return render(request, 'main_menu.html')

def index(request):
    information = {"name":"index"}
    return render(request, "index.html", information)


def variables_view(request):
    variables = RAPID7_SERVICE.view_all_variables()
    return render(request, 'variables.html', {'variables': variables})

def new_variable(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        value = request.POST.get('value')

        if not all([name, description, value]):
            return JsonResponse({"status": "error", "message": "All fields are required!"})

        API_KEY = config('RAPID7_KEY')
        
        api_url = "https://us.rest.logs.insight.rapid7.com/query/variables"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": API_KEY
        }
        data = {
            "variable": {
                "name": name,
                "description": description,
                "value": value
            }
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()  # Extract JSON response content
            if response.status_code == 201:
                return JsonResponse({"status": "success", "message": "Variable created successfully!", "data": response_data})
            else:
                return JsonResponse({
                    "status": "error", 
                    "message": response_data.get("message", "Failed to create variable!"),
                    "response_code": response.status_code,
                    "details": response_data
                })
        except requests.RequestException as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return render(request, 'new_variable.html')


def find_variable(request):
    variable_details = None
    if request.method == "POST":
        variable_id = request.POST.get('variable_id')

        if not variable_id:
            return JsonResponse({"status": "error", "message": "Variable ID is required!"})

        API_KEY = config('RAPID7_KEY')
        
        api_url = f"https://us.rest.logs.insight.rapid7.com/query/variables/{variable_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": API_KEY
        }

        try:
            response = requests.get(api_url, headers=headers)
            response_data = response.json()  # Extract JSON response content
            if response.status_code == 200:
                variable_details = response_data
                print("variable_details.id here: ",variable_details['variable']['id'])
            else:
                return JsonResponse({
                    "status": "error", 
                    "message": response_data.get("message", "Failed to retrieve variable!"),
                    "response_code": response.status_code,
                    "details": response_data
                })
        except requests.RequestException as e:
            return JsonResponse({"status": "error", "message": str(e)})
        except ValueError:  # Handle cases where response has no content
            return JsonResponse({
                "status": "error", 
                "message": "Failed to retrieve variable!",
                "response_code": response.status_code
            })
    
    return render(request, 'find_variable.html', {'variable_details': variable_details})

def update_variable(request):
    if request.method == "POST":
        variable_id = request.POST.get('variable_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        value = request.POST.get('value')

        if not all([variable_id, name, description, value]):
            return JsonResponse({"status": "error", "message": "All fields are required!"})

        API_KEY = config('RAPID7_KEY')

        api_url = f"https://us.rest.logs.insight.rapid7.com/query/variables/{variable_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": API_KEY
        }
        data = {
            "variable": {
                "name": name,  # Include the name in the request body
                "description": description,
                "value": value
            }
        }

        try:
            # Use the PUT method to update the variable
            response = requests.put(api_url, headers=headers, json=data)
            response_data = response.json()  # Extract JSON response content
            if response.status_code == 200:
                return JsonResponse({"status": "success", "message": "Variable updated successfully!", "data": response_data})
            else:
                return JsonResponse({
                    "status": "error", 
                    "message": response_data.get("message", "Failed to update variable!"),
                    "response_code": response.status_code,
                    "details": response_data
                })
        except requests.RequestException as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return render(request, 'update_variable.html')

class VariableUploadForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=255, required=False)
    excel_file = forms.FileField()

def upload_variables(request):
    if request.method == "POST":
        form = VariableUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            excel_file = request.FILES['excel_file']

            try:
                df = pd.read_excel(excel_file)
                # Flatten all values and filter out any NaN values, then join them with commas
                values = df.values.flatten()
                values = [str(v) for v in values if pd.notna(v)]
                concatenated_values = ", ".join(values)
            except Exception as e:
                return JsonResponse({"status": "error", "message": "Failed to read Excel file: " + str(e)})

            API_KEY = config('RAPID7_KEY')
            api_url = "https://us.rest.logs.insight.rapid7.com/query/variables"
            headers = {
                "Content-Type": "application/json",
                "X-Api-Key": API_KEY
            }
            
            data = {
                "variable": {
                    "name": name,
                    "description": description,
                    "value": concatenated_values
                }
            }

            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code == 201:
                response_data = response.json()
                Variable.objects.create(
                    name=name,
                    description=description,
                    value=concatenated_values
                )
                return JsonResponse({"status": "success", "message": "Variable created successfully!", "data": response_data})
            else:
                response_data = response.json()
                return JsonResponse({
                    "status": "error", 
                    "message": response_data.get("message", "Failed to create variable!"),
                    "response_code": response.status_code,
                    "details": response_data
                })
        else:
            return render(request, 'upload_variables.html', {'form': form})
    else:
        form = VariableUploadForm()
        return render(request, 'upload_variables.html', {'form': form})

# REFACTOR THIS FUNCTION 
def delete_variable_direct(request, variable_id):
    # Check if the request method is POST
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])  # Return HTTP 405 Method Not Allowed if not POST

    # Proceed with your deletion logic
    API_KEY = config('RAPID7_KEY')
    api_url = f"https://us.rest.logs.insight.rapid7.com/query/variables/{variable_id}"
    headers = {
        'x-api-key': API_KEY,
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

# updated 
def delete_variable_view(request):
    if request.method == "POST":
        variable_id = request.POST.get('variable_id')

        if not variable_id:
            return JsonResponse({"status": "error", "message": "Variable ID is required!"})
        # service method invoked
        RAPID7_SERVICE.delete_variable_by_id(variable_id)    
    return render(request, 'delete_variable_view.html')
