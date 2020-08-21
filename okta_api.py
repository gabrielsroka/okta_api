"""Call Okta API. See https://developer.okta.com/docs/reference"""

import requests
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
import time

load_dotenv()
# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

session = requests.Session()

# Apps - https://developer.okta.com/docs/reference/api/apps
def get_apps(**kwargs):
    return session.get(f'{url}/api/v1/apps', params=kwargs, headers=headers)

def get_app_pages(**kwargs):
    page = get_apps(**kwargs) 
    while page:
        yield page
        page = get_next_page(page.links)    

def get_app_schema(id):
    return session.get(f'{url}/api/v1/meta/schemas/apps/{id}/default', headers=headers)

def get_app_groups(id, **kwargs):
    return session.get(f'{url}/api/v1/apps/{id}/groups', params=kwargs, headers=headers)

def get_app_group_pages(id, **kwargs):
    page = get_app_groups(id, **kwargs) 
    while page:
        yield page
        page = get_next_page(page.links, **kwargs)    


# Groups - https://developer.okta.com/docs/reference/api/groups
def new_group(group):
    return session.post(f'{url}/api/v1/groups', json=group, headers=headers)

def get_groups(**kwargs):
    """Get Okta groups.

    **kwargs: such as `q`, `filter`, `limit`, etc. 
    
    see https://developer.okta.com/docs/reference/api/groups/#list-groups
    """
    return session.get(f'{url}/api/v1/groups', params=kwargs, headers=headers)

def get_group(id):
    return session.get(f'{url}/api/v1/groups/{id}', headers=headers)

def delete_group(id):
    return session.delete(f'{url}/api/v1/groups/{id}', headers=headers)

def add_group_member(groupid, userid):
    return session.put(f'{url}/api/v1/groups/{groupid}/users/{userid}', headers=headers)


# Mappings - https://developer.okta.com/docs/reference/api/mappings
def get_mapping(id):
    return session.get(f'{url}/api/v1/mappings/{id}', headers=headers)

def get_mappings(**kwargs):
    return session.get(f'{url}/api/v1/mappings', params=kwargs, headers=headers)


# Users - https://developer.okta.com/docs/reference/api/users
def get_user(id):
    return session.get(f'{url}/api/v1/users/{id}', headers=headers)

def get_users(**kwargs):
    """Get Okta users.
    
    **kwargs: such as `q`, `filter`, `search`, `limit`, etc. 
    
    see https://developer.okta.com/docs/reference/api/users/#list-users
    """
    return session.get(f'{url}/api/v1/users', params=kwargs, headers=headers)

def get_user_pages(**kwargs):
    page = get_users(**kwargs) 
    while page:
        yield page
        page = get_next_page(page.links)    


# Util
def get_next_page(links, **kwargs):
    next = links.get('next')
    if next:
        return session.get(next['url'], params=kwargs, headers=headers)
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
