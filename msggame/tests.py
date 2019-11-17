from django.test import Client, TestCase

from . import models
from .models import Person, Message, Link, Relay

class Tests(TestCase):
    fixtures = ['testdata.yaml']
    def test_add_link(self):
        a = Person.objects.get(name='A')
        b = Person.objects.get(name='B')
        assert Link.objects.filter(source=a, destination=b).count() == 0
        a.add_link(b)
        assert Link.objects.filter(source=a, destination=b).count() == 1

    def test_game(self):
        a = Person.objects.get(name='A')
        b = Person.objects.get(name='B')
        m1 = Message.objects.get(id=1)

        assert m1.current_holder == a
        m1.relay(b)
        assert m1.current_holder == b
        assert m1.relays == 1


    def test_login(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        c.get('/')
        assert c.session.get('user_id') is None
        c.post('/', {'pin': '1'})
        assert c.session['user_id'] == 1

        c.post('/', {'pin': '-50'})
        assert c.session['user_id'] is None
