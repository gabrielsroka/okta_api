from enum import Enum
from requests import Session


class Target(Enum):
    GROUPS_AND_USERS: str = "GROUPS_AND_USERS"
    EVERYONE: str = "EVERYONE"


def send_notification(session: Session, okta_admin_url: str, admin_xsrf_token: str, message: str, target: Target, users: list[str], groups: list[str]):
    body = {
        'message': message,
        'target': target.value,
        'users': users,
        'groups': groups
    }
    headers = {
        'X-Okta-XsrfToken': admin_xsrf_token
    }
    
    notification = session.post(f'{okta_admin_url}/api/internal/admin/notification', json=body, headers=headers).json()
    
    return notification
