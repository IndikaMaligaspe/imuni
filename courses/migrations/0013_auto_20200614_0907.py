# Generated by Django 2.2 on 2020-06-14 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20200608_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='content_summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='requirements',
            field=models.TextField(blank=True),
        ),
    ]