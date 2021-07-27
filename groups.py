import okta_api

def update_groups():
    groups = okta_api.get_groups(q='a api group').json()
    for group in groups:
        print(group['profile']['name'], group['profile']['description'])
        group['profile']['description'] = 'new desc'
        okta_api.update_group(group['id'], group)

def new_okta_group():
    group = {'profile': {'name': 'aa python group'}} # ...
    okta_api.new_group(group)

def export_group_ids(filename):
    groups = okta_api.get_groups(q='z group', limit=3).json()
    okta_api.export_csv(filename, groups, ['id'])

def export_groups():
    groups = okta_api.get_groups(q='z group', limit=3).json()
    if not groups:
        print('0 groups found.')
        return
    flat_groups = [
        {
            'id': group['id'], 
            'name': group['profile']['name'],
            'description': group['profile']['description']
        } 
        for group in groups
    ]
    okta_api.export_csv(filename, flat_groups, flat_groups[0].keys())

def delete_groups(filename):
    for group in okta_api.import_csv(filename):
        okta_api.delete_group(group['id'])

def search_groups():
    """Local search"""
    for group in okta_api.get_groups().json():
        if group['profile']['description'] == 'test':
            print(group['id'], group['profile']['name'])

def search_okta_groups():
    userid = okta_api.get_user('me').json()['id']
    for group in okta_api.get_groups(q='grp-atlassian').json():
        print(group['id'], group['profile']['name'])
        okta_api.add_group_member(group['id'], userid)

