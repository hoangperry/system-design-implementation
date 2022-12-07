import os

from .models import Shorten
from unique_id_generator.id_gen import IdGen

from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

dsitributed_id_generator = IdGen()


def home_view(request):
    final_response = {
        'page_info': {
            'name': 'HTI R&D Dashboard - Home',
            'url': '/'
        }
    }
    return render(request, 'index.html', final_response)


class RESTShortener(APIView):
    @staticmethod
    def post(request):
        original_url = request.POST.get('original_url', '')
        return Response({'a': 1}, status=status.HTTP_200_OK)
