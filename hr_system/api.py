from ninja import NinjaAPI
from users.api import user_router 
from employees.api import employee_router
from department.api import department_router
from company_address.api import company_address_router

# api
api = NinjaAPI(
    title="Hr System",
    description="",
    version="1.0.0",
    urls_namespace=""
)

# Add routers
api.add_router("/user/", user_router)
api.add_router("/employee/", employee_router)
api.add_router("/department/", department_router)
api.add_router("/company_address", company_address_router)

