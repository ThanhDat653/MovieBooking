# Generated by Django 5.2 on 2025-05-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_movie_end_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="trailer",
            field=models.URLField(blank=True, help_text="Đường dẫn video trailer"),
        ),
    ]
