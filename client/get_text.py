import json

import requests
import os
import environ
from pathlib import Path

def get_env():
    BASE_DIR = Path(__file__).resolve().parent.parent

    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    return env


env = get_env()

# Set the base URL of your Django server
BASE_URL = env('BASE_URL')  # Adjust this to the actual URL and port where your Django server runs

# Define your login credentials and test data
login_data = {
    'username': env('WEB_SERVICE_USERNAME'),
    'password': env('WEB_SERVICE_PASSWORD')
}

test_data = {
    'word_list': ['tek', "šola", "glasba"] # "šola", "tek"
}

# test_data = {
#
#     'word_list': ["kruh", "mleko", "sir"]
# }

# Authenticate first
login_url = f"{BASE_URL}/admin/login/"  # Assuming default Django admin login URL. Adjust if different.
with requests.Session() as session:
    # Get the CSRF token first
    session.get(login_url)
    csrf_token = session.cookies['csrftoken']

    # Now login using the CSRF token
    headers = {
        'X-CSRFToken': csrf_token,
        'Referer': env('WEB_SERVICE_REFERER')
    }
    login_response = session.post(login_url, data=login_data, headers=headers)

    if login_response.status_code == 200:
        # Use the session of the logged-in user to make the request
        # Adjust the endpoint URL if different
        response = session.post(
            f"{BASE_URL}/core/produce_slo_ita_example/",
            data=test_data,
            headers=headers  # Send the CSRF token again
        )

        if response.status_code == 200:
            print("Service response:", response.json())

            print()
            s = json.dumps(response.json(), indent=4, sort_keys=True)
            print(s)
        else:
            print("Error:", response.status_code, response.text)
    else:
        print("Failed to login:", login_response.status_code, login_response.text)
