from ninja import Schema, Field
from uuid import UUID
import re
from typing import List
from pydantic import field_validator

# ================
# SCHEMA FOR COMPANY ADDRESS
# ================
# GET ALL COMPANY ADDRESSES
class CompanyAddressDataSchema(Schema):
    id: UUID= Field(..., description="The id of the company address")    
    branch_name: str= Field(..., description="The name of the company address")
    branch_phone: str= Field(..., description="The phone of the company address")
    branch_email: str= Field(..., description="The email of the company address")
    branch_address: str= Field(..., description="The address of the company address")
    is_active: bool= Field(..., description="The status of the company address")

# GET ALL COMPANY ADDRESSES RESPONSE
class CompanyAddressResponse(Schema):
    status_code: int= Field(..., description="The status code of the company address")
    success: bool= Field(..., description="The success of the company address")
    message: str= Field(..., description="The message of the company address")
    data: List[CompanyAddressDataSchema]

# GET ALL COMPANY ADDRESSES RESPONSE MESSAGE
class CompanyAddressResponseMessage(Schema):
    message: str= Field(..., description="The message of the company address")
    status_code: int= Field(..., description="The status code of the company address")
    success: bool= Field(..., description="The success of the company address")

# CREATE COMPANY ADDRESS REQUEST
class CreateCompanyAddressRequest(Schema):
    branch_name: str= Field(..., description="The name of the company address")
    branch_phone: str= Field(..., description="The phone of the company address")
    branch_email: str= Field(..., description="The email of the company address")
    branch_address: str= Field(..., description="The address of the company address")
    is_active: bool= Field(..., description="The status of the company address")

    @field_validator('branch_name')
    def validate_branch_name(cls, v):
        if len(v) < 3:
            raise ValueError("Branch name must be at least 3 characters long")
        return v
    
    @field_validator('branch_email')
    def validate_branch_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email address")
        return v
    
    @field_validator('branch_address')
    def validate_branch_address(cls, v):
        if len(v) < 5:
            raise ValueError("Branch address must be at least 5 characters long")
        return v

# UPDATE COMPANY ADDRESS REQUEST
class UpdateCompanyAddressRequest(Schema):
    branch_name: str= Field(..., description="The name of the company address")
    branch_phone: str= Field(..., description="The phone of the company address")
    branch_email: str= Field(..., description="The email of the company address")
    branch_address: str= Field(..., description="The address of the company address")
    is_active: bool= Field(..., description="The status of the company address")

    @field_validator('branch_name')
    def validate_branch_name(cls, v):
        if len(v) < 3:
            raise ValueError("Branch name must be at least 3 characters long")
        return v
    
    @field_validator('branch_email')
    def validate_branch_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email address")
        return v
    
    @field_validator('branch_address')
    def validate_branch_address(cls, v):
        if len(v) < 10:
            raise ValueError("Branch address must be at least 5 characters long")
        return v
    
# DELETE COMPANY ADDRESS REQUEST
class DeleteCompanyAddressRequest(Schema):
    id: UUID= Field(..., description="The id of the company address")
