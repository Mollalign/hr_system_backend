# ===============================================================
# SCHEMA FOR EMPLOYEE
# ===============================================================
from ninja import Schema, Field
from typing import List, Optional
import uuid
from datetime import date
from pydantic import EmailStr
from department.schemas import DepartmentDataSchema

from decimal import Decimal

# ===============================
# SCHEMA FOR ALLOWANCE
# ===============================
class AllowanceSchema(Schema):
    name: str = Field(..., description="The name of the allowance")
    type: str = Field(..., description="The type of the allowance")
    percentage: float = Field(..., description="The percentage of the allowance")
    amount: float = Field(..., description="The amount of the allowance")
    description: str = Field(..., description="The description of the allowance")
    is_active: bool = Field(..., description="The active status of the allowance")

# ===============================
# SCHEMA FOR COMPANY ADDRESS
# ===============================
class CompanyAddressSchema(Schema):
    branch_name: str = Field(..., description="The branch name of the company address")
    branch_phone: str = Field(..., description="The branch phone of the company address")
    branch_email: str = Field(..., description="The branch email of the company address")
    branch_address: str = Field(..., description="The branch address of the company address")
    is_active: bool = Field(..., description="The active status of the company address")

# ===============================
# SCHEMA FOR DEDUCTION
# ===============================
class DeductionSchema(Schema):
    name: str = Field(..., description="The name of the deduction")
    type: str = Field(..., description="The type of the deduction")
    percentage: float = Field(..., description="The percentage of the deduction")
    amount: float = Field(..., description="The amount of the deduction")
    description: str = Field(..., description="The description of the deduction")
    is_active: bool = Field(..., description="The active status of the deduction")

# ===============================
# SCHEMA FOR EMPLOYEE
# ===============================
# create and update employee request schema
class CreateAndUpdateEmployeeRequestSchema(Schema):
    # Personal Info
    full_name: str = Field(..., description="The full name of the employee")
    gender: str = Field(..., description="The gender of the employee")
    date_of_birth: date = Field(..., description="The date of birth of the employee")
    maternal_status: str = Field(..., description="The maternal status of the employee")
    nationality: str = Field(..., description="The nationality of the employee")

    # Contact Info
    email: EmailStr = Field(..., description="The email of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    alternative_phone_number: Optional[str] = Field(None, description="The alternative phone number of the employee")

    # Address Info
    permanent_address: str = Field(..., description="The permanent address of the employee")
    current_address: Optional[str] = Field(None, description="The current address of the employee")
    city: str = Field(..., description="The city of the employee")
    state: str = Field(..., description="The state of the employee")
    country: str = Field(..., description="The country of the employee")
    zip_code: str = Field(..., description="The zip code of the employee")

    # Emergency Contact Info
    contact_person_name: str = Field(..., description="The name of the contact person")
    contact_person_relationship: str = Field(..., description="The relationship of the contact person")
    contact_person_phone: str = Field(..., description="The phone number of the contact person")
    contact_person_alternative_phone: Optional[str] = Field(None, description="The alternative phone number of the contact person")
    contact_person_address: str = Field(..., description="The address of the contact person")

    # Job Info
    employee_code: str = Field(..., description="The employee code of the employee")
    job_title: str = Field(..., description="The job title of the employee")
    department: uuid.UUID = Field(..., description="The department of the employee")
    employee_type: str = Field(..., description="The employee type of the employee")
    employment_shift: str = Field(..., description="The employment shift of the employee")
    employment_status: str = Field(..., description="The employment status of the employee")
    hire_date: date = Field(..., description="The hire date of the employee")
    work_location: uuid.UUID = Field(..., description="The work location of the employee")

    # Bank Info
    bank_account_number: str = Field(..., description="The bank account number of the employee")

    # Salary Info
    basic_salary: Decimal = Field(..., description="The basic salary of the employee")
    allowance: List = Field(..., description="The allowance of the employee")
    deduction: List = Field(..., description="The deduction of the employee")
    effective_date: date = Field(..., description="The effective date of the employee")
    currency_of_salary: str = Field(..., description="The currency of the salary")

    # Documents
    cv_file: Optional[str] = Field(None, description="The CV file of the employee")

    # Status Information
    is_active: bool = Field(..., description="The active status of the employee")

# employee schema   
class EmployeeSchema(CreateAndUpdateEmployeeRequestSchema):
    id: uuid.UUID
    work_location: CompanyAddressSchema
    department: DepartmentDataSchema
    allowance: List[AllowanceSchema]
    deduction: List[DeductionSchema]

# EMPLOYEE RESPONSE SCHEMA
class EmployeeResponseSchema(Schema):
    status: bool = Field(..., description="The status of the employee")
    status_code: int = Field(..., description="The status code of the employee")
    message: str = Field(..., description="The message of the employee")
    data: List[EmployeeSchema] = Field(..., description="The data of the employee")