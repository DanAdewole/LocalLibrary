# Generated by Django 4.1.7 on 2023-04-07 06:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_alter_author_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={"ordering": ["last_name", "first_name"]},
        ),
    ]
