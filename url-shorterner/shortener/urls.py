from . import views

from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.home_view, name='home'),
    path(r'^/[A-Z0-9a-z]{7}', views.to_origin, name='to_origin'),
    path('api/v1/data/shorten', csrf_exempt(views.RESTShortener.as_view()), name='shorten'),
]
