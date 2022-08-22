"""Call Okta API. See https://developer.okta.com/docs/reference"""

import requests
from dotenv import load_dotenv # pip install python-dotenv
import os
import csv
from datetime import datetime
import time

load_dotenv()
# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
admin_url = url.replace('.', '-admin.', 1)
token = os.getenv('OKTA_API_TOKEN')

# If you're making multiple API calls, using a session is much faster.
session = requests.Session()
headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json',
    'User-Agent': session.headers['user-agent'] + ' ' + os.path.basename(__file__)
}
session.headers.update(headers)


# Apps - https://developer.okta.com/docs/reference/api/apps
def get_app(id):
    return session.get(f'{url}/api/v1/apps/{id}')

def get_apps(**params):
    return session.get(f'{url}/api/v1/apps', params=params)

def get_app_pages(**params):
    page = get_apps(**params) 
    while page:
        yield page
        page = get_next_page(page.links)    

def update_app(id, app):
    return session.put(f'{url}/api/v1/apps/{id}', json=app)

def get_app_schema(id):
    return session.get(f'{url}/api/v1/meta/schemas/apps/{id}/default')

def get_app_groups(id, **params):
    return session.get(f'{url}/api/v1/apps/{id}/groups', params=params)

def get_app_group_pages(id, **params):
    page = get_app_groups(id, **params)
    while page:
        yield page
        page = get_next_page(page.links, **params)

def get_app_users(id, **params):
    return session.get(f'{url}/api/v1/apps/{id}/users', params=params)

def get_app_user_pages(id, **params):
    page = get_app_users(id, **params)
    while page:
        yield page
        page = get_next_page(page.links, **params)

def update_app_user(app_id, user_id, user):
    return session.post(f'{url}/api/v1/apps/{app_id}/users/{user_id}', json=user)

def get_app_group_push(id):
    return session.get(f'{admin_url}/api/internal/instance/{id}/grouppush')

def assign_group_to_app(appid, groupid, group={}):
    return session.put(f'{url}/api/v1/apps/{appid}/groups/{groupid}', json=group)


# Factors - https://developer.okta.com/docs/reference/api/factors
def get_user_factors(id):
    return session.get(f'{url}/api/v1/users/{id}/factors')

def issue_user_factor_challenge(userid, factorid):
    return session.post(f'{url}/api/v1/users/{userid}/factors/{factorid}/verify')


# Groups - https://developer.okta.com/docs/reference/api/groups
def new_group(group):
    return session.post(f'{url}/api/v1/groups', json=group)

def get_groups(**params):
    """Get Okta groups.
    **params: such as `q`, `filter`, `limit`, etc. 
    
    see https://developer.okta.com/docs/reference/api/groups/#list-groups
    """
    return session.get(f'{url}/api/v1/groups', params=params)

def get_group(id):
    return session.get(f'{url}/api/v1/groups/{id}')

def update_group(id, group):
    return session.put(f'{url}/api/v1/groups/{id}', json=group)

def delete_group(id):
    return session.delete(f'{url}/api/v1/groups/{id}')

def add_group_member(groupid, userid):
    return session.put(f'{url}/api/v1/groups/{groupid}/users/{userid}')


# Mappings - https://developer.okta.com/docs/reference/api/mappings
def get_mapping(id):
    return session.get(f'{url}/api/v1/mappings/{id}')

def get_mappings(**params):
    return session.get(f'{url}/api/v1/mappings', params=params)


# Users - https://developer.okta.com/docs/reference/api/users
def get_user(id):
    return session.get(f'{url}/api/v1/users/{id}')

def get_users(**params):
    """Get Okta users.
    
    **params: such as `q`, `filter`, `search`, `limit`, etc. 
    
    see https://developer.okta.com/docs/reference/api/users/#list-users
    """
    return session.get(f'{url}/api/v1/users', params=params)

def get_user_pages(**params):
    page = get_users(**params) 
    while page:
        yield page
        page = get_next_page(page.links)    


# Util
def get_next_page(links, **params):
    next = links.get('next')
    if next:
        return session.get(next['url'], params=params)
    else:
        return None

def get_limit(r):
    limit = int(r.headers['X-Rate-Limit-Limit'])
    remaining = int(r.headers['X-Rate-Limit-Remaining'])
    reset = datetime.utcfromtimestamp(int(r.headers['X-Rate-Limit-Reset']))
    return limit, remaining, reset

def snooze(r, LIMIT_REMAINING):
    limit, remaining, reset = get_limit(r)
    now = datetime.utcnow()
    if remaining < LIMIT_REMAINING:
        print('sleeping...')
        while reset > now:
            time.sleep(1)
            now = datetime.utcnow()

def import_csv(filename):
    with open(filename) as f:
        return [object for object in csv.DictReader(f)]

def export_csv(filename, rows, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


# Python requests: , proxies={'https': '127.0.0.1:8888'}, verify='./fiddler.cer'
# pwsh: ${env:HTTPS_PROXY}='127.0.0.1:8888'; ${env:REQUESTS_CA_BUNDLE}='./fiddler.cer'
# .env: HTTPS_PROXY=127.0.0.1:8888; REQUESTS_CA_BUNDLE=./fiddler.cer
