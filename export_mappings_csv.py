"""
pip install requests # or pip3
pip install python-dotenv
"""

import requests
from dotenv import load_dotenv
import os
import csv

load_dotenv()

# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

filename = 'mappings.csv'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

def main():
    mappings = []
    pages = 0
    for page in get_mapping_pages():
        pages += 1
        print('Fetching page', pages)
        for mapping in page.json():
            r = get_mapping(mapping['id'])
            map_d = r.json()
            props = map_d['properties']
            for prop in props:
                mappings.append({
                    'name': map_d['source']['name'],
                    'target': map_d['target']['name'],
                    'property': prop,
                    'expression': props[prop]['expression']
                })
    export_csv(filename, mappings, mappings[0].keys())

def get_mapping_pages(**kwargs):
    page = get_mappings(**kwargs) 
    while page:
        yield page
        page = get_next_page(page.links)  

def get_mapping(id):
    return session.get(f'{url}/api/v1/mappings/{id}')

def get_mappings(**kwargs):
    return session.get(f'{url}/api/v1/mappings', params=kwargs)

def get_next_page(links):
    next = links.get('next')
    if next:
        return session.get(next['url'])
    else:
        return None

def export_csv(filename, rows, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

main()
