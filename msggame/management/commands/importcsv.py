import csv

from django.core.management.base import BaseCommand, CommandError

from ... import models

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('input', nargs=1)

    def handle(self, *args, **options):
        reader = csv.DictReader(open(options['input'][0]))
        for line in reader:
            print(line)
            person = models.Person(name=line['name'],
                                   pin=line['pin'],
                                   secret_pin=line['secret_pin'])
            person.save()

