import logging
import networkx

from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils import timezone

from . import models
from . import network

LOG = logging.getLogger(__name__)



class LoginForm(forms.Form):
    login_pin = forms.IntegerField(label='Your secret PIN', required=True)

class LinkForm(forms.Form):
    link_pin = forms.IntegerField(label='Link to PIN', required=True)

def index(request):
    context = { }
    round = context['round'] = models.Game.round_class()

    # Login handling
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            LOG.info('logging in')
            pin = login_form.cleaned_data['login_pin']
            qs = models.Person.objects.filter(secret_pin=pin)
            if qs.count() == 1:
                request.session['user_id'] = qs.get().id
                messages.add_message(request, messages.INFO, 'Logged in')
            else:
                messages.add_message(request, messages.WARNING, 'Wrong login PIN')
                request.session['user_id'] = None
    else:
        login_form = LoginForm()
    context['login_form'] = login_form

    # Check log in
    user_id = context['user_id'] = request.session.get('user_id', None)
    user = context['user'] = None
    if user_id:
        user = context['user'] = models.Person.objects.get(id=user_id)
        #messages.add_message(request, messages.WARNING, 'user=%s'%context['user'])
        user.ts_lastactive = timezone.now()
        user.save()


    # See if any messages need sending
    if request.method == 'POST' and user and round.send_messages:
        for key, value in request.POST.items():
            if not key.startswith('send_'):
                continue
            if not value:
                continue
            msg_id = int(key.rsplit('_',1)[1])
            msg = models.Message.objects.get(id=msg_id)
            if msg.current_holder != user:
                LOG.error("User trying to send message that isn't theirs: %s, %s"%(user, msg))
                messages.add_message(request, messages.WARNING, "You are trying to relay a message that isn't yours (cheater).")
                continue
            destination_id = int(value)
            qs = models.Person.objects.filter(pin=destination_id)
            if qs.count() != 1:
                messages.add_message(request, messages.WARNING, "Unknown receiver ID: %s"%destination_id)
                continue
            destination = qs.get()
            ret = msg.relay(destination)
            if ret is True:
                messages.add_message(request, messages.INFO, "Your message was sent.")


    # Trying to make a new link?
    if request.method == 'POST' and round.allow_new_links:
        link_form = LinkForm(request.POST)
        if link_form.is_valid():
            LOG.info('making a link')
            # Are they at the max number of links?
            cur_links = models.Link.objects.filter(round=models.current_round(), source=user)
            if round.max_links and cur_links.count() > round.max_links:
                messages.add_message(request, messages.WARNING, "You are at your maximum number of links for this round")
            else:
                # Create the link
                pin = link_form.cleaned_data['link_pin']
                qs = models.Person.objects.filter(pin=pin)
                if qs.count() != 1:
                    messages.add_message(request, messages.WARNING, "Unknown linkee ID: %s"%pin)
                else:
                    other = qs.get()
                    if models.Link.objects.filter(source=user, destination=other).count() > 0:
                        messages.add_message(request, messages.WARNING, "You can't make another link with someone you've already linked to.")
                    else:
                        link = models.Link(source=user, destination=other)
                        link.save()
                        messages.add_message(request, messages.INFO, "You've linked to %s."%other.name)

    # Make new messages if none right now
    if user and round.auto_create_messages:
        user.auto_make_messages()



    if request.method == 'POST':
        return HttpResponseRedirect(request.path)
    return TemplateResponse(request, 'msggame/main.html', context)


def status(request):
    context = { }
    context['people'] = models.Person.objects.all()
    return TemplateResponse(request, 'msggame/status.html', context)

def network_digraph(request):
    G = network.get_network()
    return HttpResponse('\n'.join("%s %s"%(a,b) for (a,b) in G.edges()),
                        content_type='text/plain')

def network_temporal(request):
    G = network.get_network()
    return HttpResponse('\n'.join("%s %s"%(a,b) for (a,b) in G.edges()),
                        content_type='text/plain')

def network_stats(request):
    G = network.get_network()
    lines = [ ]
    for funcname in ['degree_centrality',
                     'in_degree_centrality',
                     'out_degree_centrality',
                     'betweenness_centrality']:
        lines.append("%s: %s"%(funcname, getattr(networkx, funcname)(G)))
    return HttpResponse('\n'.join(lines),
                        content_type='text/plain')
    #return TemplateResponse(request, 'msggame/status.html', context)
