# ===============================================================
# ATTENDANCE SERIALIZER
# ===============================================================
from .models import Attendance
from .schemas import AttendanceDataSchema, EmployeeSchema
from employees.models import Employee
from typing import List


# ===============================
    # SERIALIZER FOR EMPLOYEE
# ===============================
def serialize_employee(employee: Employee):
    return EmployeeSchema(
        id=employee.id,
        full_name=employee.full_name,
        work_location=employee.work_location.branch_name,
    )

# ===============================
# SERIALIZER FOR ATTENDANCE
# ===============================
def serialize_attendance(attendance: Attendance):
    return AttendanceDataSchema(
        id=attendance.id,
        employee=serialize_employee(attendance.employee_id),
        attendance_date=attendance.attendance_date,
        check_in_time=attendance.check_in_time,
        check_out_time=attendance.check_out_time,
        status=attendance.status,
    )

# ===============================
# HELPER SERIALIZER FOR ATTENDANCE
# ===============================
# serialize single attendance
def serialize_attendance_single(attendance: Attendance):
    return serialize_attendance(attendance).model_dump()

# serialize list of attendances
def serialize_attendance_list(attendances: List[Attendance]):
    return [serialize_attendance(attendance) for attendance in attendances]