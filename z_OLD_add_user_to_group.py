from okta import UsersClient, UserGroupsClient
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv('OKTA_ORG_URL')
token = os.getenv('OKTA_API_TOKEN')

usersClient = UsersClient(url, token)
groupsClient = UserGroupsClient(url, token)

user = usersClient.get_user('aaron')
groupId = '00g9raeyraaWXn1zF0h7'

groupsClient.add_user_to_group_by_id(groupId, user.id)
