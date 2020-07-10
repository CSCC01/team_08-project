# Generated by Django 2.2.8 on 2020-07-09 23:02

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ManualTag',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('promo', 'promo'), ('allergy', 'allergy'), ('cuisine', 'cuisine'), ('dish', 'dish')], max_length=20)),
                ('value', models.CharField(max_length=50, unique=True)),
                ('foods', djongo.models.fields.ListField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('restaurant_id', models.CharField(editable=False, max_length=24)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('picture', models.CharField(blank=True, default='', max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tags', djongo.models.fields.ListField(default=[])),
                ('specials', models.CharField(blank=True, max_length=51)),
            ],
            options={
                'unique_together': {('name', 'restaurant_id')},
            },
        ),
    ]
