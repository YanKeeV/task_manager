# Generated by Django 4.2.5 on 2023-10-10 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tag',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
