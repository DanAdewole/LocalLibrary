# Generated by Django 4.1.7 on 2023-04-03 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_book_language'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Language',
            new_name='language',
        ),
    ]
