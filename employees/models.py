import uuid
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

# ===============================
# ENUM-LIKE CHOICES
# ===============================
# Gender Choices
Gender = [
    ('male', 'Male'),
    ('female', 'Female')
]

# Maternal Status Choices
MaternalStatus = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed')
]

# Employee Type Choices
EmploymentType = [
    ('permanent', 'Permanent'),
    ('contract', 'Contract'),
    ('temporary', 'Temporary'),
    ('intern', 'Intern'),
    ('freelance', 'Freelance'),
    ('other', 'Other')
]

# Employment Type Choices
Employment_shift = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
]

# Employment Status Choices
EmploymentStatus = [
    # Leave Status
    ('on_leave', 'On Leave'),
    ('on_duty', 'On Duty'),
    ('on_work', 'On Work'),
    ('on_vacation', 'On Vacation'),
    ('on_sick_leave', 'On Sick Leave'),
    ('on_other_leave', 'On Other Leave'),
    ('on_maternity_leave', 'On Maternity Leave'),
    ('on_paternity_leave', 'On Paternity Leave'),
    ('on_compassionate_leave', 'On Compassionate Leave'),
    ('on_military_leave', 'On Military Leave'),
    ('on_religious_leave', 'On Religious Leave'),

    # Employment Status
    ('fired', 'Fired'),
    ('resigned', 'Resigned'),
    ('transferred', 'Transferred'),
    ('promoted', 'Promoted'),
    ('demoted', 'Demoted'),
    ('suspended', 'Suspended'),
    ('terminated', 'Terminated'),

    # Other Status
    ('other', 'Other'),
]

# Contact Person Relationship Choices
ContactPersonRelationship = [
    ('spouse', 'Spouse'),
    ('child', 'Child'),
    ('sibling', 'Sibling'),
    ('friend', 'Friend'),
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('guardian', 'Guardian'),
    ('grandchild', 'Grandchild'),
    ('grandparent', 'Grandparent'),
    ('other', 'Other'),
]

# ===============================
# EMPLOYEE MODEL
# ===============================
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Personal Info
    full_name = models.CharField(max_length=255, verbose_name="Full Name", null=False, blank=False, default="")
    gender = models.CharField(max_length=10, choices=Gender, verbose_name="Gender", null=False, blank=False, default="male")
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=False, blank=False)
    maternal_status = models.CharField(max_length=10, choices=MaternalStatus, verbose_name="Maternal Status", null=False, blank=False, default="single")
    nationality = models.CharField(max_length=255, verbose_name="Nationality", null=False, blank=False, default="")

    # contact info
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email", null=False, blank=False)
    phone_number = PhoneNumberField(unique=True, verbose_name="Phone Number", null=False, blank=False)
    alternative_phone_number = PhoneNumberField(unique=False, verbose_name="Alternative Phone Number", null=True, blank=True)

    # address info
    permanent_address = models.CharField(max_length=255, verbose_name="Permanent Address", null=False, blank=False, default="")
    current_address = models.CharField(max_length=255, verbose_name="Current Address", null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name="City", null=False, blank=False, default="")
    state = models.CharField(max_length=255, verbose_name="State", null=False, blank=False, default="")
    country = models.CharField(max_length=255, verbose_name="Country", null=False, blank=False, default="")
    zip_code = models.CharField(max_length=255, verbose_name="Zip Code", null=False, blank=False, default="")

    # emergency contact info
    contact_person_name = models.CharField(max_length=255, verbose_name="Contact Person Name", null=False, blank=False, default="")
    contact_person_relationship = models.CharField(max_length=255, choices=ContactPersonRelationship, verbose_name="Contact Person Relationship", null=False, blank=False, default="other")
    contact_person_phone = PhoneNumberField(unique=False, verbose_name="Contact Person Phone", null=True, blank=True)
    contact_person_alternative_phone = PhoneNumberField(unique=False, verbose_name="Contact Person Alternative Phone", null=True, blank=True)
    contact_person_address = models.CharField(max_length=255, verbose_name="Contact Person Address", null=True, blank=True)

    # Job Info
    employee_code = models.CharField(max_length=255, verbose_name="Employee Code", null=False, blank=False, default="")
    job_title = models.CharField(max_length=255, verbose_name="Job Title", null=False, blank=False, default="") #position/Designation
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, related_name="employees_department", verbose_name="Department", null=True, blank=True)
    hire_date = models.DateField(verbose_name="Hire Date", null=False, blank=False) #date of joining
    employee_type = models.CharField(max_length=20, choices=EmploymentType, verbose_name="Employee Type", null=False, blank=False, default="permanent")
    employment_shift = models.CharField(max_length=20, choices=Employment_shift, verbose_name="Employment Status", null=False, blank=False, default="full_time")
    employment_status = models.CharField(max_length=25, choices=EmploymentStatus, verbose_name="Employment Status", null=False, blank=False, default="on_duty")
    work_location = models.ForeignKey('company_address.CompanyAddress', on_delete=models.CASCADE, related_name="employees_location", verbose_name="Work Location", null=True, blank=True)
    
    # Bank Info
    bank_account_number = models.CharField(max_length=255, verbose_name="Bank Account Number", null=False, blank=False, default="")

    # Salary Info
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Basic Salary", null=False, blank=False, default=0.00)
    allowance = models.JSONField(default=list, verbose_name="Allowance", null=False, blank=False )
    deduction = models.JSONField(default=list, verbose_name="Deduction", null=False, blank=False )
    effective_date = models.DateField(verbose_name="Effective Date", null=False, blank=False)

    # Currency Info
    currency_of_salary = models.CharField(max_length=5, verbose_name="Currency of Salary", null=False, blank=False, default="ETB")

    # Documents
    cv_file = models.FileField(
        upload_to='cv_files/',
        null=True,
        blank=True,
        verbose_name="CV File",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
            )
        ]
    )
    
    # Status Information
    is_active = models.BooleanField(default=True, verbose_name="Status", null=False, blank=False)  # active/inactive
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employees"

   
    def __str__(self):
         return f"{self.full_name} - {self.job_title}"