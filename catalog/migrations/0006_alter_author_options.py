# Generated by Django 4.1.7 on 2023-04-07 06:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0005_alter_bookinstance_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={
                "ordering": ["last_name", "first_name"],
                "permissions": (
                    ("can_create_author", "Create, Edit and Delete Authors"),
                ),
            },
        ),
    ]
