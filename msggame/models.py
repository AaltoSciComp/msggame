from django.db import models

def current_generation():
    game = Game.objects.first()
    if game is None:
        return 0
    else: game.generation

def random_person():
    p = Person.objects.order_by('?').first()
    return p

class Person(models.Model):
    name = models.CharField(max_length=200)
    secret_pin = models.IntegerField(null=True, blank=True)
    public_pin = models.IntegerField(null=True, blank=True)
    centrality = models.FloatField(default=0)
    score = models.FloatField(default=0)

    def add_link(self, destination):
        link = Link(generation=1,
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
        messages = self.current_messages.filter(status='Active')
        return messages

class Link(models.Model):
    generation = models.IntegerField(default=current_generation)
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_sources')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_destinations')
    ts_create = models.DateTimeField(auto_now_add=True)
    ts_used = models.DateTimeField(auto_now=True)
    nuses = models.IntegerField(default=0)

class Message(models.Model):
    generation = models.IntegerField(default=current_generation)
    origin = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_origins')
    target = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_targets')
    current_holder = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='current_messages')
    status = models.TextField(choices=[('ACTIVE', 'Active'), ('COMPLETED','Completed'), ('STALLED', 'Stalled')], default='Active')
    ts_create = models.DateTimeField(auto_now_add=True, null=True)
    ts_last = models.DateTimeField(auto_now=True, null=True)
    ts_received = models.DateTimeField(blank=True, null=True)
    relays = models.IntegerField(default=0)
    path = models.TextField(default="")

    @classmethod
    def new(cls, origin, target):
        msg = cls(origin=origin, target=target, current_holder=origin)
        msg.save()

    def relay(self, destination):
        """Send this message on to the next person"""
        relay = Relay(source=self.current_holder, destination=destination, message=self)
        self.path += str(self.current_holder.id) + ';'
        self.current_holder = destination
        self.relays += 1
        relay.save()
        self.save()

        if self.current_holder == self.target:
            self.status = 'Completed'
            score = 128
            import re
            #for person_id in reversed(self.path.split(';')):
            for person_id in reversed(re.split(',|;', self.path)):
                if not person_id: continue
                p = Person.objects.get(id=int(person_id))
                p.score += score
                score /= 2
            self.origin.score += 128


class Relay(models.Model):
    generation = models.IntegerField(default=current_generation)
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_source')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_destination')
    ts = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

class Game(models.Model):
    generation = models.IntegerField(default=0)
