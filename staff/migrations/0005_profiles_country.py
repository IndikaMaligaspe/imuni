# Generated by Django 2.2 on 2020-07-21 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('staff', '0004_auto_20200721_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_country', to='home.Countries'),
            preserve_default=False,
        ),
    ]