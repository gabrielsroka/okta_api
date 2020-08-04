from okta_api import delete_group, import_csv

filename = 'DeleteGroups.csv'

for group in import_csv(filename):
    delete_group(group['id'])
