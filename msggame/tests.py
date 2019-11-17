from django.test import TestCase

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
