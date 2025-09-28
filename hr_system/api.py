from ninja import NinjaAPI
from employees.api import employee_router
from department.api import department_router
from company_address.api import company_address_router
from allowance.api import allowance_router
from deduction.api import deduction_router
from attendance.api import attendance_router
from emp_payroll.api import payroll_router

# api
api = NinjaAPI(
    title="Hr System",
    description="",
    version="1.0.0",
    urls_namespace=""
)

# Add routers
api.add_router("/employee/", employee_router)
api.add_router("/department/", department_router)
api.add_router("/company_address", company_address_router)
api.add_router("/allowance", allowance_router)
api.add_router("/deduction", deduction_router)
api.add_router("/attendance", attendance_router)
api.add_router("/payroll", payroll_router)

