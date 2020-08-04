import requests

url = '...'
token = '...'

headers = {
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json'
}

res = requests.get(url + '/api/v1/users/me', headers=headers)
if res.ok:
    user = res.json()
    print(user)
