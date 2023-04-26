import requests

org_url = '...'
token = '...'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

res = requests.get(org_url + '/api/v1/users/me', headers=headers)
if res.ok:
    user = res.json()
    print(user)
