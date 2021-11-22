#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            new_admin = User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER', 'admin'),
                email=os.getenv('DJANGO_SUPERUSER_MAIL', 'admin@example.com'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD', 'pass'))
            new_admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
