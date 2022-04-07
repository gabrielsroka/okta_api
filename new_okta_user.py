import requests

# Set these:
url = '...'
token = '...'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

user = {
    'profile': {
        'firstName': 'Python',
        'lastName': 'Rules',
        'email': 'python@example.com',
        'login': 'python@example.com'
    }
}
res = session.post(f'{url}/api/v1/users', json=user, headers=headers)
print(res.ok)
