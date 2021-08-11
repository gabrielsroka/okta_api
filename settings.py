import os

from dotenv import load_dotenv
load_dotenv()


OKTA_ORG_URL = os.getenv('OKTA_ORG_URL')
OKTA_ADMIN_URL = OKTA_ORG_URL.replace('.', '-admin.', 1)
OKTA_USERNAME = os.getenv('OKTA_USERNAME')
OKTA_PASSWORD = os.getenv('OKTA_PASSWORD')
OKTA_API_TOKEN = os.getenv('OKTA_API_TOKEN')

DIRECTORY_TYPE = os.getenv('DIRECTORY_TYPE')
DIRECTORY_ID = os.getenv('DIRECTORY_ID')