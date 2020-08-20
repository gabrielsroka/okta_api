import requests

url = '...'
token = '...'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

user = {
    'profile': {
        'firstName': 'Python',
        'lastName': 'Rules',
        'email': 'python@example.com',
        'login': 'python@example.com'
    }
}
res = requests.post(f'{url}/api/v1/users', json=user, headers=headers)
print(res.ok)
