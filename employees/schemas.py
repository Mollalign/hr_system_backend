# ===============================================================
# SCHEMA FOR EMPLOYEE
# ===============================================================
from ninja import Schema, Field
from typing import List, Optional
import re
import uuid
from datetime import date
from pydantic import EmailStr, field_validator
from department.schemas import DepartmentDataSchema

from decimal import Decimal

# ===============================
# SCHEMA FOR ALLOWANCE
# ===============================
class AllowanceSchema(Schema):
    id: uuid.UUID = Field(..., description="The id of the allowance")
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
    id: uuid.UUID = Field(..., description="The id of the deduction")
    branch_name: str = Field(..., description="The branch name of the company address")
    branch_phone: str = Field(..., description="The branch phone of the company address")
    branch_email: str = Field(..., description="The branch email of the company address")
    branch_address: str = Field(..., description="The branch address of the company address")
    is_active: bool = Field(..., description="The active status of the company address")

# ===============================
# SCHEMA FOR DEDUCTION
# ===============================
class DeductionSchema(Schema):
    id: uuid.UUID = Field(..., description="The id of the deduction")
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
    allowance: List[uuid.UUID] = Field(..., description="The allowance of the employee")
    deduction: List[uuid.UUID] = Field(..., description="The deduction of the employee")
    effective_date: date = Field(..., description="The effective date of the employee")
    currency_of_salary: str = Field(..., description="The currency of the salary")

    # Documents
    cv_file: Optional[str] = Field(None, description="The CV file of the employee")

    # Status Information
    is_active: bool = Field(..., description="The active status of the employee")

    # validations
    @field_validator('full_name')
    def validate_full_name(cls, value):
        if not value:
            raise ValueError("Full name is required")
        if len(value) < 3:
            raise ValueError("Full name must be at least 3 characters long")
        if len(value) > 50:
            raise ValueError("Full name must be less than 50 characters")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValueError("Full name must contain only letters and spaces")
        name_parts = [part for part in value.strip().split() if part]
        if len(name_parts) < 2:
            raise ValueError("Full name must contain at least first and last name")
        return value
    
    # @field_validator('gender')
    # def validate_gender(cls, value):
    #     if not value:
    #         raise ValueError("Gender is required")
    #     valid_genders = ['male', 'female']
    #     if value.lower() not in valid_genders:
    #         raise ValueError("Gender must be male or female")
    #     return value
    
    # @field_validator('date_of_birth')
    # def validate_date_of_birth(cls, value):
    #     if not value:
    #         raise ValueError("Date of birth is required")
    #     if value > date.today():
    #         raise ValueError("Date of birth cannot be in the future")
    #     return value
    
    @field_validator('maternal_status')
    def validate_maternal_status(cls, value):
        if not value:
            raise ValueError("Maternal status is required")
        valid_maternal_status = ['single', 'married', 'divorced', 'widowed']
        if value.lower() not in valid_maternal_status:
            raise ValueError("Maternal status must be single, married, divorced, or widowed")
        return value
    
    @field_validator('nationality')
    def validate_nationality(cls, value):
        if not value:
            raise ValueError("Nationality is required")
        if len(value) < 3:
            raise ValueError("Nationality must be at least 3 characters long")
        if len(value) > 50:
            raise ValueError("Nationality must be less than 50 characters")
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValueError("Nationality must contain only letters and spaces")
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email is required")
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if not value:
            raise ValueError("Phone number is required")
        return value

    @field_validator('permanent_address')
    def validate_permanent_address(cls, value):
        if not value:
            raise ValueError("Permanent address is required")
        return value

    @field_validator('city')
    def validate_city(cls, value):
        if not value:
            raise ValueError("City is required")
        return value

    @field_validator('state')
    def validate_state(cls, value):
        if not value:
            raise ValueError("State is required")
        return value

    @field_validator('country')
    def validate_country(cls, value):
        if not value:
            raise ValueError("Country is required")
        return value

    @field_validator('zip_code')
    def validate_zip_code(cls, value):
        if not value:
            raise ValueError("Zip code is required")
        return value

    # @field_validator('contact_person_name')
    # def validate_contact_person_name(cls, value):
    #     if not value:
    #         raise ValueError("Contact person name is required")
    #     return value

    @field_validator('contact_person_relationship')
    def validate_contact_person_relationship(cls, value):
        if not value:
            raise ValueError("Contact person relationship is required")
        return value

    @field_validator('contact_person_phone')
    def validate_contact_person_phone(cls, value):
        if not value:
            raise ValueError("Contact person phone is required")
        return value

    # @field_validator('employee_code')
    # def validate_employee_code(cls, value):
    #     if not value:
    #         raise ValueError("Employee code is required")
    #     return value

    @field_validator('job_title')
    def validate_job_title(cls, value):
        if not value:
            raise ValueError("Job title is required")
        return value

    @field_validator('department')
    def validate_department(cls, value):
        if not value:
            raise ValueError("Department is required")
        return value

    @field_validator('employee_type')
    def validate_employee_type(cls, value):
        if not value:
            raise ValueError("Employee type is required")
        return value

    # @field_validator('employment_shift')
    # def validate_employment_shift(cls, value):
    #     if not value:
    #         raise ValueError("Employment shift is required")
    #     return value

    @field_validator('employment_status')
    def validate_employment_status(cls, value):
        if not value:
            raise ValueError("Employment status is required")
        return value

    @field_validator('hire_date')
    def validate_hire_date(cls, value):
        if not value:
            raise ValueError("Hire date is required")
        if value > date.today():
            raise ValueError("Hire date cannot be in the future")
        return value

    @field_validator('work_location')
    def validate_work_location(cls, value):
        if not value:
            raise ValueError("Work location is required")
        return value

    @field_validator('bank_account_number')
    def validate_bank_account_number(cls, value):
        if not value:
            raise ValueError("Bank account number is required")
        return value

    @field_validator('basic_salary')
    def validate_basic_salary(cls, value):
        if not value:
            raise ValueError("Basic salary is required")
        if value <= 0:
            raise ValueError("Basic salary must be greater than 0")
        return value

    @field_validator('currency_of_salary')
    def validate_currency_of_salary(cls, value):
        if not value:
            raise ValueError("Currency of salary is required")
        
        return value

    @field_validator('effective_date')
    def validate_effective_date(cls, value):
        if not value:
            raise ValueError("Effective date is required")
        return value

    # @field_validator('cv_file')
    # def validate_cv_file(cls, value):
    #     if not value or value.strip() == "":
    #         raise ValueError("CV file is required")
    #     return value

# employee schema   
class EmployeeSchema(CreateAndUpdateEmployeeRequestSchema):
    id: uuid.UUID
    work_location: CompanyAddressSchema
    department: DepartmentDataSchema
    allowance: List[AllowanceSchema]
    deduction: List[DeductionSchema]

# EMPLOYE RESPONSE SCHEMA
class EmployeeResponseSchema(Schema):
    status: bool = Field(..., description="The status of the employee")
    status_code: int = Field(..., description="The status code of the employee")
    message: str = Field(..., description="The message of the employee")
    data: List[EmployeeSchema] = Field(..., description="The data of the employee")