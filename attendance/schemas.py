# ===============================================================
# ATTENDANCE SCHEMA
# ===============================================================
from ninja import Schema, Field
from typing import List, Optional
import uuid
from datetime import datetime, date, time

# ========================
# EMPLOYEE SCHEMA
# ========================
class EmployeeSchema(Schema):
    id: uuid.UUID
    full_name: str
    work_location: str

# ===============================
# ATTENDANCE STATUS
# ===============================
status = {
    # check-in status
    "late_in": False,
    "on_time_in": False,

    # check-out status
    "early_out": False,
    "on_time_out": False,

    # other status
    "missing_checkout": False,
    "present": False,
    "absent": False,
    "leave": False,
    "holiday": False,
    "permission": False,
    "overtime": False,
    "other": False
}

# ===============================
# ATTENDANCE SCHEMA
# ===============================
# check in schema
class AttendanceCheckInIn(Schema):
    employee_id: uuid.UUID
    check_in_time: time = Field(..., description="Check-in timestamp")
   
# check out schema
class AttendanceCheckOutIn(Schema):
    employee_id: uuid.UUID
    attendance_date: date | None
    check_out_time: time = Field(..., description="Check-out timestamp")

# attendance data schema
class AttendanceDataSchema(Schema):
    id: uuid.UUID
    employee: EmployeeSchema
    attendance_date: date
    check_in_time: time
    check_out_time: time | None
    status: dict

# attendance response schema
class AttendanceResponse(Schema):
    status_code: int
    success: bool
    message: str
    data: List[AttendanceDataSchema]

