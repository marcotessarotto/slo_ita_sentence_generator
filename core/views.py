from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def produce_examples(request):
    word_list = request.POST.getlist('word_list')
    slo2ita = request.POST.get('slo2ita') == 'True'
    number_of_sentences = int(request.POST.get('number_of_sentences', 0))

    # Validate parameters
    if not word_list or not (0 < number_of_sentences <= 10):
        return HttpResponseBadRequest("Invalid parameters")


    # Your logic to generate examples goes here.
    # For the sake of this example, I'll just return the same input.

    response_data = {
        'word_list': word_list,
        'slo2ita': slo2ita,
        'number_of_sentences': number_of_sentences,
    }

    return JsonResponse(response_data)


def homepage(request):

    # return an empty html page

    return HttpResponse("<html><body><h1>Homepage</h1></body></html>")