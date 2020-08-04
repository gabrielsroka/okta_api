from dotenv import load_dotenv
import requests
import os

load_dotenv()
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

headers = {
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json'
}

names = ['Finance', 'Legal']
for name in names:
    group = {
        'profile': {
            'name': name,
            'description': ''
        }
    }
    res = requests.post(url + '/api/v1/groups', json=group, headers=headers)
    print(res.ok)
