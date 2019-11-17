import logging

from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib import messages
from . import models



LOG = logging.getLogger(__name__)



class LoginForm(forms.Form):
    pin = forms.IntegerField(label='Your secret PIN', required=True)

def index(request):
    context = { }

    LOG.error('index POST')

    # Login handling
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            LOG.error('logging in')
            pin = login_form.cleaned_data['pin']
            if models.Person.objects.filter(secret_pin=pin).count() == 1:
                request.session['user_id'] = models.Person.objects.get(secret_pin=pin).id
                messages.add_message(request, messages.INFO, 'Logged in')
            else:
                messages.add_message(request, messages.WARNING, 'Wrong login PIN')
                request.session['user_id'] = None
    else:
        login_form = LoginForm()
    context['login_form'] = login_form

    # Chck log in
    user_id = context['user_id'] = request.session.get('user_id', None)
    if user_id:
        context['user'] = models.Person.objects.get(id=user_id)
        messages.add_message(request, messages.WARNING, 'user=%s'%context['user'])




    return TemplateResponse(request, 'msggame/main.html', context)


def status(request):
    context = { }
    context['people'] = models.Person.objects.all()
    return TemplateResponse(request, 'msggame/status.html', context)
