# Generated by Django 5.0.6 on 2024-06-28 14:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0002_machine_name_machine_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="machine",
            name="machine_id",
        ),
    ]
