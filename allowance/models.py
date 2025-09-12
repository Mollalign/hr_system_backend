# ===============================================================
# ALLOWANCE MODEL
# ===============================================================
# import the necessary modules
from django.db import models
import uuid
from django.core.validators import MinValueValidator

# ===============================
# ALLOWANCE MODEL
# ===============================
class Allowance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    name = models.CharField(max_length=255, verbose_name="Allowance Name", null=False, blank=False)
    type = models.CharField(max_length=255, choices=[('percentage', 'Percentage Amount'), ('fixed', 'Fixed Amount')], verbose_name="Allowance Type", null=False, blank=False, default='fixed')
    percentage = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Allowance Percentage", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Allowance Amount", null=True, blank=True)
    description = models.TextField(default='', blank=True, null=True, verbose_name="Description")

    # Status Information
    is_active = models.BooleanField(default=True, verbose_name="is active", null=False, blank=False)
    is_deleted = models.BooleanField(default=False, verbose_name="is deleted", null=False, blank=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Allowance"
        verbose_name_plural = "Allowances"
        db_table = "allowances"

    def __str__(self):
        return self.name