# Generated by Django 2.2.7 on 2019-11-18 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msggame', '0002_auto_20191118_0021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='round',
            options={'get_latest_by': 'round'},
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('round', 'source', 'destination')},
        ),
    ]
