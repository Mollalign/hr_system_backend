import uuid
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link Employee to User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )

    # Personal Info
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default="male")
    date_of_birth = models.DateField()
    maternal_status = models.CharField(max_length=10, choices=[('single', 'Single'), ('married', 'Married')], default="single")
    nationality = models.CharField(max_length=255)

    # Contact Info
    phone_number = PhoneNumberField(unique=True)
    alternative_phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    # Job Info
    employee_code = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, null=True, blank=True, related_name="employees")
    hire_date = models.DateField()
    employee_type = models.CharField(max_length=20, choices=[('permanent','Permanent'),('contract','Contract')], default="permanent")

    # Salary Info
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)

    # Documents
    cv_file = models.FileField(upload_to='cv_files/', null=True, blank=True, verbose_name="CV File", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'ods', 'odp', 'odg', 'odf', 'odc', 'odm', 'odt', 'odp', 'ods', 'odg', 'odf', 'odc', 'odm'])])

    # Status
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employees"

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"
