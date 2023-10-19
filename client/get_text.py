import requests

# Set the base URL of your Django server
BASE_URL = 'http://localhost:8000'  # Adjust this to the actual URL and port where your Django server runs

# Define your login credentials and test data
login_data = {
    'username': 'marco',
    'password': 'marco'
}

test_data = {
    'word_list': ['tek' , "šola" ] # "šola", "tek"
}

# Authenticate first
login_url = f"{BASE_URL}/admin/login/"  # Assuming default Django admin login URL. Adjust if different.
with requests.Session() as session:
    # Get the CSRF token first
    session.get(login_url)
    csrf_token = session.cookies['csrftoken']

    # Now login using the CSRF token
    headers = {
        'X-CSRFToken': csrf_token
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
        else:
            print("Error:", response.status_code, response.text)
    else:
        print("Failed to login:", login_response.status_code, login_response.text)
