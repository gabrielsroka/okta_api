"""Import a user with unsalted sha1 hash into Okta."""

import hashlib
import base64
import requests
from dotenv import load_dotenv
import os

username = 'sha1py@okta.local'
password = 'P@ssword123'

sha1 = hashlib.sha1(password.encode()).digest()
b64_sha1 = base64.b64encode(sha1).decode()
print('b64_sha1:', b64_sha1)

load_dotenv()
# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

user = {
    'profile': {
        'firstName': 'Isaac',
        'lastName': 'Brock',
        'email': username,
        'login': username
    },
    'credentials': {
        'password': {
            'hash': {
                'algorithm': 'SHA-1',
                'value': b64_sha1
            }
        }
    }
}

# Create the user.
response = requests.post(f'{url}/api/v1/users', json=user, headers=headers)
print(response.json())

# Now, sign in as the user to verify the password hash was imported correctly.
response = requests.post(f'{url}/api/v1/authn', json={'username': username, 'password': password})
authn = response.json()
if response.ok:
    print(authn['status'])
else:
    print(authn['errorSummary'])
