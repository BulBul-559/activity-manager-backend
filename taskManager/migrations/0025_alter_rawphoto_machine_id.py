# Generated by Django 5.0.6 on 2024-07-07 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0024_machine_alias_rawphoto_machine_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rawphoto",
            name="machine_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="taskManager.machine",
            ),
        ),
    ]
