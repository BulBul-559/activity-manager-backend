# Generated by Django 5.0.6 on 2024-07-01 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0004_machine_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=20)),
                ("time", models.DateTimeField(max_length=20)),
                ("content", models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name="MachineBorrowHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_time", models.DateTimeField(auto_now_add=True)),
                ("finish_time", models.DateTimeField(null=True)),
                ("actual_finish_time", models.DateTimeField(blank=True, null=True)),
                ("borrow_reason", models.CharField(default="", max_length=1000)),
                ("return_description", models.CharField(default="", max_length=1000)),
                ("is_return", models.BooleanField(default=False)),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskManager.machine",
                    ),
                ),
                (
                    "youtholer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskManager.youtholer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MachineBorrowRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_time", models.DateTimeField(auto_now_add=True)),
                ("finish_time", models.DateTimeField()),
                ("borrow_reason", models.CharField(default="", max_length=1000)),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskManager.machine",
                    ),
                ),
                (
                    "youtholer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskManager.youtholer",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="MachineAlloc",
        ),
    ]
