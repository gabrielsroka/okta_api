import requests

url = '...'
token = '...'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

res = requests.get(f'{url}/api/v1/users/me', headers=headers)
if res.ok:
    user = res.json()
    print(user)
