# Generated by Django 4.1.2 on 2022-10-16 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0006_alter_guild_name_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                blank=True, max_length=30, null=True, unique=True, verbose_name="Метка"
            ),
        ),
    ]
