# Generated by Django 2.2.7 on 2019-11-17 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msggame', '0008_person_ts_lastactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='generation',
            name='send_messages',
            field=models.BooleanField(default=True),
        ),
    ]
