from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'budget', 'genres']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class UploadForm(forms.Form):
    file = forms.FileField()
