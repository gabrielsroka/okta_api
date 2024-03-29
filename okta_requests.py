import requests
import os

# If you're making multiple API calls, using Session is much faster.
class Session(requests.Session):
    def __init__(self, org_url=os.getenv('OKTA_CLIENT_ORGURL'), token=os.getenv('OKTA_CLIENT_TOKEN')):
        super().__init__()
        self.org_url = org_url
        self.headers['authorization'] = 'SSWS ' + token

    def request(self, method, url, **kwargs):
        if not url.startswith('https:'):
            url = self.org_url + url
        return super().request(method, url, **kwargs)

    def post(self, url, json=None):
        return super().post(url, json=json)

    def put(self, url, json=None):
        return super().put(url, json=json)

    def patch(self, url, json=None):
        return super().patch(url, json=json)

    def get_objects(self, url, **params):
        while url:
            res = self.get(url, params=params)
            params = None
            for o in res.json():
                yield o
            url = res.links.get('next', {}).get('url')
