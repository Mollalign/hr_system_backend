# ===============================================================
# PAYROLL MODEL
# ===============================================================
# import the necessary modules
from django.db import models
import uuid
from django.core.validators import MinValueValidator

# ===============================
# PAYROLL MODEL
# ===============================
class Payroll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    employee_id = models.ForeignKey('employees.Employee', on_delete=models.PROTECT, verbose_name="Employee", null=False, blank=False, related_name="payrolls")

    # Salary Info
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Basic Salary", null=False, blank=False, default=0.00)
    allowance = models.JSONField(default=list, verbose_name="Allowance", null=False, blank=False )
    deduction = models.JSONField(default=dict, verbose_name="Deduction", null=False, blank=False )
    payment_date = models.DateField(verbose_name="Payment Date", null=False, blank=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"
        db_table = "payrolls"

    def __str__(self):
        return f"{self.employee_id.full_name} - {self.payment_date}"