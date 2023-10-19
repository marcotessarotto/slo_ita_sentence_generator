import hashlib

from django.db import models
import json


class Word(models.Model):
    LANGUAGES = (
        ('slovensko', 'Slovensko'),
        ('italiano', 'Italiano'),
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

    number_of_sentences = models.IntegerField()
    slovenian_text = models.TextField()
    italian_text = models.TextField()

    sha256_hash_of_slovenian_text = models.CharField(max_length=64, unique=False)
    sha256_hash_of_italian_text = models.CharField(max_length=64, unique=False)

    def __str__(self):
        return ", ".join(word.text for word in self.words.all())

    def save(self, *args, **kwargs):

        # Calculate the sha256 hash of the words
        words_list = sorted([word.text for word in self.words.all()])
        self.sha256_hash_of_words = hashlib.sha256(json.dumps(words_list).encode()).hexdigest()

        self.sha256_hash_of_slovenian_text = hashlib.sha256(self.slovenian_text.encode()).hexdigest()
        self.sha256_hash_of_italian_text = hashlib.sha256(self.italian_text.encode()).hexdigest()
        super().save(*args, **kwargs)


def parse_json_and_create_instances(json_data):
    data = json.loads(json_data)

    # Create or retrieve Word instances for each word in the words_list
    word_instances = []
    for word_text in data["words_list"]:
        # Assuming all words in this example are in Slovenian. Adjust if needed.
        word, _ = Word.objects.get_or_create(text=word_text, language='slovensko')
        word_instances.append(word)

    # Create WordListWithSampleTextAndTranslation instance linked to the Word instances
    text_translation = WordListWithSampleTextAndTranslation.objects.create(
        number_of_sentences=data["number_of_sentences"],
        slovenian_text=data["slovenian_text"],
        italian_text=data["italian_text"]
    )
    text_translation.words.set(word_instances)
