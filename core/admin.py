from django.contrib import admin

from django.contrib import admin
from .models import Word, TextTranslation

class WordAdmin(admin.ModelAdmin):
    list_display = ['text', 'language']  # Display text and language in the list view
    search_fields = ['text']  # Allow searching by word text


class TextTranslationAdmin(admin.ModelAdmin):
    list_display = ['slovenian_text', 'italian_text', 'number_of_sentences']
    search_fields = ['slovenian_text', 'italian_text']
    filter_horizontal = ('words',)  # Use a horizontal filter for many-to-many relationships


admin.site.register(Word, WordAdmin)
admin.site.register(TextTranslation, TextTranslationAdmin)

