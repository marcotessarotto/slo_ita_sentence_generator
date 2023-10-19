from django.contrib.auth.models import User
from django.test import TestCase
from core.models import Word, WordListWithSampleTextAndTranslation
from core.models import parse_json_and_create_instances  # Assuming the function is in a utils.py file in 'myapp'


class ParseJsonAndCreateInstancesTestCase(TestCase):

    def test_parse_json_and_create_instance_no_language(self):
        json_data = {
          "words_list": ["šola", "tek"],
          "slovenian_text": "Danes sem šel v šolo in se udeležil teka.",
          "italian_text": "Oggi sono andato a scuola e ho partecipato alla corsa."
        }

        with self.assertRaises(ValueError):
            parse_json_and_create_instances(json_data, language=None)

    def test_parse_json_and_create_instance_success(self):
        json_data = {
          "words_list": ["šola", "tek"],
          "slovenian_text": "Danes sem šel v šolo in se udeležil teka.",
          "italian_text": "Oggi sono andato a scuola e ho partecipato alla corsa."
        }
        instance = parse_json_and_create_instances(json_data, language="slovensko")
        self.assertEqual(instance.slovenian_text, "Danes sem šel v šolo in se udeležil teka.")
        self.assertEqual(instance.italian_text, "Oggi sono andato a scuola e ho partecipato alla corsa.")
        self.assertTrue(Word.objects.filter(text="šola", language="slovensko").exists())
        self.assertTrue(Word.objects.filter(text="tek", language="slovensko").exists())

    def test_parse_json_and_create_instance_duplicate_word(self):
        json_data = {
          "words_list": ["šola", "tek"],
          "slovenian_text": "Danes sem šel v šolo in se udeležil teka.",
          "italian_text": "Oggi sono andato a scuola e ho partecipato alla corsa."
        }

        instance1 = parse_json_and_create_instances(json_data, language="slovensko")

        instance2 = parse_json_and_create_instances(json_data, language="slovensko")

        self.assertEqual(instance1.id, instance2.id)

    # def test_parse_json_and_create_instance_duplicate_word(self):
    #     Word.objects.create(text="example", language="slovensko")
    #     json_data = {
    #       "words_list": ["šola", "tek"],
    #       "slovenian_text": "Danes sem šel v šolo in se udeležil teka.",
    #       "italian_text": "Oggi sono andato a scuola e ho partecipato alla corsa."
    #     }
    #     instance = parse_json_and_create_instances(json_data, language="slovensko")
    #     self.assertEqual(instance.slovenian_text, "This is a test.")
    #     self.assertEqual(instance.italian_text, "Questo è un test.")
    #     self.assertEqual(Word.objects.filter(text="example", language="slovensko").count(), 1)

    # Add more test cases as needed...


# class WebserviceTestCase(TestCase):
#
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(
#             username='your_username',
#             password='your_password',
#             email='testuser@example.com'
#         )
#
#     def test_auth(self):
#
#         import requests
#
#         # Set the base URL of your Django server
#         BASE_URL = 'http://localhost:8000'  # Change this if your server runs on a different URL/port
#
#         # Define test data
#         login_data = {
#             'username': 'your_username',
#             'password': 'your_password'
#         }
#
#         test_data = {
#             'word_list': ['parola1', 'parola2', 'parola3'],
#             'slo2ita': 'True',
#             'number_of_sentences': 5
#         }
#
#         # Authenticate first
#         with requests.Session() as session:
#             # Fetch the login page first to get the CSRF token
#             response = session.get(f"{BASE_URL}/admin/login/")
#
#             print(response.text)
#             print()
#
#             # Django stores the CSRF token in a cookie and in a hidden input field named 'csrfmiddlewaretoken'
#             # We can retrieve the token from the cookie or from the form
#             csrf_token = session.cookies['csrftoken']
#
#             # Include the CSRF token in login data
#             login_data['csrfmiddlewaretoken'] = csrf_token
#
#             login_response = session.post(f"{BASE_URL}/admin/login/", data=login_data)
#
#             if login_response.status_code == 200:
#                 # For the next request (after login), we can fetch the CSRF token again from the cookies
#                 # But this is optional because our session already has the cookie set
#                 csrf_token = session.cookies['csrftoken']
#
#                 headers = {
#                     'X-CSRFToken': csrf_token
#                 }
#
#                 # Use the session of the logged-in user to make the request
#                 response = session.post(f"{BASE_URL}/core/produce_examples/", data=test_data, headers=headers)
#
#                 if response.status_code == 200:
#                     print("Service response:", response.json())
#                 else:
#                     print("Error:", response.status_code, response.text)
#             else:
#                 print("Failed to login:", login_response.status_code, login_response.text)


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProduceExamplesTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_produce_examples_requires_login(self):
        # Test if the view is protected by @login_required
        response = self.client.post(reverse('produce_examples'))  # You might need to adjust the reverse name
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_produce_examples_valid_request(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        data = {
            'word_list': ['example1', 'example2'],
            'slo2ita': 'True',
            'number_of_sentences': 5
        }
        response = self.client.post(reverse('produce_examples'), data=data)

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertListEqual(json_data['word_list'], data['word_list'])
        self.assertEqual(json_data['slo2ita'], True)
        self.assertEqual(json_data['number_of_sentences'], data['number_of_sentences'])

    def test_produce_examples_invalid_request(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        data = {
            'word_list': [],
            'slo2ita': 'True',
            'number_of_sentences': 11
        }
        response = self.client.post(reverse('produce_examples'), data=data)

        self.assertEqual(response.status_code, 400)  # Bad request

    # Add more test methods as needed


