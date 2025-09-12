# ===============================================================
# SERIALIZER FOR ALLOWANCE
# ===============================================================
from .models import Allowance
from .schemas import AllowanceDataSchema

# ===============================
# SERIALIZER FOR ALLOWANCE
# ===============================
def serialize_allowance(obj: Allowance):
    if not obj:
        return None
        
    return AllowanceDataSchema(
        id=obj.id,
        name=obj.name,
        type=obj.type,
        percentage=obj.percentage,
        amount=obj.amount,
        description=obj.description,
        is_active=obj.is_active
    )

# ===============================
# HELPERS FOR SERIALIZER
# ===============================
def serialize_allowance_list(objs: list[Allowance]):
    print(objs)
    return [serialize_allowance(obj) for obj in objs]

def serialize_allowance_single(obj: Allowance):
    return serialize_allowance(obj).model_dump()