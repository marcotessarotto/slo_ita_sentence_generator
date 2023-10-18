
import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Set up django-environ
env = environ.Env(
    # Default values for variables if not set
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

OPENAI_API_KEY = env('OPENAI_API_KEY')


# work in progress, this is an example of how to use the openai api

import os
import openai

openai.api_key = OPENAI_API_KEY


system_content = "slovenian language: generate a random sentence including the words passed as role 'user."\
                  " the output must be valid JSON and must include the original words, the generated example in slovenian,"\
                  "and the italian translation of the generated example. "


response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": system_content #"You will be provided with a product description and seed words, and your task is to generate product names."
    },
    {
      "role": "user",
      "content": "('tekmovanja')"
    }
  ],
  temperature=0.8,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)
