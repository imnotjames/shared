# Generated by Django 5.0.3 on 2024-03-12 01:24

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Owner",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.owner",),
        ),
    ]
