import hashlib

from django.db import models
import json


class Word(models.Model):
    LANGUAGES = (
        ('slovensko', 'slovensko'),
        ('italiano', 'italiano'),
    )

    text = models.CharField(max_length=255)
    language = models.CharField(max_length=10, choices=LANGUAGES)

    class Meta:
        unique_together = ('text', 'language')  # Ensures that the combination of text and language is unique

    def __str__(self):
        return f"{self.text} ({self.get_language_display()})"


class WordListWithSampleTextAndTranslation(models.Model):
    words = models.ManyToManyField(Word, related_name='text_translations')

    sha256_hash_of_words = models.CharField(max_length=64, unique=False)

    number_of_sentences = models.IntegerField(default=-1)
    slovenian_text = models.TextField()
    italian_text = models.TextField()

    sha256_hash_of_slovenian_text = models.CharField(max_length=64, unique=False)
    sha256_hash_of_italian_text = models.CharField(max_length=64, unique=False)

    def __str__(self):
        return f"{self.get_words_list()} ({self.number_of_sentences} sentences)"

    # calculate hash of words
    def get_hash_of_words(self):
        # sort words by text and language
        sorted_word_list = self.words.all().order_by('text', 'language')

        words_list = [f"{word.text}|{word.language}" for word in sorted_word_list]
        return hashlib.sha256(json.dumps(words_list).encode()).hexdigest()

    def save(self, *args, **kwargs):

        self.sha256_hash_of_words = self.get_hash_of_words()

        self.sha256_hash_of_slovenian_text = hashlib.sha256(self.slovenian_text.encode()).hexdigest()
        self.sha256_hash_of_italian_text = hashlib.sha256(self.italian_text.encode()).hexdigest()
        super().save(*args, **kwargs)


def parse_json_and_create_instances(json_data, language, check_presence=True):
    # data = json.loads(json_data)

    if not language:
        raise ValueError("Language must be specified")

    # check existence of all words in database and create them if they don't exist
    words_list = sorted(json_data["words_list"])

    words_instances = []
    for word in words_list:
        rs = Word.objects.filter(text=word, language=language)
        if not rs.exists():
            # create new Word instance
            w = Word.objects.create(text=word, language=language)
            w.save()
        else:
            w = rs.first()

        words_instances.append(w)

    if check_presence:
        # check if the same list of words is already present in the database
        words_list = [f"{word.text}|{word.language}" for word in words_instances]
        sha256_hash_of_words = hashlib.sha256(json.dumps(words_list).encode()).hexdigest()

        rs = WordListWithSampleTextAndTranslation.objects.filter(sha256_hash_of_words=sha256_hash_of_words)
        if rs.exists():
            return rs.first()

    # Create or retrieve Word instances for each word in the words_list
    # word_instances = []
    # for word_text in json_data["words_list"]:
    #     # Assuming all words in this example are in Slovenian. Adjust if needed.
    #     word, _ = Word.objects.get_or_create(text=word_text, language='slovensko')
    #     word_instances.append(word)

    # Create WordListWithSampleTextAndTranslation instance linked to the Word instances
    text_translation = WordListWithSampleTextAndTranslation.objects.create(
        # number_of_sentences=json_data["number_of_sentences"],
        slovenian_text=json_data["slovenian_text"],
        italian_text=json_data["italian_text"]
    )
    text_translation.words.set(words_instances)
