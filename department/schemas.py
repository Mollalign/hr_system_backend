from ninja import Schema, Field
import uuid
from typing import List, Optional
from pydantic import field_validator

# ===============================
# SCHEMA FOR DEPARTMENT
# ===============================
# GET ALL DEPARTMENTS
class DepartmentDataSchema(Schema):
    id: uuid.UUID = Field(..., description="The id of the department")
    name: str = Field(..., description="The name of the department")
    manager_name: str = Field(..., description="The manager name of the department")
    is_active: bool = Field(..., description="The status of the department")

class GetAllDepartmentsResponseSchema(Schema):
    status_code: int = Field(..., description="The status code of the department")
    success: bool = Field(..., description="The success of the department")
    message: str = Field(..., description="The message of the department")
    data: List[DepartmentDataSchema] = Field(..., description="The data of the department")

# CREATE DEPARTMENT
class CreateDepartmentRequestSchema(Schema):
    name: str = Field(..., description="The name of the department")
    manager_id: Optional[str] = Field(None, description="The manager id of the department")
    is_active: bool = Field(..., description="The status of the department")

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Department name must be at least 3 characters long")
        return v
    
# UPDATE DEPARTMENT  
class UpdateDepartmentRequestSchema(Schema):
    name: str = Field(..., description="The name of the department")
    manager_id: Optional[str] = Field(None, description="The manager id of the department")
    is_active: bool = Field(..., description="The status of the department")

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Department name must be at least 3 characters long")
        return v
    
# DELETE DEPARTMENT
class DeleteDepartmentRequestSchema(Schema):
    id: uuid.UUID = Field(..., description="The id of the department")

# DELETE DEPARTMENT RESPONSE
class DepartmentResponseMessageSchema(Schema):
    message: str = Field(..., description="The message of the department")
    status_code: int = Field(..., description="The status code of the department")
    success: bool = Field(..., description="The success of the department")
