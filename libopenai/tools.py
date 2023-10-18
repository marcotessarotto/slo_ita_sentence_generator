import json
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


system_content = ("the input is a list of slovenian words (one or more words, up to 5), where each word is included in apexes. "
                  "You have to generate a random text (composed by one or more sentences) which must include, at least once, all the input words passed as role 'user'."
                  " The output must be valid JSON and must include: the original input words (parameter name: words_list), the generated text in slovenian language,"
                  "and the italian translation of the same text. ")


response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": system_content
    },
    {
      "role": "user",
      "content": "'tekmovanja'"
    }
  ],
  temperature=0.8,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)


data_str = response.choices[0].message.content

print(data_str)

print()
print("***")

data_json = json.loads(data_str)
#
# # Now, data_json is a dictionary.
print(data_json['slovenian_text'])
