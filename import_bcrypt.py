"""Import a user with salted bcrypt hash into Okta."""

import bcrypt
import requests
from dotenv import load_dotenv
import os

def encode_bcrypt(password):
    """Create a Bcrypt password that Okta will accept"""
    rounds = 10 # 20 works, but takes over 1 minute.
    salt = bcrypt.gensalt(rounds)
    hashed = bcrypt.hashpw(password, salt)
    salt_only = salt.decode('utf-8').split('$')[3]
    value_only = hashed.decode('utf-8').split('$')[3].replace(salt_only, '')
    return {
        'algorithm': 'BCRYPT',
        'workFactor': rounds,
        'salt': salt_only,
        'value': value_only
    }

username = 'bcryptpy8@okta.local'
password = 'P@ssword123'

hash = encode_bcrypt(password.encode())
print('bcrypt hash', hash)

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
            'hash': hash
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
