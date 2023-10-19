from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from core.models import get_number_of_examples, parse_json_and_create_instances
from libopenai.tools import generate_example_text_slo_ita


@login_required
@csrf_exempt
@require_POST
def produce_examples(request):
    word_list = request.POST.getlist('word_list')
    slo2ita = request.POST.get('slo2ita') == 'True'
    number_of_sentences = int(request.POST.get('number_of_sentences', 0))

    # Validate parameters
    if not word_list or len(word_list) < 1:
        return JsonResponse({
            "success": False,
            "error": {
                "code": "WRONG_PARAMETERS",
                "message": "Invalid parameters",
                "details": "word_list missing or empty"
            }
        }, status=400)  # 400 is for Bad Request. You can use other status codes as appropriate.

    # Your logic to generate examples goes here.
    # For the sake of this example, I'll just return the same input.

    response_data = {
        'word_list': word_list,
        'slo2ita': slo2ita,
        'number_of_sentences': number_of_sentences,
    }

    return JsonResponse(response_data)


@login_required
@csrf_exempt
@require_POST
def produce_slo_ita_example(request):
    word_list = request.POST.getlist('word_list')

    # Validate parameters
    if not word_list or len(word_list) < 1:
        return JsonResponse({
            "success": False,
            "error": {
                "code": "WRONG_PARAMETERS",
                "message": "Invalid parameter: word_list",
                "details": "word_list missing or empty"
            }
        }, status=400)  # 400 is for Bad Request. You can use other status codes as appropriate.

    try:
        max_num_examples_per_word_list = int(request.POST.get('max_num_examples_per_word_list', 1))
    except ValueError:
        max_num_examples_per_word_list = 1

    # Validate parameters
    if max_num_examples_per_word_list < 1 or max_num_examples_per_word_list > 10:
        return JsonResponse({
            "success": False,
            "error": {
                "code": "WRONG_PARAMETERS",
                "message": "Invalid parameter: max_num_examples_per_word_list",
                "details": "max_num_examples_per_word_list must be between 1 and 10"
            }
        }, status=400)  # 400 is for Bad Request. You can use other status codes as appropriate.

    # for word in word_list:
    #     print(word)

    if rs := get_number_of_examples(word_list, language='slovenian', return_list=True):
        if rs.count() >= max_num_examples_per_word_list:
            return JsonResponse({
                "success": True,
                "message": "There are already enough examples for the provided words",
                "data": {
                        "result": {r.id: r.to_json() for r in rs},
                        # "word_list": word_list,
                        "language": "slo_to_ita"
                        },
            })

    # check is user is allowed to create new examples
    if not request.user.is_superuser:
        return JsonResponse({
            "success": False,
            "error": {
                "code": "NOT_ALLOWED",
                "message": "user is not allowed to use openai",
                "details": ""
            }
        }, status=400)  # 400 is for Bad Request. You can use other status codes as appropriate.

    data_json, data_str, response = generate_example_text_slo_ita(word_list)

    instance = parse_json_and_create_instances(data_json, language='slovenian', check_presence=True)

    results = [instance]
    results.extend(rs)

    return JsonResponse({
        "success": True,
        "message": "new example created",
        "data": {
            "result": {r.id: r.to_json() for r in results},
            # "word_list": word_list,
            "language": "slo_to_ita"
        },
    })


def homepage(request):
    # return an empty html page

    return HttpResponse("<html><body><h1>Homepage</h1></body></html>")
