# Generated by Django 2.2.12 on 2020-11-05 13:58

from django.db import migrations, models
import django.db.models.deletion
import otree.db.idmap
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('accepted_chat_count', otree.db.models.IntegerField(null=True)),
                ('is_reported', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('will_be_detected', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('will_be_sued', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('reputation_num', otree.db.models.IntegerField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartelgame_group', to='otree.Session')),
            ],
            options={
                'db_table': 'cartelgame_group',
            },
            bases=(models.Model, otree.db.idmap.GroupIDMapMixin),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('last_round', otree.db.models.IntegerField(choices=[(8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], null=True)),
                ('treatment', otree.db.models.StringField(max_length=20, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartelgame_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'cartelgame_subsession',
            },
            bases=(models.Model, otree.db.idmap.SubsessionIDMapMixin),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_role', otree.db.models.StringField(max_length=10000, null=True)),
                ('units_sold', otree.db.models.IntegerField(default=0, null=True)),
                ('gross_earnings', otree.db.models.CurrencyField(default=0, null=True)),
                ('penalty', otree.db.models.CurrencyField(default=0, null=True)),
                ('additional_penalty', otree.db.models.CurrencyField(default=0, null=True)),
                ('net_earnings', otree.db.models.CurrencyField(default=0, null=True)),
                ('accepted_chat', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('agree_count', otree.db.models.IntegerField(choices=[(4, 'All 4'), (3, 'Only 3'), (2, 'Only 2'), (0, 'No one')], null=True, verbose_name='How many players in your group agreed on a common offer price in this round?')),
                ('common_price', otree.db.models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], null=True, verbose_name='What price did you agree on?')),
                ('price', otree.db.models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], null=True)),
                ('reported', otree.db.models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('report_time', otree.db.models.IntegerField(blank=True, null=True)),
                ('report_page', otree.db.models.StringField(blank=True, max_length=30, null=True)),
                ('first_to_report', otree.db.models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cartelgame.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartelgame_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartelgame_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartelgame.Subsession')),
            ],
            options={
                'db_table': 'cartelgame_player',
            },
            bases=(models.Model, otree.db.idmap.PlayerIDMapMixin),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartelgame.Subsession'),
        ),
    ]
