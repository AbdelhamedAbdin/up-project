from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from list_app.models import Words, Sentences, Films, Characters, Actors


def index(request):
    return render(request, 'index/index.html')


def home(request):
    if "query" in request.GET:
        print(request.GET)
        request_query = request.GET.get("query", "")
        sentence = Sentences.objects.all()
        if "formsets-option" in request.GET:
            request.GET['formsets-option'] = "contains"
        if request.GET.get("verb-option"):
            request.GET["verb-option"] = "Pron"
        sentence.filter(
            Q(orth__contains=request_query) |
            Q(tag__contains=request_query) |
            Q(pron__contains=request_query)
        ).exclude(tag__contains='Pu')

        paginator = Paginator(sentence, 20)
        page_number = request.GET.get('page_number')
        sentence = paginator.get_page(page_number)
        # return redirect(reverse_lazy("search:search", kwargs={'sentences': sentence}))
        return redirect("index:home", kwargs={'sentences': sentence})
    return render(request, 'index/home.html')


def old_version(request):
    return render(request, 'index/old_version.html')
