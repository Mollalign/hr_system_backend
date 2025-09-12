# ===============================================================
# SCHEMA FOR DEDUCTION ,TAX AND PENSION AND OTHER DEDUCTIONS
# ===============================================================
from ninja import Schema, Field
from typing import List, Optional
from enum import Enum
import uuid

# ===============================
# SCHEMA FOR DEDUCTION
# ===============================
# create and update deduction
class DeductionCreateAndUpdateRequestSchema(Schema):
    type: str = Field(..., description="The name of the deduction")
    data: list = Field(..., description="The data of the deduction")
    is_active: bool = Field(..., description="The status of the deduction")

# get all deductions 
class DeductionDataSchema(DeductionCreateAndUpdateRequestSchema): # inherit the deduction create and update request schema
    id: uuid.UUID = Field(..., description="The id of the deduction")
    description: str = Field(..., description="The description of the deduction")

# get all deductions
class DeductionResponseSchema(Schema):
    status_code: int = Field(..., description="The status code of the deduction")
    success: bool = Field(..., description="The status of the deduction")
    message: str = Field(..., description="The message of the deduction")
    data: List[DeductionDataSchema] = Field(..., description="The data of the deduction")

# ===============================
# SCHEMA FOR TAX 
# ===============================
# create and update tax
class TaxCreateAndUpdateRequestSchema(Schema):
    name: str = Field(..., description="The name of the tax")
    min_salary: float = Field(..., description="The minimum salary of the tax")
    max_salary: Optional[float | str] = Field(..., description="The maximum salary of the tax")
    rate: float = Field(..., description="The rate of the tax")
    deduction: float = Field(..., description="The deduction of the tax")

# get all taxes
class TaxDataSchema(TaxCreateAndUpdateRequestSchema):
    id: uuid.UUID = Field(..., description="The id of the tax")

# ==============================
# SCHEMA FOR PENSION
# ==============================
# create and update pension
class PensionCreateAndUpdateRequestSchema(Schema):
    percentage: float = Field(..., description="The percentage of the pension")

# get all pensions
class PensionDataSchema(PensionCreateAndUpdateRequestSchema):
    id: uuid.UUID = Field(..., description="The id of the pension")

# ==============================
# SCHEMA FOR OTHER DEDUCTIONS
# ==============================
# type choices
class DeductionTypeChoices(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'

# create and update other deduction
class OtherDeductionCreateAndUpdateRequestSchema(Schema):
    name: str = Field(..., description="The name of the other deduction")
    type: DeductionTypeChoices = Field(..., description="The type of the other deduction")
    percentage: float = Field(..., description="The percentage of the other deduction")
    amount: float = Field(..., description="The amount of the other deduction")
    description: str = Field(..., description="The description of the other deduction")
    is_active: bool = Field(..., description="The status of the other deduction")

# get all other deductions
class OtherDeductionDataSchema(OtherDeductionCreateAndUpdateRequestSchema):
    id: uuid.UUID = Field(..., description="The id of the other deduction")
    