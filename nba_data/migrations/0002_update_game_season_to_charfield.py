# Generated by Django 5.2 on 2025-04-14 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nba_data", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="season",
            field=models.CharField(max_length=9),
        ),
    ]
