# Generated by Django 4.1.2 on 2022-10-15 22:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ads", "0003_alter_ad_media_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ad",
            name="media_content",
            field=models.ImageField(blank=True, null=True, upload_to="pics/%Y/%m/%d/"),
        ),
    ]
