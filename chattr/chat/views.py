from django.shortcuts import render
from django.http import JsonResponse
from .models import Channel


def index(request):
    return render(request, 'index.html', {'channels': Channel.objects.all()})

def channel_list(request):
    return JsonResponse(list(Channel.objects.all().values()), safe=False)


def channel(request, channel_id):
    return render(request, 'channel.html', {'channel': Channel.objects.get(pk=channel_id)})
