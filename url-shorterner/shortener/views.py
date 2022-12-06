import os

from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


def home_view(request):
    final_response = {
        'page_info': {
            'name': 'HTI R&D Dashboard - Home',
            'url': '/'
        }
    }
    return render(request, 'page/index.html', final_response)


class RESTShortener(APIView):
    @staticmethod
    def post(request):

        return Response({'a': 1}, status=status.HTTP_200_OK)
