# Generated by Django 4.2.7 on 2023-12-01 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_rename_name_test_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='title',
            new_name='name',
        ),
    ]
