import okta_api

filename = 'DeleteGroups.csv'

groups = okta_api.get_groups(q='z group', limit=3).json()
okta_api.export_csv(filename, groups, ['id'])


# def export_groups():
#     groups = okta_api.get_groups(q='z group', limit=3).json()
#     if len(groups) == 0:
#         print('0 groups found.')
#         return
#     flat_groups = [
#         {
#             'id': group['id'], 
#             'name': group['profile']['name'],
#             'description': group['profile']['description']
#         } 
#         for group in groups
#     ]
#     okta_api.export_csv(filename, flat_groups, flat_groups[0].keys())

# export_groups()


# def search_groups():
#     for group in okta_api.get_groups().json():
#         if group['profile']['description'] == 'abc':
#             print(group['id'], group['profile']['name'])

# search_groups()


# group = {'profile': {'name': 'aa python group'}} # ...
# okta_api.new_group(group)
