from django.core.management.base import BaseCommand

from core.models import parse_json_and_create_instances
from libopenai.tools import generate_example_text_slo_ita


class Command(BaseCommand):
    help = "Receives a list of words as arguments."

    def add_arguments(self, parser):
        # Add a positional argument for the words. nargs='+' allows for multiple arguments.
        parser.add_argument('words', nargs='+', type=str, help='List of words to process')

    def handle(self, *args, **kwargs):
        words = kwargs['words']

        # Do something with the words. For this example, we'll just print them.
        self.stdout.write(self.style.SUCCESS('Received the following words:'))
        for word in words:
            self.stdout.write(word)

        data_json, data_str, response = generate_example_text_slo_ita(list(words))

        self.stdout.write(self.style.SUCCESS('Received the following data_json:'))
        self.stdout.write(data_str)

        instance = parse_json_and_create_instances(data_json, language='slovenian', check_presence=True)

        self.stdout.write(self.style.SUCCESS('Created the following instance:'))
        self.stdout.write(instance)


