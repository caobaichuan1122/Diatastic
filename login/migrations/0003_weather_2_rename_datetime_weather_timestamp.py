# Generated by Django 4.0.4 on 2022-08-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_weather'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather_2',
            fields=[
                ('postcode', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('uv', models.FloatField()),
            ],
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='datetime',
            new_name='timestamp',
        ),
    ]
