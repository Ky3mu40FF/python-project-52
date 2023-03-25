# Generated by Django 4.1.6 on 2023-03-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0003_alter_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, through='tasks.TaskLabel', to='labels.label', verbose_name='Labels'),
        ),
    ]
