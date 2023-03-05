# Generated by Django 4.1.6 on 2023-03-05 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_alter_task_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executing_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status', verbose_name='Status'),
        ),
    ]