# ===============================================================
# VALIDATION FOR PAYROLL
# ===============================================================
from schemas import CreatePayrollSchema
from .models import Payroll
from employees.models import Employee
from ninja.errors import ValidationError
from datetime import datetime, date
import uuid

def validate_payroll_creation(data: dict) -> str:
    """
    Validate payroll creation data.

    Args:
        data: Payroll data with keys: 'payment_date'.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Validate required fields
    if not data.get('payment_date'):
        return "Payment date is required"

    # Validate payment date format
    if isinstance(data['payment_date'], str):
        try:
            payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
        except ValueError:
            return "Invalid payment date format. Use YYYY-MM-DD"
    else:
        payment_date = data['payment_date']

    # Validate payment date is not in the future
    today = date.today()
    if payment_date > today:
        return "Payment date cannot be in the future"

    # Validate payment date is not too far in the past (more than 1 year)
    from datetime import timedelta
    one_year_ago = today - timedelta(days=365)
    if payment_date < one_year_ago:
        return "Payment date cannot be more than 1 year in the past"

    return ""

def validate_payroll_bulk_creation(data: list[dict]) -> str:
    """
    Validate bulk payroll creation data.

    Args:
        data: List of payroll data.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    errors = {}
    validated_items = []

    for index, item in enumerate(data):
        try:
            # Validate schema types
            valid_data = CreatePayrollSchema(**item)
            
            # Business rules validation
            error_message = validate_payroll_creation(item)
            if error_message:
                errors[f"index_{index}"] = error_message
                continue

            validated_items.append(valid_data)

        except Exception as e:
            errors[f"error_at_index_{index}"] = str(e)

    if errors:
        return f"Validation errors: {errors}"

    return ""

def validate_payroll_update(payroll_id: uuid.UUID, data: dict) -> str:
    """
    Validate payroll update data.

    Args:
        payroll_id: Payroll ID.
        data: Update data.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Check if payroll exists
    try:
        payroll = Payroll.objects.get(id=payroll_id)
    except Payroll.DoesNotExist:
        return "Payroll record not found"

    # Validate payment date if provided
    if 'payment_date' in data:
        if isinstance(data['payment_date'], str):
            try:
                payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
            except ValueError:
                return "Invalid payment date format. Use YYYY-MM-DD"
        else:
            payment_date = data['payment_date']

        # Validate payment date is not in the future
        today = date.today()
        if payment_date > today:
            return "Payment date cannot be in the future"

    return ""

def validate_payroll_deletion(payroll_id: uuid.UUID) -> str:
    """
    Validate payroll deletion.

    Args:
        payroll_id: Payroll ID.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Check if payroll exists
    try:
        payroll = Payroll.objects.get(id=payroll_id)
    except Payroll.DoesNotExist:
        return "Payroll record not found"

    # Check if payroll is already processed (cannot delete processed payrolls)
    if hasattr(payroll, 'is_processed') and payroll.is_processed:
        return "Cannot delete processed payroll record"

    return ""

def validate_payroll_employee_data(employee_id: uuid.UUID) -> str:
    """
    Validate employee data for payroll generation.

    Args:
        employee_id: Employee ID.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Check if employee exists and is active
    try:
        employee = Employee.objects.get(id=employee_id, is_active=True, is_deleted=False)
    except Employee.DoesNotExist:
        return "Employee not found or inactive"

    # Check if employee has basic salary
    if not employee.basic_salary or employee.basic_salary <= 0:
        return "Employee must have a valid basic salary"

    # Check if employee has valid department
    if not employee.department:
        return "Employee must be assigned to a department"

    return ""

def validate_payroll_calculation_data(employee_id: uuid.UUID, payroll_data: dict) -> str:
    """
    Validate payroll calculation data.

    Args:
        employee_id: Employee ID.
        payroll_data: Payroll calculation data.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Validate basic salary
    if 'basic_salary' in payroll_data:
        if payroll_data['basic_salary'] <= 0:
            return "Basic salary must be greater than 0"

    # Validate allowances
    if 'allowance' in payroll_data:
        allowance_data = payroll_data['allowance']
        if isinstance(allowance_data, dict):
            for key, value in allowance_data.items():
                if not isinstance(value, (int, float)) or value < 0:
                    return f"Allowance {key} must be a non-negative number"

    # Validate deductions
    if 'deduction' in payroll_data:
        deduction_data = payroll_data['deduction']
        if isinstance(deduction_data, dict):
            for key, value in deduction_data.items():
                if not isinstance(value, (int, float)) or value < 0:
                    return f"Deduction {key} must be a non-negative number"

    # Validate net salary calculation
    if 'net_salary' in payroll_data:
        net_salary = payroll_data['net_salary']
        if not isinstance(net_salary, (int, float)) or net_salary < 0:
            return "Net salary must be a non-negative number"

    return ""

def validate_payroll_period(payment_date: date) -> str:
    """
    Validate payroll period.

    Args:
        payment_date: Payment date.
        db_name: Database alias.

    Returns:
        str: Empty if valid, error message if invalid.
    """
    # Check if payroll already exists for this period
    existing_payroll = Payroll.objects.filter(payment_date=payment_date).exists()
    if existing_payroll:
        return f"Payroll already exists for {payment_date}"

    return ""
