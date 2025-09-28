# ===============================================================
# ATTENDANCE API
# ===============================================================
# import the necessary modules
from datetime import datetime
import uuid
from ninja import Router

# ===============================
# MODELS
# ===============================
from .models import Attendance
from employees.models import Employee

# ===============================
# SCHEMAS
# ===============================
from .schemas import AttendanceResponse, AttendanceCheckInIn, AttendanceCheckOutIn, status

# ===============================
# SERIALIZERS
# ===============================
from .serializer import serialize_attendance_list, serialize_attendance_single

# ===============================
# UTILS
# ===============================
from utility.attendance import check_in_status, check_out_status

# ====================
# ROUTER
# ====================
attendance_router = Router(tags=["Attendance"])

# ====================
# ATTENDANCE ENDPOINT
# ====================
# =====================================================================
# Endpoint: Get All Attendance
# ---------------------------------------------------------------------
# This API endpoint retrieves all attendance records from the database 
# that have not been marked as deleted (i.e., is_deleted=False). 
# It uses the Attendance model to query the database.
# It uses the serialize_attendance_list function to serialize the attendance records.
# The endpoint is registered at the '/' path of the attendance router and returns a response conforming to the AttendanceResponseSchema.
# On success, it returns a list of all attendance records with their details; on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a complete overview of all current attendance records is required.
# =====================================================================
@attendance_router.get(
    "/",
    response=AttendanceResponse,
    description="Get all attendance records",
    url_name="list_attendance"
)
def list_attendance(request):
    """
    Get all attendance records.

    Args:
        request: The request object.

    Returns:
        The response object.
    """
    try:
        attendance = Attendance.objects.select_related("employee_id").all()
        data = serialize_attendance_list(attendance)
        return AttendanceResponse(status_code=200, success=True, message="Attendance records fetched", data=data)
    except Exception as e:
        return AttendanceResponse(status_code=500, success=False, message=str(e), data=[])

# =====================================================================
# Endpoint: Get Attendance by ID
# ---------------------------------------------------------------------
# This API endpoint retrieves a single attendance record from the database 
# by its ID. It uses the Attendance model to query the database.
# The endpoint is registered at the '/{attendance_id}' path of the attendance router and returns a response conforming to the AttendanceResponseSchema.
# On success, it returns the attendance record with its details; on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a single attendance record can be retrieved by its ID.
# =====================================================================
@attendance_router.get(
    "/{attendance_id}", 
    response=AttendanceResponse, 
    description="Get attendance record by ID",
    summary="Get attendance record by ID",
)
def get_attendance(request, attendance_id: uuid.UUID):
    """
    Get attendance record by ID.

    Args:
        request: The request object.
        attendance_id: The ID of the attendance record.

    Returns:
        The response object.
    """
    try:
        attendance = Attendance.objects.select_related("employee_id").get(id=attendance_id)
        data = serialize_attendance_single(attendance)
        return AttendanceResponse(status_code=200, success=True, message="Attendance record fetched", data=[data])
    except Attendance.DoesNotExist:
        return AttendanceResponse(status_code=404, success=False, message="Attendance record not found", data=[])
    except Exception as e:
        return AttendanceResponse(status_code=500, success=False, message=str(e), data=[])

# =====================================================================
# Endpoint: Create Attendance
# ---------------------------------------------------------------------
# This API endpoint creates a new attendance record in the database. 
# It uses the Attendance model to create the record.
# The endpoint is registered at the '/' path of the attendance router and returns a response conforming to the AttendanceResponseSchema.
# On success, it returns the attendance record with its details; on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a new attendance record can be created.
# =====================================================================
@attendance_router.post(
    "/", 
    response=AttendanceResponse, 
    description="Create a new attendance record",
    summary="Create a new attendance record",
)
def create_attendance(request, payload: AttendanceCheckInIn):
    """
    Create a new attendance record.

    Args:
        request: The request object.
        payload: The payload object.

    Returns:
        The response object.
    """
    try:
        today = datetime.now().date()
        employee = Employee.objects.get(id=payload.employee_id)
        is_exists = Attendance.objects.filter(employee_id=employee, attendance_date=today).exists()
        if is_exists:
            return AttendanceResponse(status_code=400, success=False, message="Attendance record already exists", data=[])
        status.update(check_in_status(payload.check_in_time))

        attendance = Attendance.objects.create(
            employee_id_id=payload.employee_id,
            attendance_date=today,
            check_in_time=payload.check_in_time,
            check_out_time=None,
            status=status,
        )
        data = serialize_attendance_single(attendance)
        return AttendanceResponse(status_code=200, success=True, message="Attendance record created", data=[data])
    except Employee.DoesNotExist:
        return AttendanceResponse(status_code=404, success=False, message="Employee not found", data=[])
    except Exception as e:
        return AttendanceResponse(status_code=500, success=False, message=str(e), data=[])


# =====================================================================
# Endpoint: Update Attendance
# ---------------------------------------------------------------------
# This API endpoint updates an existing attendance record in the database. 
# It uses the Attendance model to update the record.
# The endpoint is registered at the '/{attendance_id}' path of the attendance router and returns a response conforming to the AttendanceResponseSchema.
# On success, it returns the attendance record with its details; on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where an existing attendance record can be updated.
# =====================================================================
@attendance_router.put(
    "/{attendance_id}", 
    response=AttendanceResponse,
    description="Update attendance record",
    summary="Update attendance record",
)
def update_attendance(request, attendance_id: uuid.UUID, payload: AttendanceCheckOutIn):
    """
    Update attendance record.

    Args:
        request: The request object.
        attendance_id: The ID of the attendance record.
        payload: The payload object.

    Returns:
        The response object.
    """
    try:
        attendance = Attendance.objects.get(id=attendance_id, employee_id=payload.employee_id, attendance_date=payload.attendance_date)

        if attendance.check_in_time is None:
            return AttendanceResponse(status_code=400, success=False, message="Attendance record not checked in", data=[])

        if attendance.check_out_time is not None:
            return AttendanceResponse(status_code=400, success=False, message="Attendance record already checked out", data=[])

        status.update(check_out_status(payload.check_out_time))

        attendance.check_out_time = payload.check_out_time
        attendance.status = status

        attendance.save()
        data = serialize_attendance_single(attendance)
        return AttendanceResponse(status_code=200, success=True, message="Attendance record updated", data=[data])
    except Attendance.DoesNotExist:
        return AttendanceResponse(status_code=404, success=False, message="Attendance record not found", data=[])
    except ValueError as e:
        return AttendanceResponse(status_code=400, success=False, message=str(e), data=[])
    except Exception as e:
        return AttendanceResponse(status_code=500, success=False, message=str(e), data=[])

# =====================================================================
# Endpoint: Delete Attendance(hard delete)
# ---------------------------------------------------------------------
# This API endpoint deletes an existing attendance record in the database. 
# It uses the Attendance model to delete the record.
# The endpoint is registered at the '/{attendance_id}' path of the attendance router and returns a response conforming to the AttendanceResponseSchema.
# On success, it returns a success message; on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where an existing attendance record can be deleted(hard delete).
# =====================================================================
@attendance_router.delete(
    "/",
    response=AttendanceResponse,
    description="Delete attendance record. Returns a success message. Useful for administrative overviews and management dashboards.",
    summary="Delete attendance record(hard delete)",
)
def delete_attendance(request):
    """
    Delete attendance record(hard delete).

    Args:
        request: The request object.

    Returns:
        The response object.
    """
    try:
        attendance = Attendance.objects.all()
        for attendance in attendance:
            attendance.delete()
        return AttendanceResponse(status_code=200, success=True, message="Attendance record deleted", data=[])
    except Exception as e:
        return AttendanceResponse(status_code=500, success=False, message=str(e), data=[])