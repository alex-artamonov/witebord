# Generated by Django 4.1.2 on 2022-10-16 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ads", "0007_alter_tag_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="guild",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="pics/guilds"),
        ),
    ]
