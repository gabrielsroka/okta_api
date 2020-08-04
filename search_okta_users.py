import okta_api

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

if len(users) > 0:
    okta_api.export_csv('users.csv', users, users[0].keys())


# def main():
#     """Export to CSV."""
#     print('Getting users.')
#     keys = ['id', 'profile.login','profile.email']
#     users = []
#     for page in okta_api.get_user_pages(filter='profile.lastName eq "Doe"', limit=2):
#         users.extend(pluck(page.json(), keys))
#         print('Total users found:', len(users))

#     if len(users) > 0:
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
