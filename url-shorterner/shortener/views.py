import os

from .models import Shorten
from .base62 import encode

from unique_id_generator.id_gen import IdGen
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# machine_id is ID of this machine, to avoid collision across server
MACHINE_ID = int(os.environ.get('MACHINE_ID', 123))
distributed_id_generator = IdGen(machine_id=MACHINE_ID)


def home_view(request):
    final_response = {
        'page_info': {
            'name': 'HTI R&D Dashboard - Home',
            'url': '/'
        }
    }
    return render(request, 'index.html', final_response)


def to_origin(request):
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
        nu_id = distributed_id_generator.generate()
        shorten = encode(nu_id)
        new_shorten = Shorten(
            id=nu_id,
            shorten=shorten,
            origin=original_url,
        )
        new_shorten.save()
        return Response({'shorten': '/' + shorten}, status=status.HTTP_200_OK)
