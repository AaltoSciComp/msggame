from django.test import Client, TestCase

from . import models
from .models import Person, Message, Link, Relay

class ModelTests(TestCase):
    fixtures = ['testdata.yaml']
    def test_add_link(self):
        """Test adding a link using model API"""
        a = Person.objects.get(name='A')
        b = Person.objects.get(name='B')
        assert Link.objects.filter(source=a, destination=b).count() == 0
        a.add_link(b)
        assert Link.objects.filter(source=a, destination=b).count() == 1

    def test_game(self):
        """Test relaying a message using model API"""
        a = Person.objects.get(name='A')
        b = Person.objects.get(name='B')
        m1 = Message.objects.get(id=1)

        assert m1.current_holder == a
        m1.relay(b)
        assert m1.current_holder == b
        assert m1.relays == 1

class ViewTests(TestCase):
    fixtures = ['testdata.yaml']

    def test_login(self):
        """Test logging in"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        c.get('/')
        assert c.session.get('user_id') is None
        c.post('/', {'login_pin': '1'})
        assert c.session['user_id'] == 1

        c.post('/', {'login_pin': '-50'})
        assert c.session['user_id'] is None

    def test_sending(self):
        """Test login and sending the pre-made message"""
        # Login
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        c.post('/', {'login_pin': '1'})
        response = c.get('/')
        # Test that the message defined in testdata.yaml is there
        assert response.status_code == 200
        assert 'send_1' in response.content.decode()
        # Send the message, assert it isn't there anymore.
        response = c.post('/', {'send_1': '33'})
        assert response.status_code in {200, 302}
        assert 'send_1' not in response.content.decode()



