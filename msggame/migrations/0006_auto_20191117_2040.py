# Generated by Django 2.2.7 on 2019-11-17 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msggame', '0005_auto_20191117_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='public_pin',
            new_name='pin',
        ),
        migrations.AddField(
            model_name='generation',
            name='auto_create_messages',
            field=models.BooleanField(default=True),
        ),
    ]
