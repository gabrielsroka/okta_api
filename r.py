import urllib.request
import json as json_
import gzip
import re

_headers = {}

def set_headers(headers):
    global _headers
    _headers = headers
    _headers['Accept-Encoding'] = 'gzip'

def get(url, json=None, headers={}, method='GET'):
    headers = headers or _headers.copy()
    if json:
        data = json_.dumps(json, separators=(',', ':')).encode()
        headers['Content-Type'] = 'application/json'
    else:
        data = None
    req = urllib.request.Request(url, data, headers, method=method)
    with urllib.request.urlopen(req) as res:
        if res.reason != 'No Content': # (204), TODO: add more reasons/statuses?
            fp = gzip.open(res) if res.headers['Content-Encoding'] == 'gzip' else res
            res.json = json_.load(fp)
    links = [link for link in res.headers.get_all('link') or [] if 'rel="next"' in link]
    res.next_url = re.search('<(.*)>', links[0]).group(1) if links else None
    return res
    # print(res.reason, res.status, res.headers)

def post(url, json=None, headers={}):
    return get(url, json, headers, 'POST')

def put(url, json=None, headers={}):
    return get(url, json, headers, 'PUT')

def delete(url, json=None, headers={}):
    return get(url, json, headers, 'DELETE')
