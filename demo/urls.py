"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.home),
    path('number/<int:id>', views.number),
    path('index/', views.template_test),
    path('movies/', views.get_movies),
    path('movies/<int:id>', views.get_movie_info),
    path('post_movie/', views.post_movie),
    path('movies/<int:id>/update', views.update_movie),
    path('admin/', admin.site.urls),
]