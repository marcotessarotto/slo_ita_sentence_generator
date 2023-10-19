import json
import os
import openai
import environ
from pathlib import Path


def get_openai_api_key():
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    return env('OPENAI_API_KEY')


def generate_example_text_slo_ita(word_list, OPENAI_API_KEY=None, temperature=0.8, max_tokens=256, top_p=1):
    """
    generate a random text (composed by one or more sentences) which must include, at least once, all the input words passed as role 'user'.
    The output must be valid JSON and must include: the original input words (parameter name: words_list), the generated text in slovenian language,
    and the correct italian translation of the same text.

    :param word_list:  list of slovenian words (one or more words; N is the number of slovenian words), where each word is included in apexes.
    :param OPENAI_API_KEY:
    :param temperature:
    :param max_tokens:
    :param top_p:
    :return:  data_json, data_str, response

    example of JSON result:

    {
      "words_list": ["tekmovanja"],
      "number_of_sentences": 2,
      "slovenian_text": "Naša šola je organizirala veliko športnih tekmovanj. Tudi letos bomo imeli tekmovanje v teku, kjer se lahko vsi učenci pomerijo.",
      "italian_translation": "La nostra scuola ha organizzato molte competizioni sportive. Anche quest'anno avremo una gara di corsa, in cui tutti gli studenti possono competere."
    }
    """

    if not OPENAI_API_KEY:
        OPENAI_API_KEY = get_openai_api_key()

    openai.api_key = OPENAI_API_KEY

    # system_content = (
    #     "the input is a list of slovenian words (one or more words; N is the number of slovenian words), where each word is included in apexes. "
    #     "You have to generate a random text (composed by one or more sentences) which must include, at least once, all the input words passed as role 'user'."
    #     " The output must be valid JSON and must include: the original input words (parameter name: words_list), the generated text in slovenian language,"
    #     "and the correct italian translation of the same text. "
    #     "Also, in the JSON output, you must include the number of sentences generated in the slovenian text (parameter name: number_of_sentences)."
    #     )

    system_content = (
        "the input is a list of slovenian words, where each word is included in apexes. "
        "You have to generate a random text which must include all the input words passed as role 'user'. Try to minimize the number of sentences generated."
        " The output must be valid JSON and must include: the original input words (parameter name: words_list), the generated text in slovenian language (parameter name: slovenian_text,"
        "and the correct italian translation of the same text (parameter name: 'italian_text'). "
        )

    # system_content = ("the input is a list of slovenian words (one or more words; N is the number of slovenian words), where each word is included in apexes. "
    #                   "You have to generate a random text (composed by one or more sentences) which must include, at least once, all the input words passed as role 'user'."
    #                   " The output must be valid JSON and must include: the original input words (parameter name: words_list), the generated text in slovenian language,"
    #                   "and the correct italian translation of the same text. "
    #                   "Also, in the JSON output, you must include the number of sentences generated in the slovenian text (parameter name: number_of_sentences)."
    #                   "Also, in the JSON output, you must include other N-1 italian texts (grouped in a list called 'wrong_ita_answers')"
    #                   " which are random i.e not even correlated to the 'correct' translation of the generated slovene text."
    #                   )

    str_word_list = ", ".join([f"'{word}'" for word in word_list])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": str_word_list
            }
        ],
        temperature=temperature,  # default 0.8
        max_tokens=max_tokens,  # default 256
        top_p=top_p,  # default 1
        frequency_penalty=0,
        presence_penalty=0
    )

    # print(response)

    try:
        data_str = response.choices[0].message.content
    except Exception:
        data_str = "error"

    try:
        data_json = json.loads(data_str)
    except Exception:
        data_json = { "error": "True" }

    return data_json, data_str, response



if __name__ == '__main__':
    # word_list = ["tekmovanja", "šola", "tek", "učenci", "pomerijo"]
    # word_list = ["tekmovanja", "šola", "tek", "učenci", "pomerijo", "tekmovalci",
    #                 "tekmovanje", "šport", "športni", "športna", "športno", "športne",
    #                 "športnik", "športniki", "športnica", "športnice", "športnico", "športnic",
    #                 "športnikov", "športnikom", "športnikih", "športniku", "športniki",
    #                 "športnikov", "športnikom", "športnikih", "športniku", "športniki",
    #              ]

    word_list = ["tekmovanja", "šola", ]

    data_json, data_str, response = generate_example_text_slo_ita(word_list)

    print(data_json)

