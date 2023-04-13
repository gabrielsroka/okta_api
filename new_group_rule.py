import requests

# Set these:
org_url = '...'
token = '...'

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

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
res = session.post(f'{org_url}/api/v1/groups/rules', json=group_rule)
print(res.ok)
