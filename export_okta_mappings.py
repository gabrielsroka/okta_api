import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

filename = 'mappings.json'

headers = {
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json'
}

def main():
    mappings = []
    pages = 0
    for page in get_mapping_pages():
        pages += 1
        print('Fetching page', pages)
        for mapping in page.json():
            r = get_mapping(mapping['id'])
            mappings.append(r.text)
    with open(filename, 'w') as f:
        f.write('[')
        f.write(',\n'.join(mappings))
        f.write(']')

def get_mapping_pages(**kwargs):
    page = get_mappings(**kwargs) 
    while page:
        yield page
        page = get_next_page(page.links)  

def get_mapping(id):
    return requests.get(url + '/api/v1/mappings/' + id, headers=headers)

def get_mappings(**kwargs):
    return requests.get(url + '/api/v1/mappings', params=kwargs, headers=headers)

def get_next_page(links):
    next = links.get('next')
    if next:
        return requests.get(next['url'], headers=headers)
    else:
        return None

main()
