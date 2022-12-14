"""Call Okta APIs using Session (cookies) and xsrfToken -- just like a browser. SSWS API Token is not needed.

### CAUTION: Code to call private APIs is not supported by Okta. The APIs can change at any time.
###          Test in a dev or oktapreview tenant before trying this in production.

This will work with users who have Push MFA. This won't work if Apps > Apps > "Okta Admin Console" > Sign On Policy > MFA is enabled.
"""

import requests
import getpass
import time
import re
from dotenv import load_dotenv
import os

load_dotenv()
# Store these in a local .env file.
okta_url = os.getenv('OKTA_ORG_URL') # eg https://XXX.okta.com
username = os.getenv('OKTA_USERNAME')

okta_admin_url = okta_url.replace('.', '-admin.', 1)

# A session uses cookies and reuses the HTTP connection.
session = requests.Session()

def main():
    sign_in()
    user = get_user('me')
    admin_xsrf_token = admin_sign_in()
    send_notification(admin_xsrf_token, user['id'])
    get_user_factors(user['id'])

def sign_in():
    print('URL:', okta_url)
    print('Username:', username)
    password = getpass.getpass()

    print('Signing in...')
    response = session.post(f'{okta_url}/api/v1/authn', json={'username': username, 'password': password})
    authn = response.json()
    if not response.ok:
        print(authn['errorSummary'])
        exit()

    if authn['status'] == 'MFA_REQUIRED':
        token = send_push(authn['_embedded']['factors'], authn['stateToken'])
    else:
        token = authn['sessionToken']

    session.get(f'{okta_url}/login/sessionCookieRedirect?redirectUrl=/&token={token}' )

def send_push(factors, state_token):
    print('Push MFA...')
    push_factors = [f for f in factors if f['factorType'] == 'push']
    if not push_factors:
        print('Push factor not found')
        exit()
    push_url = push_factors[0]['_links']['verify']['href']
    while True:
        authn = session.post(push_url, json={'stateToken': state_token}).json()
        if authn['status'] == 'SUCCESS':
            return authn['sessionToken']
        result = authn['factorResult']
        if result == 'WAITING':
            time.sleep(4) # 4 seconds
            print('Waiting...')
        elif result in ['REJECTED', 'TIMEOUT']:
            print('Push rejected')
            exit()

def admin_sign_in():
    response = session.get(f'{okta_url}/home/admin-entry')

    # old style
    match = re.search(r'"token":\["(.*)"\]', response.text)
    if match:
        body = {'token': match.group(1)}
        response = session.post(f'{okta_admin_url}/admin/sso/request', data=body)

    # new style (w/ new OIDC flow)
    match = re.search(r'<span.* id="_xsrfToken">(.*)</span>', response.text)
    if not match:
        print('admin_sign_in: token not found. Go to Apps > Apps > "Okta Admin Console" > Sign On Policy and disable MFA.')
        exit()
    admin_xsrf_token = match.group(1)
    return admin_xsrf_token

def send_notification(admin_xsrf_token, userid):
    body = {
        'message': 'testing 1125',
        'target': 'GROUPS_AND_USERS', # or EVERYONE
        'users': [userid],
        'groups': []
    }
    headers = {'X-Okta-XsrfToken': admin_xsrf_token}
    notification = session.post(f'{okta_admin_url}/api/internal/admin/notification', json=body, headers=headers).json()
    print('\nNotification:')
    print(notification)

def get_user(userid):
    user = session.get(f'{okta_url}/api/v1/users/{userid}').json()
    print('\nUser:')
    print(user)
    return user

def get_user_factors(userid):
    factors = session.get(f'{okta_url}/api/v1/users/{userid}/factors').json()
    print('\nFactors:')
    print(factors)

main()
