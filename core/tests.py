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

# Create your tests here.

# from django.test import TestCase
# from django.urls import reverse

# from .models import Question

# class QuestionModelTests(TestCase):

#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)

#     def test_was_published_recently_with_old_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)

#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)

# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)

# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('core:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('core:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],