# ===============================================================
# EMPLOYEE UTILS
# ===============================================================

from hr_system.models.allowance import Allowance
from hr_system.models.deduction import Deduction
import uuid

# get allowance data by id
def get_allowance_data_by_id(data: list[uuid.UUID], db_name: str):
    if data:
        return Allowance.objects.using(db_name).filter(id__in=data, is_deleted=False)
    return []

# get deduction data by id
def get_deduction_data_by_id(data: list[str], db_name: str):
    if data:
        other_deduction = Deduction.objects.using(db_name).filter(type="Other").first()
        deduction_data = [d for d in other_deduction.data if d['id'] in data]
        return deduction_data
    return []