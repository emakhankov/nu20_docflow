# Generated by Django 3.0.3 on 2020-03-15 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docflowuser',
            name='can_add_documents',
            field=models.BooleanField(default=False, verbose_name='can create documents'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='docflowuser',
            name='can_find_documents',
            field=models.BooleanField(default=False, verbose_name='can find documents'),
            preserve_default=False,
        ),
    ]
