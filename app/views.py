from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import MovieForm
from .models import Movie

def home(request):
    return HttpResponse("Home Page")    

def number(request, id):
    return HttpResponse("Number: " + str(id))  

def template_test(request):
    return render(request, 'index.html')

def get_movie_info(request, id):
    try:
        movie = Movie.objects.get(id=id)
        return render(request, 'movie.html', {'movie': movie})
    except Movie.DoesNotExist:
        return render(request, '404.html')

def get_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})

def post_movie(request):
    form = MovieForm()

    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

            return redirect('/movies/')

    return render(request, 'post_movie.html', {'form': form})

def update_movie(request, id):
    movie = Movie.objects.get(pk=id)

    if request.method == "POST":
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie_form.save()
            return redirect('/movies/{}'.format(id))
    elif request.method == "GET":
        movie_form = MovieForm(instance=movie)
    return render(request, 'update_movie.html', {'form': movie_form})