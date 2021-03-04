from django.shortcuts import render, redirect
from list_app.models import Words, Sentences, Films, Characters, Actors
from django.db.models import Q
from django.core.paginator import Paginator


def filters(request):
    context = {
        'actors': Actors.objects.all(),
        'films': Films.objects.all(),
        'words': Words.objects.all()
    }
    return context


# Search, Filter
def search(request):
    sentence = None
    word = None
    filtering = filters(request)
    actor = ""

    if request.method == "GET":
        # the query name of search formsets
        if "query" in request.GET:
            if request.GET['query'] != "":
                request_query = request.GET.get('query')
                sentence = Sentences.objects.all()
                verb_option = request.GET.get("verb-option")
                # loop sentence
                if request.GET['formsets-option'] == "contains":
                    sentence = sentence.filter(
                        Q(orth__contains=request_query) |
                        Q(tag__contains=request_query) |
                        Q(pron__contains=request_query)
                    ).exclude(tag='Pu').filter(tag__contains=verb_option)
                elif request.GET['formsets-option'] == "is":
                    sentence = sentence.filter(
                        Q(orth__iexact=request_query) |
                        Q(tag__iexact=request_query) |
                        Q(pron__iexact=request_query)
                    ).exclude(tag='Pu').filter(tag__iexact=verb_option)
                elif request.GET['formsets-option'] == "start_with":
                    sentence = sentence.filter(
                        Q(orth__startswith=request_query) |
                        Q(tag__startswith=request_query) |
                        Q(pron__startswith=request_query)
                    ).exclude(tag='Pu').filter(tag__startswith=verb_option)
                elif request.GET['formsets-option'] == "end_with":
                    sentence = sentence.filter(
                        Q(orth__endswith=request_query) |
                        Q(tag__endswith=request_query) |
                        Q(pron__endswith=request_query)
                    ).exclude(tag='Pu').filter(tag__endswith=verb_option)
            else:
                return redirect("search:search")

        if sentence:
            paginator = Paginator(sentence, 20)
            page_number = request.GET.get('page_number')
            sentence = paginator.get_page(page_number)
    context = {
        'sentences': sentence,
        'filter': filtering
    }
    return render(request, "search/search.html", context)
