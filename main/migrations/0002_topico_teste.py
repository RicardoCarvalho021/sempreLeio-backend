# Generated by Django 3.1.6 on 2022-02-20 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topico',
            name='teste',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]