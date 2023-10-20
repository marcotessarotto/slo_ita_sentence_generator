from django.core.management.base import BaseCommand

from core.models import parse_json_and_create_instances, get_number_of_examples
from libopenai.tools import generate_example_text_slo_ita


class Command(BaseCommand):
    help = "Receives a list of words as arguments. Creates a WordListWithSampleTextAndTranslation instance."

    def add_arguments(self, parser):
        # Add a positional argument for the words. nargs='+' allows for multiple arguments.
        parser.add_argument('words', nargs='+', type=str, help='List of words to process')

        # add an optional integer argument
        parser.add_argument(
            '--max_num_examples_per_word_list',
            action='store',
            dest='max_num_examples_per_word_list',
            default=1,
            type=int,
            help='Maximum number of examples per word list'
        )

        # add an optional boolean argument
        parser.add_argument(
            '--remote',
            action='store_true',
            dest='remote',
            default=False,
            help='Whether to use the remote API or the local API'
        )

    def call_remote_api(self, words, max_num_examples_per_word_list):

        pass

    def handle(self, *args, **kwargs):
        words = kwargs['words']

        max_num_examples_per_word_list = kwargs['max_num_examples_per_word_list']

        remote = kwargs['remote']

        # Do something with the words. For this example, we'll just print them.
        self.stdout.write(self.style.SUCCESS('Received the following words:'))
        for word in words:
            self.stdout.write(word)

        if remote:
            self.call_remote_api(words, max_num_examples_per_word_list)

        if (num := get_number_of_examples(words, language='slovenian')) > max_num_examples_per_word_list:
            self.stdout.write(self.style.ERROR(f'There are already {num} examples for the provided words'))
            return

        data_json, data_str, response = generate_example_text_slo_ita(list(words))

        self.stdout.write(self.style.SUCCESS('Received the following data_json:'))
        self.stdout.write(data_str)

        instance = parse_json_and_create_instances(data_json, language='slovenian', check_presence=True)

        self.stdout.write(self.style.SUCCESS('Created the following instance:'))
        self.stdout.write(str(instance.id))


