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


def call_remote_api(words, max_num_examples_per_word_list, debug_msg=True):
    """
    Call the remote API; web service url is constructed using BASE_URL defined in .env file;
     credentials for the web service are also defined in .env file (WEB_SERVICE_USERNAME and WEB_SERVICE_PASSWORD)
    
    :param words: 
    :param max_num_examples_per_word_list: 
    :return: response.status_code, response.json()
    """
    env = get_env()

    # Set the base URL of your Django server
    BASE_URL = env('BASE_URL')  # Adjust this to the actual URL and port where your Django server runs

    # Define your login credentials and test data
    login_data = {
        'username': env('WEB_SERVICE_USERNAME'),
        'password': env('WEB_SERVICE_PASSWORD')
    }

    request_data = {
        'word_list': words
    }

    # Authenticate first
    login_url = f"{BASE_URL}/admin/login/"  # Assuming default Django admin login URL. Adjust if different.
    with requests.Session() as session:
        # Get the CSRF token first
        session.get(login_url)
        csrf_token = session.cookies['csrftoken']

        # Now login using the CSRF token
        headers = {
            'X-CSRFToken': csrf_token,
            'Referer': f"{BASE_URL}/core/"
        }
        login_response = session.post(login_url, data=login_data, headers=headers)

        if login_response.status_code == 200:
            # Use the session of the logged-in user to make the request
            # Adjust the endpoint URL if different
            response = session.post(
                f"{BASE_URL}/core/produce_slo_ita_example/",
                data=request_data,
                headers=headers  # Send the CSRF token again
            )

            if response.status_code == 200:
                # print("Service response:", response.json())
                # print()
                # s = json.dumps(response.json(), indent=4, sort_keys=True)
                # print(s)

                return response.status_code, response.json(), "Success"
            else:
                if debug_msg:
                    print("Error:", response.status_code, response.text)

                return response.status_code, None, response.text
        else:
            if debug_msg:
                print("Failed to login:", login_response.status_code, login_response.text)

            return login_response.status_code, None, "Failed to login"


if __name__ == '__main__':
    words = ['tek', 'šola', 'glasba']
    # words = [ "šola", "tek" ]
    # words = ['kruh', 'mleko', 'sir']
    
    max_num_examples_per_word_list = 1

    status_code, json_data, msg = call_remote_api(words, max_num_examples_per_word_list)

    if status_code == 200:
        print("Service response:", json_data)
        print()
        s = json.dumps(json_data, indent=4, sort_keys=True)
        print(s)
    else:
        print("Error:", status_code, msg)


