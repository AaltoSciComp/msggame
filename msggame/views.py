from django.shortcuts import render

from django.http import HttpResponse

from django.template.response import TemplateResponse
from . import models

def index(request):
    return HttpResponse("Hello, world.")


def status(request):
    context = { }
    context['people'] = models.Person.objects.all()
    return TemplateResponse(request, 'msggame/status.html', context)
