# Generated by Django 5.0.6 on 2024-07-07 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0023_activityentry_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="alias",
            field=models.CharField(default="online", max_length=10),
        ),
        migrations.AddField(
            model_name="rawphoto",
            name="machine_id",
            field=models.ForeignKey(
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="taskManager.machine",
            ),
        ),
    ]
