import sys
import time

from utils.common import parse_safe_json_response, print_progress_bar
from requests import Session
from tabulate import tabulate


def start_directory_import(session: Session, xsrf_token: str, okta_admin_url: str, directory_type: str, directory_id: str):
    url = f"{okta_admin_url}/admin/user/import/{directory_type}/{directory_id}/start"
    body = {
        "fullImport": "true",
        "_xsrfToken": xsrf_token,
    }
    headers = {
        "X-Okta-XsrfToken": xsrf_token,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(url, data=body, headers=headers)

    if not response.ok:
        print("Error starting directory import")
        sys.exit()

    json_resp = parse_safe_json_response(response)
    
    return json_resp["modelMap"]["jobId"]


def monitor_job_status(session: Session, okta_admin_url: str, job_id: str, xsrf_token: str):
    headers = {
        "X-Okta-XsrfToken": xsrf_token,
    }

    while True:
        url = f"{okta_admin_url}/joblist/status?jobs={job_id}"
        response = session.get(url, headers=headers)
        json_resp = parse_safe_json_response(response)
        
        job = json_resp["jobList"]["jobList"][0]
        
        if job["status"] == "COMPLETED":
            print_progress_bar(100, 100)
            break

        print_progress_bar(job["currentStep"], job["totalSteps"] or 100)
        time.sleep(2)

    url = f"{okta_admin_url}/job/status?jobid={job_id}"
    response = session.get(url, headers=headers)
    json_resp = parse_safe_json_response(response)
    job = json_resp["job"]

    table_headers = ["", "Scanned", "Imported", "Updated", "Unchanged", "Removed"]
    table = [
        ["Users", job["usersScanned"], job["usersAdded"], job["usersUpdated"], job["usersUnchanged"], job["usersRemoved"]],
        ["Groups", job["groupsScanned"], job["groupsAdded"], job["groupsUpdated"], job["groupsUnchanged"], job["groupsRemoved"]]
    ]
    print(tabulate(table, headers=table_headers, tablefmt="fancy_grid"))