from django.shortcuts import render
from .models import Words, Films, Characters, Actors


def listWords(request):
    words = Words.objects.all().exclude(tag='Pu')
    context = {
        'words': enumerate(words),
        'pages': words
    }
    return render(request, 'list_app/words.html', context)


def listCharacters(request):
    chars = Characters.objects.all()
    context = {
        'characters': enumerate(chars),
        'pages': chars
    }
    return render(request, 'list_app/char.html', context)


def listActors(request):
    actors = Actors.objects.all()
    context = {
        'actors': enumerate(actors),
        'pages': actors
    }
    return render(request, 'list_app/actors.html', context)


def listFilms(request):
    films = Films.objects.all()
    context = {
        'films': enumerate(films),
        'pages': films
    }
    return render(request, 'list_app/films.html', context)
