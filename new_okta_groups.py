from dotenv import load_dotenv
import requests
import os

load_dotenv()
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

names = ['Finance', 'Legal']
for name in names:
    group = {
        'profile': {
            'name': name,
            'description': ''
        }
    }
    res = session.post(f'{url}/api/v1/groups', json=group)
    print(res.ok)
