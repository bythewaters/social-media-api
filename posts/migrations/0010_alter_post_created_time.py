# Generated by Django 4.2.1 on 2023-05-16 12:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0009_alter_post_created_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
