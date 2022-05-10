from dotenv import load_dotenv
import os
import requests

load_dotenv()
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

oldGroupId = '00g9raeyraaWXn1zF0h7'
newGroupId = '00goz2pusnPu0lRCB0h7'
group_rule = {
    'type': 'group_rule',
    'name': 'a Python rules 12',
    'conditions': {
        'expression': {
            'value': f"isMemberOfAnyGroup('{oldGroupId}')",
            'type': 'urn:okta:expression:1.0'
        }
    },
    'actions': {
        'assignUserToGroups': {
            'groupIds': [
                newGroupId
            ]
        }
    }
}
res = session.post(f'{url}/api/v1/groups/rules', json=group_rule)
print(res.ok)
