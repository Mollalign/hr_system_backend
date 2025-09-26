from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_hr_data(sender, **kwargs):
    if sender.name == "hr_system":
        Deduction = apps.get_model("hr_system", "Deduction")

        Deduction.objects.get_or_create(
            type="Tax",
            defaults={"description": "Mandatory government income tax deducted from employee salaries in accordance with national tax regulations. This ensures compliance and proper reporting to tax authorities."},
        )
        Deduction.objects.get_or_create(
            type="Pension",
            defaults={"description": "Employee contributions to the national or company-managed pension scheme. This deduction secures retirement benefits and long-term financial security for employees."},
        )
        Deduction.objects.get_or_create(
            type="Other",
            defaults={"description": "Any additional deductions not classified under tax or pension, such as loan repayments, insurance premiums, or voluntary contributions, applied according to company policy or employee agreements."},
        )