# Generated by Django 4.1.6 on 2023-02-27 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]