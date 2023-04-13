import requests

# Set these:
org_url = '...'
token = '...'

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

user = {
    'profile': {
        'firstName': 'Python',
        'lastName': 'Rules',
        'email': 'python@example.com',
        'login': 'python@example.com'
    }
}
res = session.post(org_url + '/api/v1/users', json=user)
print(res.ok)
