from django.core.management.base import BaseCommand
from deduction.models import Deduction

class Command(BaseCommand):
    help = "Seed default deduction categories (Tax, Pension, Other)"

    def handle(self, *args, **kwargs):
        default_categories = ["Tax", "Pension", "Other"]
        for cat in default_categories:
            Deduction.objects.get_or_create(
                type=cat,
                defaults={"description": f"Default {cat} rules", "data": []}
            )
        self.stdout.write(self.style.SUCCESS("Deduction categories seeded!"))
