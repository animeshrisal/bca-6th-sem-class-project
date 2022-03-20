import math
from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth import authenticate, login, logout

from .ml import get_recommendation_for_movie

from .forms import MovieForm, ReviewForm, UploadForm
from .models import Movie, Review
# from .ml import get_recommendation_for_movie

from django.db import transaction
import pandas as pd

def home(request):
    return render(request, 'index.html')  

def number(request, id):
    return HttpResponse("Number: " + str(id))  

def get_movie_info(request, id):
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.movie_id = id
                review.user_id = request.user.id
                review.save()
        
        movie = Movie.objects.get(id=id)
        reviews = Review.objects.filter(
            movie=movie
        ).order_by('-created_at')[0:4]
    
        context = {
            'is_favorite': False
        }

        movie_ids = get_recommendation_for_movie(id)

        recommended_movies = Movie.objects.filter(id__in=movie_ids)

        if movie.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True

        return render(request, 'movie.html', 
        {   
            'reviews': reviews,
            'review_form': review_form,
            'movie': movie, 
            'context': context,
            'recommended_movies': recommended_movies
        })

    except Movie.DoesNotExist:
        return render(request, '404.html')

def get_movies(request, page_number):
    page_size = 10

    if page_number < 1:
        page_number = 1

    movie_count = Movie.objects.count()

    last_page = math.ceil(movie_count / page_size)
    
    pagination = {
        'previous_page': page_number - 1,
        'current_page': page_number,
        'next_page': page_number + 1,
        'last_page': last_page
    }

    movies = Movie.objects.all()[(page_number-1)
                                 * page_size:page_number*page_size]
    return render(request, 'movies.html',
         {'movies': movies, 'pagination': pagination})


def post_movie(request):
    form = MovieForm()

    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

            return redirect('/movies/page/1')

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

def delete_movie(request, id):
    movie = Movie.objects.get(pk=id)
    movie.delete()
    return redirect('/movies/page/1')

def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/movies/page/1')

    return render(request, 'signin.html', {'form': form})

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/movies/page/1')

    return render(request, 'signup.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/movies/page/1')

def add_to_favorite(request, id):
    movie = Movie.objects.get(id=id)
    movie.favorite.add(request.user)

    return redirect('/movies/{0}'.format(id))

def remove_from_favorites(request, id):
    movie = Movie.objects.get(id=id)
    movie.favorite.remove(request.user)

    return redirect('/movies/{0}'.format(id))


def get_user_favorites(request):
    movies = request.user.favorite.all()
    return render(request, 'user_favorite.html', {'movies': movies})


def upload_dataset(request):
    file_form = UploadForm()
    error_messages = {}

    if request.method == "POST":
        print("Got here!")
        file_form = UploadForm(request.POST, request.FILES)
        try:
            print(file_form.is_valid())
            if file_form.is_valid():
                dataset = pd.read_csv(request.FILES['file'])
                new_movies_list = []
                dataset['budget'] = dataset['budget'].fillna(0)
                print("Got here")
                with transaction.atomic():
                    for index, row in dataset.iterrows():
                        movie = Movie(
                            title=row['title'],
                            budget=row['budget'],
                            genres=row['genres'],
                            keywords=row['keywords'],
                            overview=row['overview'],
                            tagline=row['tagline'],
                            cast=row['cast'],
                            director=row['director']
                        )

                        new_movies_list.append(movie)
                
                Movie.objects.bulk_create(new_movies_list)
                return redirect('/movies/page/1')

        except Exception as e:
            print(e)
            error_messages['error'] = e

    return render(request, 'upload_dataset.html', {'form': file_form, 'error_messages': error_messages})

