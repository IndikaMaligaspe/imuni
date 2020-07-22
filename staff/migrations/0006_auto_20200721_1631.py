# Generated by Django 2.2 on 2020-07-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_profiles_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='address',
            field=models.CharField(db_index=True, default=None, max_length=500, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='city',
            field=models.CharField(db_index=True, default=None, max_length=50, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='mobile',
            field=models.CharField(db_index=True, default=None, max_length=50, verbose_name='mobile'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='phone',
            field=models.CharField(db_index=True, default=None, max_length=50, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='webpage',
            field=models.CharField(db_index=True, default=None, max_length=50, verbose_name='webpage'),
        ),
    ]
