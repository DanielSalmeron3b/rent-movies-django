# Generated by Django 4.1 on 2022-08-31 08:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MovieAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(13)])),
                ('wallet', models.IntegerField(default=0)),
                ('area', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='movie_admin_portal.area')),
                ('movie_admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=20)),
                ('genre', models.CharField(max_length=10)),
                ('duration', models.CharField(max_length=10)),
                ('is_available', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=100)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movie_admin_portal.movieadmin')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movie_admin_portal.area')),
            ],
        ),
    ]
