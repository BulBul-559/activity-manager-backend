# Generated by Django 5.0.6 on 2024-07-03 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0008_machineborrowrecord_borrow_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machineborrowrecord",
            name="borrow_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
