# Generated by Django 2.2.14 on 2020-07-25 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelinecomment',
            name='Timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='timelinepost',
            name='Timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
