# ===============================================================
# SERIALIZER FOR DEDUCTION CATEGORY AND DEDUCTION
# ===============================================================
from .models import Deduction
from .schemas import DeductionDataSchema, TaxDataSchema, PensionDataSchema, OtherDeductionDataSchema

# ===============================
# SERIALIZER FOR DEDUCTION 
# ===============================
def serialize_deduction(obj: Deduction):
    data = []
    if not obj:
        return None

    if obj.type == 'Tax':
        data = serialize_tax(obj.data)
        
    elif obj.type == 'Pension':
        data = serialize_pension(obj.data)
        
    elif obj.type == 'Other':
        data = serialize_other_deduction(obj.data)
        
    return DeductionDataSchema(
        id=obj.id,
        type=obj.type,
        data=data,
        description=obj.description,
        is_active=obj.is_active
    )

# ===============================
# SERIALIZER FOR TAX
# ===============================
def serialize_tax(obj: list[dict]):
    if not obj:
        return []
        
    return [TaxDataSchema(
        id=obj['id'],
        name=obj['name'],
        min_salary=obj['min_salary'],
        max_salary=obj['max_salary'] if obj['max_salary'] else "UNLIMITED",
        rate=obj['rate'],
        deduction=obj['deduction']
    ) for obj in obj]

# ===============================
# SERIALIZER FOR PENSION
# ===============================
def serialize_pension(obj: list[dict]):
    if not obj:
        return []

    return [PensionDataSchema(
        id=obj['id'],
        percentage=obj['percentage']
    ) for obj in obj]
    
# ===============================
# SERIALIZER FOR OTHER DEDUCTIONS
# ===============================
def serialize_other_deduction(obj: list[dict]):
    if not obj:
        return []
    return [OtherDeductionDataSchema(
        id=obj['id'],
        name=obj['name'],
        type=obj['type'],
        percentage=obj['percentage'],
        amount=obj['amount'],
        description=obj['description'],
        is_active=obj['is_active']
    ) for obj in obj]
    
# ================================================================================
# HELPER FUNCTION FOR SERIALIZATION OF LIST OF DEDUCTIONS AND DEDUCTION CATEGORIES
# ================================================================================
# serialize list of deductions
def serialize_deduction_list(objs: list[Deduction]):
    return [serialize_deduction(obj) for obj in objs]

# serialize single deduction
def serialize_deduction_single(objs: Deduction) -> dict:
    result = serialize_deduction(objs).model_dump()
    return result