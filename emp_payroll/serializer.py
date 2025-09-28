# ===============================================================
# PAYROLL SERIALIZER
# ===============================================================
from .models import Payroll
from .schemas import PayrollSchema, EmployeeSchema, DepartmentSchema

# ===============================
# SERIALIZER FOR PAYROLL
# ===============================
def serialize_payroll(obj: Payroll):
    return PayrollSchema(
        id=obj.id,  
        employee_id=EmployeeSchema(
            id=obj.employee_id.id,
            full_name=obj.employee_id.full_name,
        ),
        basic_salary=obj.basic_salary,
        department=DepartmentSchema(
                    id=obj.employee_id.department.id,
                    name=obj.employee_id.department.dep_name,
                    manager_name=obj.employee_id.department.manager_id.full_name if obj.employee_id.department.manager_id else "Not Assiged",
                ),
        allowance=obj.allowance,
        deduction=obj.deduction,
        payment_date=obj.payment_date
    )   

# ===============================
# HELPER SERIALIZER FOR PAYROLL LIST AND SINGLE
# ===============================
# serialize the list of payrolls
def serialize_payroll_list(obj: list[Payroll]):
    return [serialize_payroll(item) for item in obj]

# serialize the single payroll
def serialize_payroll_single(obj: Payroll):
    return serialize_payroll(obj).model_dump()