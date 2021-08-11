import re
import time
import settings
import sys

from requests import Session
from tabulate import tabulate


def sign_in(session: Session):
    print('Signing in...')
    
    response = session.post(
        f'{settings.OKTA_ORG_URL}/api/v1/authn',
        json={
            'username': settings.OKTA_USERNAME,
            'password': settings.OKTA_PASSWORD
        }
    )

    authn = response.json()
    if not response.ok:
        print(authn['errorSummary'])
        sys.exit()

    if authn['status'] == 'MFA_REQUIRED':
        token = send_push(session, authn['_embedded']['factors'], authn['stateToken'])
    else:
        token = authn['sessionToken']

    session.get(f'{settings.OKTA_ORG_URL}/login/sessionCookieRedirect?redirectUrl=/&token={token}')


def send_push(session: Session, factors: dict, state_token: str):
    print('Push MFA...')
    push_factor = next(f for f in factors if f['factorType'] == 'push')
    
    if not push_factor:
        print('Push factor not found')
        sys.exit()

    push_url = push_factor['_links']['verify']['href']
    
    while True:
        authn = session.post(push_url, json={'stateToken': state_token}).json()
        authn_status = authn.get('status')
        factor_result = authn.get('factorResult')
        
        if authn_status == 'SUCCESS':
            return authn['sessionToken']
        elif factor_result == 'WAITING':
            time.sleep(4)
            print('Waiting...')
        elif factor_result in ['REJECTED', 'TIMEOUT']:
            print('Push rejected')
            sys.exit()


def get_admin_xsrf_token(session: Session):
    response = session.get(f'{settings.OKTA_ORG_URL}/home/admin-entry')

    # new style (w/ new OIDC flow)
    match = re.search(r'<span.* id="_xsrfToken">(.*)</span>', response.text)
    if not match:
        print('admin_sign_in: token not found. Go to "Apps > Apps > Okta Admin Console" > Sign On Policy and disable MFA.')
        sys.exit()
    
    admin_xsrf_token = match.group(1)
    return admin_xsrf_token