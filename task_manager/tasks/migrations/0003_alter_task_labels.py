# Generated by Django 4.1.6 on 2023-03-23 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(through='tasks.TaskLabel', to='labels.label', verbose_name='Labels'),
        ),
    ]
