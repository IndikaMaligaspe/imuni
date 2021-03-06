# Generated by Django 2.2 on 2020-06-07 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0009_auto_20200607_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField(choices=[('ONE', 1), ('OND_AND_HALF', 1.5), ('TWO', 2), ('TWO_AND_HALF', 2.5), ('THREE', 3), ('THRE EAND_HALF', 3.5), ('FOUR', 4), ('FOR ANDJALF', 4.5), ('FIVE', 5)], default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='courses.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
