# ===============================================================
# PAYROLL SCHEMA
# ===============================================================
# import the necessary modules
from ninja import Schema, Field

import uuid
from datetime import datetime

# ===============================
# Employee SCHEMA
# ===============================
class EmployeeSchema(Schema):
    id: uuid.UUID = Field(..., description="The full name of the employee")
    full_name: str = Field(..., description="The full name of the employee")

# ===============================
# Department SCHEMA
# ===============================
class DepartmentSchema(Schema):
    id: uuid.UUID = Field(..., description="The full name of the employee")
    name: str = Field(..., description="The name of the department")
    manager_name: str = Field(..., description="The manager name of the department")

# ===============================
# PAYROLL SCHEMA
# ===============================
# create and update payroll
class CreatePayrollSchema(Schema):
    payment_date: datetime = Field(..., description="The payment date of the payroll")

# payroll schema
class PayrollSchema(Schema):
    id: uuid.UUID = Field(..., description="The id of the payroll")
    employee_id: EmployeeSchema = Field(..., description="The employee of the payroll")
    basic_salary: float = Field(..., description="The basic salary of the payroll")
    department: DepartmentSchema = Field(..., description="The department of the payroll")
    allowance: dict = Field(..., description="The allowance of the payroll")
    deduction: dict = Field(..., description="The deduction of the payroll")
    payment_date: datetime = Field(..., description="The payment date of the payroll")

# payroll response schema
class PayrollResponseSchema(Schema):
    status: bool = Field(..., description="The status of the response")
    status_code: int = Field(..., description="The status code of the response")
    message: str = Field(..., description="The message of the response")
    data: list[PayrollSchema] = Field(..., description="The data of the response")

# single payroll response schema
class PayrollSingleResponseSchema(Schema):
    status: bool = Field(..., description="The status of the response")
    status_code: int = Field(..., description="The status code of the response")
    message: str = Field(..., description="The message of the response")
    data: PayrollSchema = Field(..., description="The single payroll data")  # Single object, not list