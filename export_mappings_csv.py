import requests # pip install requests
import csv

# Set these:
org_url = 'https://EXAMPLE.okta.com'
token = '...'
filename = 'mappings.csv'

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

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

def get_mapping_pages(**params):
    page = get_mappings(**params) 
    while page:
        yield page
        page = get_next_page(page.links)  

def get_mapping(id):
    return session.get(f'{org_url}/api/v1/mappings/{id}')

def get_mappings(**params):
    return session.get(f'{org_url}/api/v1/mappings', params=params)

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
