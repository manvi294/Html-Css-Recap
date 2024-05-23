#

import requests

tenant_id = 'YOUR_TENANT_ID'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
scope = 'https://graph.microsoft.com/.default'
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

token_r = requests.post(token_url, data=token_data)
token = token_r.json().get('access_token')


.


graph_api_url = 'https://graph.microsoft.com/v1.0/sites/root'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(graph_api_url, headers=headers)
sites = response.json()

print(sites)
