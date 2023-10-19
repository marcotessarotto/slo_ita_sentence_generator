from django.contrib import admin
from .models import Word , WordListWithSampleTextAndTranslation


class WordAdmin(admin.ModelAdmin):
    list_display = ['text', 'language']  # Display text and language in the list view
    search_fields = ['text']  # Allow searching by word text


class WordListWithSampleTextAndTranslationAdmin(admin.ModelAdmin):
    list_display = ['id', 'slovenian_text', 'italian_text', 'sha256_hash_of_words']
    search_fields = ['slovenian_text', 'italian_text']
    filter_horizontal = ('words',)  # Use a horizontal filter for many-to-many relationships


admin.site.register(Word, WordAdmin)
admin.site.register(WordListWithSampleTextAndTranslation, WordListWithSampleTextAndTranslationAdmin)
