import urllib.request
import urllib.parse
import json as json_
import gzip
import re

headers = {'Accept-Encoding': 'gzip'}

def url(url, **kwargs):
    return url + '?' + urllib.parse.urlencode(kwargs)

def r(method, url, json=None):
    """Returns HTTPResponse object (including res.reason, .status, .headers) and also .json, .next_url."""
    _headers = headers.copy()
    if json:
        data = json_.dumps(json, separators=(',', ':')).encode()
        _headers['Content-Type'] = 'application/json'
    else:
        data = None
    req = urllib.request.Request(url, data, _headers, method=method)
    with urllib.request.urlopen(req) as res:
        if res.reason != 'No Content': # (204), TODO: add more reasons/statuses?
            fp = gzip.open(res) if res.headers['Content-Encoding'] == 'gzip' else res
            res.json = json_.load(fp)
    return res

def get(url):
    res = r('GET', url)
    links = [link for link in res.headers.get_all('link', []) if 'rel="next"' in link]
    res.next_url = re.search('<(.*)>', links[0]).group(1) if links else None
    return res 

def post(url, json=None):
    return r('POST', url, json)

def put(url, json=None):
    return r('PUT', url, json)

def patch(url, json=None):
    return r('PATCH', url, json)

def delete(url):
    return r('DELETE', url)
