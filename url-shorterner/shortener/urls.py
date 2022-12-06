from . import views

from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.home_view, name='home view'),
    path('api/v1/data/shorten', csrf_exempt(views.RESTNews.as_view()), name='news'),
]
