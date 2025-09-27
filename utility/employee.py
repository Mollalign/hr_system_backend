# ===============================================================
# EMPLOYEE UTILS
# ===============================================================

from allowance.models import Allowance
from deduction.models import Deduction
import uuid

# get allowance data by id
def get_allowance_data_by_id(data: list[uuid.UUID]):
    if data:
        return Allowance.objects.filter(id__in=data, is_deleted=False)
    return []

# get deduction data by id
def get_deduction_data_by_id(data: list[str]):
    if data:
        other_deduction = Deduction.objects.filter(type="Other").first()
        deduction_data = [d for d in other_deduction.data if d['id'] in data]
        return deduction_data
    return []