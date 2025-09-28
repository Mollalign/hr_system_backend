# ===============================================================
# PAYROLL UTILS
# ===============================================================

from deduction.models import Deduction
from allowance.models import Allowance
import uuid

def get_tax(tax_data: dict, salary: float):
    for data in tax_data:
        try:
            min_salary = float(data["min_salary"])
        except (ValueError, TypeError):
            continue  # skip if invalid

        max_val = data.get("max_salary")

        if max_val is None:
            max_salary = float("inf")
        elif isinstance(max_val, str) and max_val.lower() in ["UNLIMITED"]:
            max_salary = float("inf")
        else:
            try:
                max_salary = float(max_val)
            except (ValueError, TypeError):
                continue  # skip if invalid

        if min_salary <= salary <= max_salary:
            return data
    return None

      
# get deductions
def get_deductions(deduction: dict, salary: float):
    # ===============================
    # DEDUCTIONS
    # ===============================
    # get tax and pension deductions
    deductions = Deduction.objects.filter(is_active=True, type__in=["Tax", "Pension"])
    deduction_tax = deductions.get(type="Tax")
    deduction_pension = deductions.get(type="Pension")
    all_deduction = {}
    total_deduction = {
        "total": 0
    }

    # tax deduction
    employee_tax_obj = get_tax(deduction_tax.data, salary) if deduction_tax is not None else []
    if employee_tax_obj:
        all_deduction["TAX"] = employee_tax_obj
        tax_deduction = (float(salary) * float(employee_tax_obj["rate"])) / 100 - float(employee_tax_obj["deduction"])
        total_deduction["total"] = tax_deduction
    else:
        all_deduction["TAX"] = {}

    # pension deduction 
    if deduction_pension.data:
        all_deduction["PENSION"] = deduction_pension.data[0]
        pension_deduction = (float(salary) * float(deduction_pension.data[0]["percentage"])) / 100
        total_deduction["total"] += pension_deduction
    else:
        all_deduction["PENSION"] = {}
    other_deduction_list = []
    # other deduction
    if deduction:
        for deduction in deduction: 
            deduction_data = get_deduction_data_by_id(deduction)
            if deduction_data:
                if deduction_data[0]["type"] == "fixed":
                    total_deduction["total"] += float(deduction_data[0]["amount"])
                elif deduction_data[0]["type"] == "percentage":
                    total_deduction["total"] += (float(salary) * float(deduction_data[0]["percentage"])) / 100
                other_deduction_list.append({
                    "id": str(deduction_data[0]["id"]),
                    "name": str(deduction_data[0]["name"]),
                    "type": str(deduction_data[0]["type"]),
                    "percentage": float(deduction_data[0]["percentage"]),
                    "amount": float(deduction_data[0]["amount"]),
                    "description": str(deduction_data[0]["description"]),
                    "is_active": bool(deduction_data[0]["is_active"])
                })
    else:
        other_deduction_list = []
    all_deduction["OTHER"] = other_deduction_list
    all_deduction["TOTAL"] = total_deduction["total"]

    return all_deduction

# get allowances
def get_allowances(allowance: list, salary: float):
    # ===============================
    # ALLOWANCES
    # ===============================
    all_allowance = {}
    allowance_list = []
    total_allowance = {
        "total": 0
    }   
    if allowance:
        for allowance in allowance:
            allowance_data = get_allowance_data_by_id(allowance)
            if allowance_data:
                if allowance_data.type == "fixed":
                    total_allowance["total"] += float(allowance_data.amount)
                elif allowance_data.type == "percentage":
                    total_allowance["total"] += (float(salary) * float(allowance_data.percentage)) / 100
                allowance_list.append({
                    "id": str(allowance_data.id),
                    "name": str(allowance_data.name),
                    "type": str(allowance_data.type),
                    "percentage": float(allowance_data.percentage),
                    "amount": float(allowance_data.amount),
                    "description": str(allowance_data.description),
                    "is_active": bool(allowance_data.is_active)
                })
    else:
        all_allowance["ALLOWANCE"] = []
        
    all_allowance["ALLOWANCE"] = allowance_list
    all_allowance["TOTAL"] =  total_allowance["total"]
    return all_allowance

# is active allowance
def get_allowance_data_by_id(allowance: uuid.UUID):
    allowance_data = Allowance.objects.filter(id=allowance, is_active=True, is_deleted=False).first()
    return allowance_data if allowance_data else None

def get_deduction_data_by_id(deduction: uuid.UUID):
   OtherDeduction = Deduction.objects.filter(is_active=True, type="Other").first()
   other_deduction_data = [d for d in OtherDeduction.data if d['id'] == deduction]    
   return other_deduction_data if other_deduction_data else None