# Generated by Django 4.1.2 on 2022-10-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Guild",
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
                (
                    "name",
                    models.CharField(
                        max_length=25, unique=True, verbose_name="Наименование"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
            ],
            options={
                "verbose_name": "Гильдия",
                "verbose_name_plural": "Гильдии",
                "ordering": ["-name"],
            },
        ),
    ]
