# ===============================================================
# DEDUCTION MODEL AND DEDUCTION CATEGORY
# ===============================================================
# import the necessary modules
from django.db import models
import uuid

# ===============================
# DEDUCTION CATEGORY MODEL
# ===============================
class AssignedDeduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, verbose_name="Employee", null=False, blank=False, related_name="assigned_deduction")
    deduction_id = models.UUIDField(verbose_name="Deduction ID(from the other deduction data) which will be deducted from the employee", null=False, blank=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Assigned Deduction"
        verbose_name_plural = "Assigned Deductions"
        db_table = "assigned_deduction"

    def __str__(self):
        return self.name

# ===============================
# DEDUCTION MODEL
# ===============================
class Deduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    type = models.CharField(max_length=255, verbose_name="Deduction Type", null=False, blank=False, default='Other')
    description = models.TextField(default='', blank=True, null=True, verbose_name="Description")
    data = models.JSONField(default=list, verbose_name="Deduction Data", null=False, blank=False)
    
    # Status Information    
    is_active = models.BooleanField(default=True, verbose_name="is active", null=False, blank=False) #for tax and pension for other it is always true because it is contine on data for every deducation on other its based on data 
     
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True) 
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Deduction"
        verbose_name_plural = "Deductions"
        db_table = "deductions"

    def __str__(self):
        return self.type