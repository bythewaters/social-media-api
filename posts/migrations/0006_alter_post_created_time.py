# Generated by Django 4.2.1 on 2023-05-15 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0005_alter_post_created_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023,
                    5,
                    15,
                    10,
                    56,
                    28,
                    715686,
                    tzinfo=datetime.timezone.utc,
                )
            ),
        ),
    ]
