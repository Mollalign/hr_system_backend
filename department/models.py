from django.db import models
import uuid

# ===============================
# DEPARTMENT MODEL
# ===============================
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   
    # ================
    # Basic Information
    # ================
    dep_name = models.CharField(max_length=255, verbose_name="Department Name", null=False, blank=False)
   
    # ================
    # Manager Information
    # ================
    manager = models.ForeignKey('employees.Employee', on_delete=models.PROTECT, verbose_name="Manager", null=True, blank=True, related_name="departments_managed")
   
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
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = "departments"

    def __str__(self):
        return self.dep_name