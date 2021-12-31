import r

base_url = '...'
token = '...'

group_id = '...'

r.set_headers({
    'Authorization': f'SSWS {token}',
    'Accept': 'application/json'
})

res = r.get(f'{base_url}/api/v1/users/me')
me = res.json
user_id = me['id']
print(me['profile']['login'], me['profile']['title'], res.headers['x-rate-limit-remaining'])

url = f'{base_url}/api/v1/users?filter=profile.lastName+eq+%22Doe%22&limit=2'
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
