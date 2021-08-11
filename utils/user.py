from requests import Session


def get_user(session: Session, okta_url: str, userid: str):
    return session.get(f'{okta_url}/api/v1/users/{userid}').json()


def get_user_factors(session: Session, okta_url: str, userid):
    return session.get(f'{okta_url}/api/v1/users/{userid}/factors').json()