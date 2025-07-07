import okta_requests

# Set these:
filter = 'profile.lastName eq "Doe"'
limit = 200
group_id = '00g...'

session = okta_requests.Session()

# Paginate users.
for user in session.get_objects('/api/v1/users', filter=filter, limit=limit):
    print(user['profile']['login'])

# Get me.
res = session.get('/api/v1/users/me') # NOTE: don't use 'me' with OAuth.
user = res.json()
user_id = user['id']
print(user['profile']['login'], user['profile']['title'])

# Update my title.
# res = session.post('/api/v1/users/me', {'profile': {'title': 'admin'}})
# user = res.json()
# print(user['profile']['title'])

# Add me to a group.
# res = session.put(f'/api/v1/groups/{group_id}/users/{user_id}')
# print(res.ok)

# Remove me from the group.
# res = session.delete(f'/api/v1/groups/{group_id}/users/{user_id}')
# print(res.ok)
