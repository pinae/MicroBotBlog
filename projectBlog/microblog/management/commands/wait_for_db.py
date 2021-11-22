#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Checking the connection to the database.')
        database_connected = False
        while not database_connected:
            try:
                connection.ensure_connection()
                database_connected = True
            except OperationalError:
                print(self.style.ERROR(
                    "Database still unavailable."),
                    end='')
                print(" Waiting 1 second.")
                time.sleep(1)
        print(self.style.SUCCESS('Database available!'))