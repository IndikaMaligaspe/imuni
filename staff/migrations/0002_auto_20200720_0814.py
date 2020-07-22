# Generated by Django 2.2 on 2020-07-20 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='address',
            field=models.CharField(db_index=True, default='en', max_length=50, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='city',
            field=models.CharField(db_index=True, default='en', max_length=50, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='country',
            field=models.CharField(db_index=True, default=1, max_length=50, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='email_display',
            field=models.CharField(choices=[(0, 'Hide my email address from non-privilage users'), (1, 'Allow everyone to see my email address'), (2, 'Allow only course members to see my email address')], default=0, max_length=500, verbose_name='email_display'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='mobile',
            field=models.CharField(db_index=True, default='en', max_length=50, verbose_name='mobile'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='phone',
            field=models.CharField(db_index=True, default='en', max_length=50, verbose_name='phone'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='webpage',
            field=models.CharField(db_index=True, default='en', max_length=50, verbose_name='webpage'),
        ),
    ]
