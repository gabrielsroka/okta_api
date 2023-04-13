"""
Export Okta groups, apps, and app groups to csv.
https://github.com/gabrielsroka/okta_api/blob/master/okta_to_csv.py

1. run the Python to export Okta to csv files
2. run the SQLite commands using the sqlite3 CLI [0] to create the db, import the csv files, run the query, and create output csv

$ sqlite3 -csv -header okta.db
-- import csv files (only need to do this one time)
.import apps.csv apps
.import groups.csv groups
.import app_groups.csv app_groups

-- send output of next query to csv
.once results.csv

-- or, to excel
.excel

-- query
select apps.label app_label, groups.name group_name, groups.description group_desc
from apps inner join app_groups on apps.id = app_groups.app_id
inner join groups on groups.id = app_groups.group_id
where apps.label like 'logfood%';


[0] DL CLI: https://www.sqlite.org/download.html
CLI docs: https://www.sqlite.org/cli.html
Python sqlite: https://docs.python.org/3/library/sqlite3.html
"""

import requests
import csv
from datetime import datetime
import time

# Set these:
org_url = 'https://ORG.okta.com'
token = '...'
LIMIT_REMAINING = 10

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

def get_objects(path):
    url = org_url + path
    while url:
        res = session.get(url)
        for o in res.json():
            yield o
        snooze(res)
        url = res.links.get('next', {}).get('url')

def snooze(response):
    remaining = int(response.headers['X-Rate-Limit-Remaining'])
    limit = int(response.headers['X-Rate-Limit-Limit'])
    if remaining <= LIMIT_REMAINING:
        reset = datetime.utcfromtimestamp(int(response.headers['X-Rate-Limit-Reset']))
        print('sleeping...', remaining, limit, reset)
        while reset > datetime.utcnow():
            time.sleep(1)

def export_csv(filename, rows, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

print('fetching groups')
groups = []
for group in get_objects('/api/v1/groups'):
    groups.append({
        'id':  group['id'],
        'name': group['profile']['name'],
        'description': group['profile']['description']
    })
export_csv('groups.csv', groups, groups[0].keys())

print('fetching apps and app groups')
apps = []
app_groups = []
for app in get_objects('/api/v1/apps'): # ?q=logfood&limit=200
    for app_group in get_objects(f"/api/v1/apps/{app['id']}/groups"):
        app_groups.append({
            'app_id': app['id'],
            'group_id': app_group['id']
        })
    apps.append({
        'id': app['id'],
        'label': app['label']
    })
export_csv('apps.csv', apps, apps[0].keys())
export_csv('app_groups.csv', app_groups, app_groups[0].keys())
