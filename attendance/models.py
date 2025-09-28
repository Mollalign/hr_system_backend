# ===============================================================
# ATTENDANCE MODEL
# ===============================================================
# import the necessary modules
from django.db import models
import uuid

# ===============================
# ATTENDANCE MODEL
# ===============================
class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    employee_id = models.ForeignKey('employees.Employee', on_delete=models.PROTECT, verbose_name="Employee", null=False, blank=False, related_name="attendances")

    # Attendance Information
    check_in_time = models.TimeField(null=True, blank=True,verbose_name="Check In Time")
    check_out_time = models.TimeField(null=True, blank=True,verbose_name="Check Out Time")
    attendance_date = models.DateField(verbose_name="Attendance Date",null=False,blank=False)

    # Status Information
    status = models.JSONField(default=dict, verbose_name="Attendance Status",null=False,blank=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        db_table = "attendances"

    def __str__(self):
        return f"{self.employee_id.full_name} - {self.attendance_date}"
