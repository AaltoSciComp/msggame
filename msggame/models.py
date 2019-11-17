import logging
import re

from django.db import models
from django.db.models import F

LOG = logging.getLogger(__name__)


def current_round():
    game = Game.objects.first()
    if game is None:
        return 1
    else:
        return game.round

def random_person():
    p = Person.objects.order_by('?').first()
    return p

class Person(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=50, null=True, blank=True)
    secret_pin = models.IntegerField(null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    centrality = models.FloatField(default=0)
    score = models.FloatField(default=0)
    consent_research = models.BooleanField(default=False)
    consent_research_withname = models.BooleanField(default=False)
    consent_research_open = models.BooleanField(default=False)
    ts_lastactive = models.DateTimeField(null=True, blank=True)

    def add_link(self, destination):
        link = Link(round=1,
                    source=self,
                    destination=destination)
        link.save()

    def auto_make_messages(self):
        messages = self.active_messages
        if len(messages) == 0:
            p = None
            while p is None or p == self:
                p = random_person()
            msg = Message(origin=self,
                          target=p,
                          current_holder=self,
                          )
            msg.save()

    @property
    def active_messages(self):
        messages = self.current_messages.filter(status='Active', round=current_round())
        return messages

    @property
    def completed_messages(self):
        messages = Message.objects.filter(origin=self, status='Completed', round=current_round())
        return messages

    @property
    def current_links(self):
        links = self.link_sources.filter(round=current_round())
        return links

    @property
    def all_links(self):
        links = self.link_sources.filter()
        return links

class Link(models.Model):
    round = models.IntegerField(default=current_round)
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_sources')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_destinations')
    ts_create = models.DateTimeField(auto_now_add=True)
    ts_used = models.DateTimeField(auto_now=True)
    nuses = models.IntegerField(default=0)

class Message(models.Model):
    round = models.IntegerField(default=current_round)
    origin = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_origins')
    target = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_targets')
    current_holder = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='current_messages')
    status = models.TextField(choices=[('ACTIVE', 'Active'), ('COMPLETED','Completed'), ('STALLED', 'Stalled')], default='Active')
    ts_create = models.DateTimeField(auto_now_add=True, null=True)
    ts_last = models.DateTimeField(auto_now=True, null=True)
    ts_received = models.DateTimeField(blank=True, null=True)
    relays = models.IntegerField(default=0)
    path_ids = models.TextField(default="")

    @classmethod
    def new(cls, origin, target):
        msg = cls(origin=origin, target=target, current_holder=origin)
        msg.save()

    def relay(self, destination):
        """Send this message on to the next person"""
        if destination == self.current_holder:
            LOG.info("Atempting to send message to yourself")
            return
        relay = Relay(source=self.current_holder, destination=destination, message=self)
        self.path_ids += str(self.current_holder.id) + ';'
        self.current_holder = destination
        self.relays += 1
        relay.save()
        self.save()

        # Check if we have reached our destination
        if self.current_holder == self.target:
            self.status = 'Completed'
            score = 1000
            #for person_id in reversed(self.path.split(';')):
            for p in reversed(self.path()):
                if p == self.target:
                    continue
                p.score = F('score') + int(score)
                score /= 1.5
                p.save()
            self.origin.score = F('score') + int(score)
            self.origin.save()
            self.save()

    def path(self):
        if not self.path_ids:
            return [ ]
        path = [ ]
        for person_id in re.split(',|;', self.path_ids):
            if not person_id:
                continue
            p = Person.objects.get(id=int(person_id))
            path.append(p)
        return path



class Relay(models.Model):
    round = models.IntegerField(default=current_round)
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_source')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_destination')
    ts = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)



class Game(models.Model):
    round = models.IntegerField(default=0)

    @staticmethod
    def round_class():
        Round.objects.get(round=current_round())



class Round(models.Model):
    round = models.IntegerField(unique=True)
    send_messages = models.BooleanField(default=True)
    max_links = models.IntegerField(default=10)
    allow_new_links = models.BooleanField(default=True)
    disallow_existing_links = models.BooleanField(default=False)
    require_links = models.BooleanField(default=False)
    links_from_relays = models.BooleanField(default=True)
    auto_create_messages = models.BooleanField(default=True)
