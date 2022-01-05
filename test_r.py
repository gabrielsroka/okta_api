import r
import json

# Set these:
with open('okta.yaml') as f: # in JSON format: {"okta":{"client":{"orgUrl":"...","token":"..."}}}
    config = json.load(f)['okta']['client']
    base_url = config['orgUrl'] # eg 'https://gsroka.oktapreview.com'

group_id = '...'

r.headers.update({
    'Authorization': 'SSWS ' + config['token'],
    'Accept': 'application/json'
})

res = r.get(f'{base_url}/api/v1/users/me')
me = res.json
user_id = me['id']
print(me['profile']['login'], me['profile']['title'], res.headers['x-rate-limit-remaining'])

# Pagination.
url = r.url(f'{base_url}/api/v1/users', filter='profile.lastName eq "Doe"', limit=2)
while url:
    res = r.get(url)
    print(len(res.json), url, res.headers['x-rate-limit-remaining'])
    for user in res.json:
        print(user['profile']['login'])
    url = res.next_url

res = r.post(f'{base_url}/api/v1/users/{user_id}', {'profile': {'title': 'technoking'}})
me = res.json
print(me['profile']['title'], res.headers['x-rate-limit-remaining'])

res = r.put(f'{base_url}/api/v1/groups/{group_id}/users/{user_id}')
print(res.headers['x-rate-limit-remaining'])

res = r.delete(f'{base_url}/api/v1/groups/{group_id}/users/{user_id}')
print(res.headers['x-rate-limit-remaining'])
