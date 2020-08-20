import okta_api

def export_users():
    # Export to CSV.
    print('Getting users.')
    users = []
    for page in okta_api.get_user_pages(filter='profile.lastName eq "Doe"'): #, limit=2):
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
            if r.ok: # Skip bookmark apps.
                schema = r.json()
                print(app['id'], app['label'], schema['definitions']['custom'])


# def main():
#     """Export to CSV."""
#     print('Getting users.')
#     keys = ['id', 'profile.login','profile.email']
#     users = []
#     for page in okta_api.get_user_pages(filter='profile.lastName eq "Doe"', limit=2):
#         users.extend(pluck(page.json(), keys))
#         print('Total users found:', len(users))

#     if users:
#         okta_api.export_csv('users.csv', users, keys)

# def pluck(list, keys):
#     new_list = []
#     for item in list:
#         new_item = {}
#         for key in keys:
#             d = item
#             for k in key.split('.'):
#                 d = d[k]
#             new_item[key] = d
#         new_list.append(new_item)
#     return new_list

# main()


# old style

# page = okta_api.get_users(limit=2, filter='profile.lastName eq "Doe"')
# while page:
#     for user in page.json():
#         print(user['id'], user['profile']['login'])
#     page = okta_api.get_next_page(page.links)
