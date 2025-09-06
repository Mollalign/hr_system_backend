from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField

class CompanyAddress(models.Model):
    # ================
    # Basic Information
    # ================
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_name = models.CharField(max_length=255)
    branch_phone = PhoneNumberField(unique=True)
    branch_email = models.EmailField()
    branch_address = models.TextField()

    # ================
    # Status Information
    # ================
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # ================
    # Timestamps
    # ================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Company Address"
        verbose_name_plural = "Company Addresses"
        db_table = "company_addresses"

    def __str__(self):
        return self.branch_name