"""
Management command: ensure_admin
Creates or resets the superuser so Django admin is always accessible.
Usage: python manage.py ensure_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Ensure a superuser exists for Django admin access'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Superuser username (default: admin)')
        parser.add_argument('--password', default='admin123', help='Superuser password (default: admin123)')
        parser.add_argument('--email', default='admin@example.com', help='Superuser email')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" password updated.'))
        self.stdout.write(f'  Username : {username}')
        self.stdout.write(f'  Password : {password}')
        self.stdout.write(f'  Admin URL: http://127.0.0.1:8000/admin/')
