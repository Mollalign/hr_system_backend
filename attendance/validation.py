# ===============================================================
# VALIDATION FOR ATTENDANCE
# ===============================================================
from .schemas import AttendanceCheckInIn, AttendanceCheckOutIn
from hr_system import Attendance
from employees.models import Employee
from ninja.errors import ValidationError
from datetime import datetime, date, time
import uuid

def validate_attendance_check_in(data: dict, db_name: str) -> str:
    """
    Validate attendance check-in data.

    Args:
        data: Check-in data with keys: 'employee_id', 'check_in_time'.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    errors = {}

    # Validate employee exists
    try:
        employee = Employee.objects.using(db_name).get(id=data['employee_id'], is_deleted=False)
    except Employee.DoesNotExist:
        return "Employee not found or deleted"

    # Validate check-in time
    if not isinstance(data['check_in_time'], (time, str)):
        return "Check-in time must be a valid time"

    # Check if already checked in today
    today = date.today()
    existing_checkin = Attendance.objects.using(db_name).filter(
        employee_id=data['employee_id'],
        attendance_date=today,
        check_in_time__isnull=False
    ).first()

    if existing_checkin:
        return "Employee has already checked in today"

    return ""

def validate_attendance_check_out(data: dict, db_name: str) -> str:
    """
    Validate attendance check-out data.

    Args:
        data: Check-out data with keys: 'employee_id', 'attendance_date', 'check_out_time'.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    errors = {}

    # Validate employee exists
    try:
        employee = Employee.objects.using(db_name).get(id=data['employee_id'], is_deleted=False)
    except Employee.DoesNotExist:
        return "Employee not found or deleted"

    # Validate check-out time
    if not isinstance(data['check_out_time'], (time, str)):
        return "Check-out time must be a valid time"

    # Check if already checked out today
    attendance_date = data.get('attendance_date', date.today())
    existing_attendance = Attendance.objects.using(db_name).filter(
        employee_id=data['employee_id'],
        attendance_date=attendance_date
    ).first()

    if not existing_attendance:
        return "No check-in record found for today"

    if existing_attendance.check_out_time:
        return "Employee has already checked out today"

    # Validate check-out time is after check-in time
    if existing_attendance.check_in_time and data['check_out_time']:
        if isinstance(data['check_out_time'], str):
            check_out_time = datetime.strptime(data['check_out_time'], '%H:%M:%S').time()
        else:
            check_out_time = data['check_out_time']
        
        if check_out_time <= existing_attendance.check_in_time:
            return "Check-out time must be after check-in time"

    return ""

def validate_attendance_data(data: list[dict], db_name: str) -> str:
    """
    Validate attendance data for bulk operations.

    Args:
        data: List of attendance data.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    errors = {}
    validated_items = []

    for index, item in enumerate(data):
        try:
            # Validate required fields
            if 'employee_id' not in item:
                errors[f"{index}.employee_id"] = "Employee ID is required"
                continue

            if 'attendance_date' not in item:
                errors[f"{index}.attendance_date"] = "Attendance date is required"
                continue

            # Validate employee exists
            try:
                employee = Employee.objects.using(db_name).get(id=item['employee_id'], is_deleted=False)
            except Employee.DoesNotExist:
                errors[f"{index}.employee_id"] = "Employee not found or deleted"
                continue

            # Validate attendance date
            if isinstance(item['attendance_date'], str):
                try:
                    attendance_date = datetime.strptime(item['attendance_date'], '%Y-%m-%d').date()
                except ValueError:
                    errors[f"{index}.attendance_date"] = "Invalid date format. Use YYYY-MM-DD"
                    continue
            else:
                attendance_date = item['attendance_date']

            # Check for duplicate attendance record
            existing_attendance = Attendance.objects.using(db_name).filter(
                employee_id=item['employee_id'],
                attendance_date=attendance_date
            ).first()

            if existing_attendance:
                errors[f"{index}.duplicate"] = "Attendance record already exists for this employee and date"
                continue

            # Validate check-in time if provided
            if 'check_in_time' in item and item['check_in_time']:
                if not isinstance(item['check_in_time'], (time, str)):
                    errors[f"{index}.check_in_time"] = "Check-in time must be a valid time"

            # Validate check-out time if provided
            if 'check_out_time' in item and item['check_out_time']:
                if not isinstance(item['check_out_time'], (time, str)):
                    errors[f"{index}.check_out_time"] = "Check-out time must be a valid time"

                # If both check-in and check-out times are provided, validate order
                if 'check_in_time' in item and item['check_in_time'] and item['check_out_time']:
                    check_in_time = item['check_in_time']
                    check_out_time = item['check_out_time']
                    
                    if isinstance(check_in_time, str):
                        check_in_time = datetime.strptime(check_in_time, '%H:%M:%S').time()
                    if isinstance(check_out_time, str):
                        check_out_time = datetime.strptime(check_out_time, '%H:%M:%S').time()
                    
                    if check_out_time <= check_in_time:
                        errors[f"{index}.time_order"] = "Check-out time must be after check-in time"

            validated_items.append(item)

        except Exception as e:
            errors[f"error_at_index_{index}"] = str(e)

    if errors:
        return f"Validation errors: {errors}"

    return ""

def validate_attendance_update(data: dict, attendance_id: uuid.UUID, db_name: str) -> str:
    """
    Validate attendance update data.

    Args:
        data: Update data.
        attendance_id: Attendance ID to update.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Check if attendance record exists
    try:
        attendance = Attendance.objects.using(db_name).get(id=attendance_id)
    except Attendance.DoesNotExist:
        return "Attendance record not found"

    # Validate employee if provided
    if 'employee_id' in data:
        try:
            employee = Employee.objects.using(db_name).get(id=data['employee_id'], is_deleted=False)
        except Employee.DoesNotExist:
            return "Employee not found or deleted"

    # Validate time order if both times are provided
    if 'check_in_time' in data and 'check_out_time' in data:
        if data['check_in_time'] and data['check_out_time']:
            check_in_time = data['check_in_time']
            check_out_time = data['check_out_time']
            
            if isinstance(check_in_time, str):
                check_in_time = datetime.strptime(check_in_time, '%H:%M:%S').time()
            if isinstance(check_out_time, str):
                check_out_time = datetime.strptime(check_out_time, '%H:%M:%S').time()
            
            if check_out_time <= check_in_time:
                return "Check-out time must be after check-in time"

    return ""
