import requests

# Set these:
org_url = 'https://EXAMPLE.okta.com'
token = '...'
filename = 'mappings.json'

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
            mappings.append(r.text)
    with open(filename, 'w') as f:
        f.write('[')
        f.write(',\n'.join(mappings))
        f.write(']')

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

main()
