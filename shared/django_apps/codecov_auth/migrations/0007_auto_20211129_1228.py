# Generated by Django 3.1.13 on 2021-11-29 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("codecov_auth", "0006_auto_20211123_1535")]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE owners ALTER COLUMN plan SET DEFAULT 'users-basic';"
        )
    ]