#!/usr/bin/python3

"""Export Okta apps and groups to json."""

import requests
import json
from datetime import datetime
import time

# Set these:
org_url = '...'
token = '...'
LIMIT_REMAINING = 10

def fetch(url, name):
    print('fetching ' + name)
    with open(name + '.json', 'w') as f:
        for o in get_objects(url):
            print(to_json(o), file=f)

def fetch_sub(url, name, sub):
    print('fetching ' + name + ' and ' + sub)
    with open(name + '.json', 'w') as f, open(name[:-1] + '_' + sub + '.json', 'w') as fs:
        for o in get_objects(url):
            urls = o['_links'][sub]['href']
            print(to_json(o), file=f)
            for os in get_objects(urls):
                os[sub[:-1] + '_id'] = os.pop('id')
                os[name[:-1] + '_id'] = o['id']
                print(to_json(os), file=fs)

def get_objects(url):
    while url:
        res = session.get(url)
        for o in res.json():
            yield o
        snooze(res)
        url = res.links.get('next', {}).get('url')

def snooze(response):
    remaining = int(response.headers['X-Rate-Limit-Remaining'])
    if remaining <= LIMIT_REMAINING:
        limit = int(response.headers['X-Rate-Limit-Limit'])
        reset = datetime.utcfromtimestamp(int(response.headers['X-Rate-Limit-Reset']))
        print('sleeping...', remaining, limit, reset)
        while reset > datetime.utcnow():
            time.sleep(1)

def to_json(o):
    del o['_links']
    return json.dumps(o, separators=(',', ':'))

# When making multiple calls, session is faster than requests.
session = requests.Session()
session.headers['authorization'] = 'SSWS ' + token

fetch(f'{org_url}/api/v1/groups', 'groups')
fetch_sub(f'{org_url}/api/v1/apps?limit=200', 'apps', 'groups')


"""
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
select apps.label app_label,
    groups.name group_name,
    groups.description group_desc
from apps inner join app_groups on apps.id = app_groups.app_id
inner join groups on groups.id = app_groups.group_id
where apps.label like 'logfood%';

-- create a view
create view v_app_groups as select ...

-- json
$ sqlite3 -header okta.db
.import groups.json groups_j
select json->>'id' from groups_j;

-- join json->>'id' with a relational column
select apps.json->>'label' app_label,
    apps.json->>'status' app_status,
    groups.json->>'profile.name' group_name
from apps_j apps, groups_j groups, app_groups 
where apps.json->>'id' = app_groups.app_id 
and app_groups.group_id = groups.json->>'id';

-- json views
create view v_apps_j as 
select json->>'id' id,
    json->>'label' label,
    json->>'status' status
from apps_j;

create view v_groups_j as
select json->>'id' id,
    json->>'profile.name' name
from groups_j;

create view v_all as
select apps.label,
    apps.status,
    groups.name
from v_apps_j apps, v_groups_j groups, app_groups 
where apps.id = app_groups.app_id 
and app_groups.group_id = groups.id;
"""
