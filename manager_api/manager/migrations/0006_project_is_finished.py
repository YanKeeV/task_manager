# Generated by Django 4.2.4 on 2023-09-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]