# Generated by Django 2.2 on 2020-06-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='thumbnail_image',
            field=models.ImageField(blank=True, upload_to='courses/%Y/%m/%d/'),
        ),
    ]