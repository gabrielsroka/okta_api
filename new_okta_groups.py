import requests

# Set these:
org_url = '...'
token = '...'

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

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
