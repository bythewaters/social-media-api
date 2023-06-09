# Generated by Django 4.2.1 on 2023-05-13 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "likes",
            "0002_remove_reaction_dislike_remove_reaction_like_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="reaction",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reaction",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="reaction",
            name="reaction",
            field=models.CharField(
                choices=[("LIKE", "Like"), ("DISLIKE", "Dislike")],
                default=2,
                max_length=63,
            ),
            preserve_default=False,
        ),
    ]
