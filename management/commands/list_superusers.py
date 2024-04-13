# myapp/management/commands/list_superusers.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'List all superusers'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        if superusers.exists():
            self.stdout.write(self.style.SUCCESS("Superusers:"))
            for user in superusers:
                self.stdout.write(f"- {user.username}")
        else:
            self.stdout.write("No superusers found")