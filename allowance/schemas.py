# ===============================================================
# SCHEMA FOR ALLOWANCE
# ===============================================================
from ninja import Schema, Field
from typing import List
import uuid

# ===============================
# SCHEMA FOR ALLOWANCE
# ===============================
# create allowance
class CreateAndUpdateAllowanceSchema(Schema):
    name: str = Field(..., description="The name of the allowance")
    type: str = Field(..., description="The type of the allowance")
    percentage: float = Field(..., description="The percentage of the allowance")
    amount: float = Field(..., description="The amount of the allowance")
    description: str = Field(..., description="The description of the allowance")
    is_active: bool = Field(..., description="The status of the allowance")

# get all allowances
class AllowanceDataSchema(CreateAndUpdateAllowanceSchema):
    id: uuid.UUID = Field(..., description="The id of the allowance")

class AllowanceResponseSchema(Schema):
    status: bool = Field(..., description="The status of the allowance")
    status_code: int = Field(..., description="The status code of the allowance")
    message: str = Field(..., description="The message of the allowance")
    data: List[AllowanceDataSchema] = Field(..., description="The data of the allowance")

