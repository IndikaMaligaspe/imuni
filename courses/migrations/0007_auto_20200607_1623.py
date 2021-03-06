# Generated by Django 2.2 on 2020-06-07 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_thumbnail_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.FloatField(default=5),
        ),
        migrations.AddField(
            model_name='course',
            name='level_choices',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('All Levels', 'All Levels')], default='All Levels', max_length=50),
        ),
    ]
