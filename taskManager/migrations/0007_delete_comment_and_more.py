# Generated by Django 5.0.6 on 2024-07-03 12:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("taskManager", "0006_alter_machineborrowrecord_borrow_time"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
        migrations.RenameField(
            model_name="machineborrowrecord",
            old_name="borrow_time",
            new_name="start_time",
        ),
    ]
