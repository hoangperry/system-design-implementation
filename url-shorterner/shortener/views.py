import os

from .models import Shorten
from .base62 import encode

from unique_id_generator.id_gen import IdGen
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# machine_id is ID of this machine, to avoid collision across server
MACHINE_ID = int(os.environ.get('MACHINE_ID', 123))
distributed_id_generator = IdGen(machine_id=MACHINE_ID)


def home_view(request):
    return render(request, 'index.html')


def to_origin(request):
    shorten_path = request.path
    if '/' in shorten_path:
        shorten_path = shorten_path[1:]
    if len(shorten_path) != 7:
        # Raise 404 or return a noti
        return render(request, 'index.html')

    query_result = Shorten.objects.filter(shorten=shorten_path).first()
    if query_result is None:
        return render(request, 'index.html')

    return redirect(query_result.origin, permanent=True)


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
