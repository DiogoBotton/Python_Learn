import os
import requests
from requests.auth import HTTPBasicAuth

# Variáveis de ambiente
organization_url = os.getenv('AZURE_DEVOPS_URL')
token = os.getenv('AZURE_DEVOPS_TOKEN')
task_id = os.getenv('BUILD_SOURCEVERSIONMESSAGE')

# URL da API do Azure DevOps
url = f'{organization_url}/_apis/wit/workitems/{task_id}?api-version=6.0'

# Cabeçalhos e dados da requisição
headers = {
    'Content-Type': 'application/json-patch+json'
}

data = [
    {
        "op": "add",
        "path": "/fields/System.State",
        "value": "Active"
    }
]

# Fazendo a requisição para atualizar a task
response = requests.patch(
    url,
    auth=HTTPBasicAuth('', token),
    headers=headers,
    json=data
)

# Verifica o resultado da requisição
if response.status_code == 200:
    print("Task updated successfully.")
else:
    print(f"Failed to update task: {response.status_code}")
    print(response.json())
