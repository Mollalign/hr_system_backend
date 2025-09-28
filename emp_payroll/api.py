# ===============================================================
# PAYROLL API
# ===============================================================
# import the necessary modules
from ninja import Router

# ===============================
# MODELS
# ===============================
from .models import Payroll
from employees.models import Employee

# ===============================
# SCHEMAS
# ===============================
from .schemas import PayrollResponseSchema, CreatePayrollSchema, PayrollSingleResponseSchema

# ===============================
# SERIALIZERS
# ===============================
from .serializer import serialize_payroll_list, serialize_payroll_single

# ===============================
# UTILTIS
# ===============================
from utility.payroll import get_deductions, get_allowances

# ===============================
# ROUTERS
# ===============================
payroll_router = Router()

# ===============================
# PAYROLL API ENDPOINTS
# ===============================
# =====================================================================
# Endpoint: Get All Payrolls
# ---------------------------------------------------------------------
# This API endpoint retrieves all payroll records from the database 
# that have not been marked as deleted (i.e., is_deleted=False). 
# It uses the Payroll model to query the database.
# The endpoint is registered at the '/' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns a list of all payrolls with their details; 
# on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a complete overview of all current payrolls is required.
# =====================================================================
@payroll_router.get(
    "/", 
    response=PayrollResponseSchema, 
    description="Get all payrolls. Returns a list of all payrolls with their details. Useful for administrative overviews and management dashboards.",
    summary="Get all payrolls",
)
def get_payroll(request):
    """
    Get all payrolls.

    Args:
        request: The request object.

    Returns:
        The response object.
    """
    try:
        payrolls = Payroll.objects.select_related('employee_id').all()
        print(payrolls)
        result = serialize_payroll_list(payrolls)
        return PayrollResponseSchema(status=True, status_code=200, message="Fetch Payrolls", data=result)
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=404, message=str(e), data=[])
    
# =====================================================================
# Endpoint: Get Payroll by Employee ID
# ---------------------------------------------------------------------
# This API endpoint retrieves all payroll records from the database 
# that have not been marked as deleted (i.e., is_deleted=False) and 
# are associated with the specified employee ID. It uses the Payroll model to query the database.
# The endpoint is registered at the '/employee/{employee_id}' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns a list of all payrolls with their details; 
# on failure, it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a complete overview of all current payrolls for a specific employee is required.
# =====================================================================
@payroll_router.get(
    "/employee/{employee_id}", 
    response=PayrollResponseSchema, 
    description="Get a payroll by employee id. Returns a list of all payrolls with their details. Useful for administrative overviews and management dashboards.",
    summary="Get a payroll by employee id",
)
def get_payroll_by_employee_id(request, employee_id: str):
    """
    Get a payroll by employee id.

    Args:
        request: The request object.
        employee_id: The id of the employee.

    Returns:
        The response object.
    """
    try:
        employee = Employee.objects.get(id=employee_id)
        payrolls = Payroll.objects.filter(employee_id=employee)
        result = serialize_payroll_list(payrolls)
        return PayrollResponseSchema(status=True, status_code=200, message="Fetch Payrolls", data=result)
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=404, message=str(e), data=[])

# =====================================================================
# Endpoint: Get Payroll by ID
# ---------------------------------------------------------------------
# This API endpoint retrieves a specific payroll record from the 
# database based on the provided ID. It uses the Payroll model to 
# query the database.
# The endpoint is registered at the '/{id}' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns the payroll with its details; on failure, 
# it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a specific payroll's details are required.
# =====================================================================
@payroll_router.get(
    "/{id}", 
    response=PayrollSingleResponseSchema, 
    description="Get a payroll by id. Returns the payroll with its details. Useful for administrative overviews and management dashboards.",
    summary="Get a payroll by id",
)
def get_payroll_by_id(request, id: str):
    """
    Get a payroll by id.

    Args:
        request: The request object.
        id: The id of the payroll.

    Returns:
        The response object.
    """
    try:
        payroll = Payroll.objects.get(id=id)
        result = serialize_payroll_single(payroll)
        return PayrollSingleResponseSchema(status=True, status_code=200, message="Fetch Payroll", data=result)
    except Exception as e:
        return PayrollSingleResponseSchema(status=False, status_code=404, message=str(e), data=[])

# =====================================================================
# Endpoint: Get Payroll by ID and Employee ID
# ---------------------------------------------------------------------
# This API endpoint retrieves a specific payroll record from the 
# database based on the provided ID and employee ID. It uses the Payroll model to query the database.
# The endpoint is registered at the '/{id}/{employee_id}' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns the payroll with its details; on failure, 
# it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a specific payroll's details are required.
# =====================================================================
@payroll_router.get(
    "/{id}/{employee_id}", 
    response=PayrollResponseSchema, 
    description="Get a payroll by id and employee id. Returns the payroll with its details. Useful for administrative overviews and management dashboards.",
    summary="Get a payroll by id and employee id",
)
def get_payroll_by_id_and_employee_id(request, id: str, employee_id: str):
    """
    Get a payroll by id and employee id.

    Args:
        request: The request object.
        id: The id of the payroll.
        employee_id: The id of the employee.

    Returns:
        The response object.
    """
    try:
        payroll = Payroll.objects.get(id=id, employee_id=employee_id)
        result = serialize_payroll_single(payroll)
        return PayrollResponseSchema(status=True, status_code=200, message="Fetch Payroll", data=result)
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=404, message=str(e), data=[])

# =====================================================================
# Endpoint: Get All Payrolls by Employee ID
# ---------------------------------------------------------------------
# This API endpoint retrieves all payroll records from the database 
# that have not been marked as deleted (i.e., is_deleted=False) and 
# are associated with the specified employee ID. It uses the Payroll model to query the database.
# The endpoint is registered at the '/' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns a list of all payrolls with their details; on failure, 
# it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a complete overview of all current payrolls for a specific employee is required.
# =====================================================================
@payroll_router.get(
    "/employee/{employee_id}", 
    response=PayrollResponseSchema, 
    description="Get all payrolls by employee id. Returns a list of all payrolls with their details. Useful for administrative overviews and management dashboards.",
    summary="Get all payrolls by employee id",
)
def get_all_payrolls_by_employee_id(request, employee_id: str):
    """
    Get all payrolls by employee id.

    Args:
        request: The request object.
        employee_id: The id of the employee.

    Returns:
        The response object.
    """
    try:
        employee = Employee.objects.get(id=employee_id)
        payrolls = Payroll.objects.filter(employee_id=employee)
        result = serialize_payroll_list(payrolls)
        return PayrollResponseSchema(status=True, status_code=200, message="Fetch Payrolls", data=result)
    except Employee.DoesNotExist:
        return PayrollResponseSchema(status=False, status_code=404, message="Employee not found", data=[])
    except Payroll.DoesNotExist:
        return PayrollResponseSchema(status=False, status_code=404, message="Payroll not found", data=[])
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=404, message=str(e), data=[])

# =====================================================================
# Endpoint: Create Payroll for All Active Employees
# ---------------------------------------------------------------------
# This API endpoint creates a new payroll record for all active employees for a given month. It uses the Payroll model to create the new record.
# The endpoint is registered at the '/' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns the created payroll with its details; on failure, 
# it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a new payroll can be created for all active employees for a given month.
# =====================================================================
@payroll_router.post(
    "/", 
    response=PayrollResponseSchema, 
    description="Create a new payroll for all active employees for a given month. Returns the created payroll with its details. Useful for administrative overviews and management dashboards.",
    summary="Create a new payroll for all active employees for a given month",
)
def create_payroll(request, payroll: CreatePayrollSchema):
    """
    Create a new payroll for all active employees for a given month.

    Args:
        request: The request object.
        payroll: The payroll data.

    Returns:
        The response object.
    """
    try:
        employees = Employee.objects.filter(is_deleted=False, is_active=True)
        payroll_list = []
        for employee in employees:
            all_allowance = get_allowances(employee.allowance, employee.basic_salary)
            all_deduction = get_deductions(employee.deduction, employee.basic_salary)
            payroll = Payroll.objects.create(
                employee_id=employee,
                basic_salary=employee.basic_salary,
                allowance=all_allowance,
                deduction=all_deduction,
                payment_date=payroll.payment_date
            )
            result = serialize_payroll_single(payroll)
            payroll_list.append(result)
        return PayrollResponseSchema(status=True, status_code=200, message="Payroll created successfully", data=payroll_list)
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=404, message=str(e), data=[])
    
# =====================================================================
# Endpoint: Create Payroll by Employee ID
# ---------------------------------------------------------------------
# This API endpoint creates a new payroll record for a specific employee for a given month. It uses the Payroll model to create the new record.
# The endpoint is registered at the '/employee/{employee_id}' path of the payroll 
# router and returns a response conforming to the PayrollResponseSchema.
# On success, it returns the created payroll with its details; on failure, 
# it returns an error message and an empty data list.
# This endpoint is useful for administrative interfaces or dashboards 
# where a new payroll can be created for a specific employee for a given month.
# =====================================================================
@payroll_router.post("/employee/{employee_id}", response=PayrollResponseSchema, 
    description="Create a payroll by employee id. Returns the created payroll with its details. Useful for administrative overviews and management dashboards.",
    summary="Create a payroll by employee id",
)
def create_payroll_by_employee_id(request, employee_id: str, payload: CreatePayrollSchema):
    """
    Create a payroll by employee id.

    Args:
        request: The request object.
        employee_id: The id of the employee.
        payload: The payroll data.

    Returns:
        The response object.
    """
    try:
        employee = Employee.objects.get(id=employee_id, is_deleted=False, is_active=True)
        all_deduction = get_deductions(employee.deduction, employee.basic_salary)
        all_allowance = get_allowances(employee.allowance, employee.basic_salary)
        
        # ===============================
        # CREATE PAYROLL
        # ===============================
        payroll = Payroll.objects.create(
            employee_id=employee,
            basic_salary=employee.basic_salary,
            allowance=all_allowance,
            deduction=all_deduction,
            payment_date=payload.payment_date
        )
        result = serialize_payroll_single(payroll)
        return PayrollResponseSchema(status=True, status_code=200, message="Payroll created successfully", data=[])
    except Employee.DoesNotExist:
        return PayrollResponseSchema(status=False, status_code=404, message="Employee not found", data=[])
    except Exception as e:
        return PayrollResponseSchema(status=False, status_code=500, message=str(e), data=[])
  