import okta_api
import time

def test_push():
    user_id = okta_api.get_user('me').json()['id']
    factors = okta_api.get_user_factors(user_id).json()
    push_factors = [f for f in factors if f['factorType'] == 'push']
    if not push_factors:
        print('Push factor not found')
        return
    resp = okta_api.issue_user_factor_challenge(user_id, push_factors[0]['id']).json()
    print('Sent push')
    while True:
        result = resp['factorResult']
        print(result)
        if result == 'WAITING':
            time.sleep(4) # 4 seconds
            resp = okta_api.session.get(resp['_links']['poll']['href']).json()
        elif result in ['SUCCESS', 'REJECTED', 'TIMEOUT']:
            return

def export_users():
    # Export to CSV.
    print('Getting users.')
    users = []
    for page in okta_api.get_user_pages(filter='profile.lastName eq "Doe"'): # limit=2
        for user in page.json():
            users.append({
                'id': user['id'], 
                'login': user['profile']['login'],
                'email': user['profile']['email']
            })
        print('Total users found:', len(users))

    if users:
        okta_api.export_csv('users.csv', users, users[0].keys())

def get_schemas():
    for page in okta_api.get_app_pages():
        for app in page.json():
            r = okta_api.get_app_schema(app['id'])
            if r.ok: # Skip bookmark apps, etc.
                schema = r.json()
                print(app['id'], app['label'], schema['definitions']['custom'])

def get_app_groups(app):
    LIMIT_REMAINING = 10
    for page in okta_api.get_app_group_pages(app['id'], expand='group'):
        groups = page.json()
        for group in groups:
            app_groups.append({'app': app['label'], 'group': group['_embedded']['group']['profile']['name']})
        if not groups:
            app_groups.append({'app': app['label'], 'group': '(no groups)'})
        okta_api.snooze(page, LIMIT_REMAINING)

app_groups = []
def get_apps_and_groups():
    for page in okta_api.get_app_pages():
        for app in page.json():
            print('fetching', app['label'])
            get_app_groups(app)
    okta_api.export_csv('app_groups.csv', app_groups, app_groups[0].keys())



# def main():
#     """Export to CSV."""
#     print('Getting users.')
#     keys = ['id', 'profile.login','profile.email']
#     users = []
#     for page in okta_api.get_user_pages(filter='profile.lastName eq "Doe"', limit=2):
#         users.extend(pluck(page.json(), keys)) # [{key: reduce(getitem, key.split('.'), user) for key in keys} for user in users]
#         print('Total users found:', len(users))

#     if users:
#         okta_api.export_csv('users.csv', users, keys)

# def pluck(items, keys):
#     new_list = []
#     for item in items:
#         d = {}
#         for key in keys:
#             v = item
#             for k in key.split('.'):
#                 v = v[k]
#             d[key] = v
#         new_list.append(d)
#     return new_list

# main()


# old style

# page = okta_api.get_users(limit=2, filter='profile.lastName eq "Doe"')
# while page:
#     for user in page.json():
#         print(user['id'], user['profile']['login'])
#     page = okta_api.get_next_page(page.links)
