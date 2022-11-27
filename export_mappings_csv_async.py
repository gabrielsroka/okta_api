import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()

# Store these in a local .env file.
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')
limit = 75 # Concurrent rate limits are 15, 35, or 75.
LIMIT_REMAINING = 75

filename = 'mappings.csv'

headers = {
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
}

# globals
mappings = []
session = None

async def main():
    pages = 0
    global session
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async for page in get_mapping_pages():
                pages += 1
                print('Fetching page', pages)
                coros = (get_mapping(mapping['id']) for mapping in page)
                await asyncio.gather(*coros)
        except Exception as e:
            print(e)
    export_csv(filename, mappings, mappings[0].keys())

async def get_mapping(id):
    async with session.get(f'{url}/api/v1/mappings/{id}') as r:
        mapping = await r.json()
        props = mapping['properties']
        global mappings
        for prop in props:
            mappings.append({
                'name': mapping['source']['name'],
                'target': mapping['target']['name'],
                'property': prop,
                'expression': props[prop]['expression']
            })
        await snooze(r)

async def get_mapping_pages():
    page, links = await get_mappings() 
    while page:
        yield page
        page, links = await get_next_page(links)  

async def get_mappings():
    async with session.get(f'{url}/api/v1/mappings?limit={limit}') as page:
        return await page.json(), page.links

async def get_next_page(links):
    next = links.get('next')
    if next:
        async with session.get(next['url']) as page:
            result = await page.json()
            if page.ok:
                return result, page.links
            else:
                raise Exception(result)
    else:
        return None, None

def export_csv(filename, rows, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

def get_limit(r):
    limit = int(r.headers['X-Rate-Limit-Limit'])
    remaining = int(r.headers['X-Rate-Limit-Remaining'])
    reset = datetime.utcfromtimestamp(int(r.headers['X-Rate-Limit-Reset']))
    return limit, remaining, reset

async def snooze(r):
    limit, remaining, reset = get_limit(r)
    print(f'{limit = }, {remaining = }, {reset = }')
    if remaining < LIMIT_REMAINING:
        now = datetime.utcnow()
        delay = (reset - now).total_seconds()
        if delay > 0:
            print('sleeping...', delay)
            await asyncio.sleep(delay)

start = datetime.now()
asyncio.run(main())

end = datetime.now()
print(end - start)
