# Generated by Django 4.2.1 on 2023-05-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_alter_post_created_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_time",
            field=models.DateTimeField(),
        ),
    ]
