import settings

from requests import Session
from utils.authentication import sign_in, get_admin_xsrf_token
from utils.directory import start_directory_import, monitor_job_status


def trigger_directory_import():
    session = Session()
    sign_in(session)
    xsrf_token = get_admin_xsrf_token(session)

    directory_type = settings.DIRECTORY_TYPE
    directory_id = settings.DIRECTORY_ID

    job_id = start_directory_import(session, xsrf_token, settings.OKTA_ADMIN_URL, directory_type, directory_id)
    monitor_job_status(session, settings.OKTA_ADMIN_URL, job_id, xsrf_token)


if __name__ == "__main__":
    trigger_directory_import()
