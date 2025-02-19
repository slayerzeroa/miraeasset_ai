# Generated by Django 5.0.7 on 2024-07-17 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="crawling",
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
                ("date", models.DateField(verbose_name="date published")),
                ("title", models.CharField(max_length=100)),
                ("link", models.URLField(max_length=1024)),
                ("content", models.TextField(max_length=2000)),
                ("summary", models.TextField(blank=True, max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name="easy_summary",
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
                ("summary", models.TextField(max_length=2000)),
                ("easy", models.TextField(blank=True, max_length=2000)),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="summary.crawling",
                    ),
                ),
            ],
        ),
    ]
