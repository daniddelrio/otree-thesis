# Generated by Django 2.2.12 on 2020-10-31 06:39

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('cartelgame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsession',
            name='reputation_num',
            field=otree.db.models.IntegerField(null=True),
        ),
    ]
