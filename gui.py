"""Call Okta APIs using Session (cookies) -- just like a browser. SSWS API Token is not needed.

This will work with users who have Push MFA. This won't work if Apps > Apps > "Okta Admin Console" > Sign On Policy > MFA is enabled.
"""

import requests
import json
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

# Set these defaults:
okta_url = 'https://ORG.okta.com'
username = '...'

# A session uses cookies and reuses the HTTP connection.
session = requests.Session()

def main():
    global user_info_text
    root, url_entry, username_entry, password_entry, sign_in_button, user_info_text = gui(f"""
        Okta URL
        _{okta_url}_
        Username
        _{username}_
        Password
        _*_
        [Sign In]
        User Info
        |text|
    """)
    
    command = lambda _=None: sign_in(url_entry.get(), username_entry.get(), password_entry.get())
    sign_in_button['command'] = command
    password_entry.bind("<Return>", command)
    password_entry.focus()
    root.mainloop()

def gui(s):
    root = tk.Tk()
    root.title("Okta")

    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, sticky='w', padx=10, pady=10)

    ws = [root]
    for row, w in enumerate(w.strip() for w in s.split('\n') if w.strip()):
        text = w[1:-1]
        if w.startswith('_'):
            show, text = (text, '') if text == '*' else ('', text)
            w = ttk.Entry(main_frame, width=40, show=show)
            w.insert(0, text)
        elif w.startswith('['):
            w = ttk.Button(main_frame, text=text)
        elif w.startswith('|'):
            w = ScrolledText(main_frame, wrap=tk.WORD, width=100, height=30)
        else:
            w = ttk.Label(main_frame, text=w + ':')
        w.grid(row=row, sticky='w')
        if not isinstance(w, ttk.Label): ws.append(w)
    return ws

def sign_in(okta_url, username, password):
    response = session.post(okta_url + '/api/v1/authn', json={'username': username, 'password': password})
    authn = response.json()
    if not response.ok:
        messagebox.showerror("Error", authn['errorSummary'])
        return

    if authn['status'] == 'MFA_REQUIRED':
        token = send_push(authn['_embedded']['factors'], authn['stateToken'])
    else:
        token = authn['sessionToken']

    session.get(okta_url + '/login/sessionCookie?token=' + token)

    user = session.get(okta_url + '/api/v1/users/me').json()
    del user['_links']
    user_info_text.insert("1.0", json.dumps(user, indent=4))

def send_push(factors, state_token):
    push_factors = [f for f in factors if f['factorType'] == 'push']
    if not push_factors:
        messagebox.showerror("Error", "Push factor not found")
        exit()

    push_url = push_factors[0]['_links']['verify']['href']
    while True:
        authn = session.post(push_url, json={'stateToken': state_token}).json()
        if authn['status'] == 'SUCCESS':
            return authn['sessionToken']
        result = authn['factorResult']
        if result == 'WAITING':
            time.sleep(4)  # 4 seconds
        elif result in ['REJECTED', 'TIMEOUT']:
            messagebox.showerror("Error", "Push rejected")
            exit()

main()
