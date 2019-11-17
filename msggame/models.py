from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    secret_pin = models.IntegerField(null=True, blank=True)
    public_pin = models.IntegerField(null=True, blank=True)
    centrality = models.FloatField(default=0)
    score = models.FloatField(default=0)

class Link(models.Model):
    generation = models.IntegerField()
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_sources')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='link_destinations')
    ts_create = models.DateTimeField(auto_now_add=True)
    ts_used = models.DateTimeField(auto_now=True)
    nuses = models.IntegerField(default=0)

class Message(models.Model):
    origin = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_origins')
    target = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='message_targets')
    current_holder = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='current_messages')
    status = models.TextField(choices=[('ACTIVE', 'Active'), ('COMPLETED','Completed'), ('STALLED', 'Stalled')], default='Active')
    ts_create = models.DateTimeField(auto_now_add=True)
    ts_last = models.DateTimeField(auto_now=True)
    ts_received = models.DateTimeField(blank=True)
    relays = models.IntegerField(default=0)

class Relay(models.Model):
    source = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_source')
    destination = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relay_destination')
    ts = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
