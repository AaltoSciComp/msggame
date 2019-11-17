# Generated by Django 2.2.7 on 2019-11-17 02:45

from django.db import migrations, models
import msggame.models


class Migration(migrations.Migration):

    dependencies = [
        ('msggame', '0003_message_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='generation',
            field=models.IntegerField(default=msggame.models.current_generation),
        ),
        migrations.AddField(
            model_name='relay',
            name='generation',
            field=models.IntegerField(default=msggame.models.current_generation),
        ),
        migrations.AlterField(
            model_name='link',
            name='generation',
            field=models.IntegerField(default=msggame.models.current_generation),
        ),
    ]
