# Generated by Django 4.2.4 on 2023-11-05 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_projectinvite_message_alter_teaminvite_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permissions',
            old_name='can_edit_user_permission',
            new_name='can_edit_user',
        ),
    ]
