# Generated by Django 2.2.7 on 2019-11-17 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msggame', '0009_generation_send_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField(unique=True)),
                ('send_messages', models.BooleanField(default=True)),
                ('max_links', models.IntegerField(default=10)),
                ('allow_new_links', models.BooleanField(default=True)),
                ('disallow_existing_links', models.BooleanField(default=False)),
                ('require_links', models.BooleanField(default=False)),
                ('links_from_relays', models.BooleanField(default=True)),
                ('auto_create_messages', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Generation',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='generation',
            new_name='round',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='generation',
            new_name='round',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='generation',
            new_name='round',
        ),
        migrations.RenameField(
            model_name='relay',
            old_name='generation',
            new_name='round',
        ),
    ]