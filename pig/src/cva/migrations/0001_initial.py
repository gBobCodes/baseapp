# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 19:35
from __future__ import unicode_literals
import os

from django.db import migrations, models
from django.contrib.auth.management import create_permissions
from django.db import migrations


def create_admin(apps, schema_editor):
    """Assign admin users the Admin group"""
    Group = apps.get_model('auth', 'group')
    User = apps.get_model('auth', 'user')

    admin_users = os.getenv('ADMIN_USERS', '').split()
    admin_group = Group.objects.get(name="Administrator")

    if admin_users:
        for username in admin_users:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.groups.add(admin_group)


def add_permission(apps, schema_editor):
    """Add the auth.change_user perm to the Administrator group."""
    Group = apps.get_model('auth', 'group')
    Permission = apps.get_model('auth', 'permission')
    admin_group = Group.objects.get(name='Administrator')
    perm = Permission.objects.get(codename='change_user')
    admin_group.permissions.add(perm)

def create_groups(apps, schema_editor):
    """Create the Groups if they do not exist."""
    Group = apps.get_model('auth', 'group')
    group_names = [
        'Administrator',
        'Engineer',
        'Liaison',
        'PM',
    ]
    for group_name in group_names:
        Group.objects.get_or_create(name=group_name)

def migrate_permissions(apps, schema_editor):
    """
    Create the permissions so we can add a permission to a group.
    http://stackoverflow.com/questions/31735042/adding-django-admin-permissions-in-a-migration-permission-matching-query-does-n
    Without this method, we get this error when running the migrations:
    __fake__.DoesNotExist: Permission matching query does not exist.
    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

def remove_groups(apps, schema_editor):
    """Remove all Groups."""
    Group = apps.get_model('auth', 'group')
    Group.objects.all().delete()


class Migration(migrations.Migration):
    """Create the Groups for the Content Exchange application."""
    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('name', models.TextField(editable=False, primary_key=True, serialize=False, verbose_name='Configuration option')),
                ('value', models.TextField(verbose_name='Configuration value')),
            ],
        ),
        migrations.RunPython(create_groups, remove_groups),
        migrations.RunPython(migrate_permissions, migrations.RunPython.noop),
        migrations.RunPython(add_permission, migrations.RunPython.noop),
        migrations.RunPython(create_admin, migrations.RunPython.noop),
    ]
