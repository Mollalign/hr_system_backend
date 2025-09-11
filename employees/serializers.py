# ===============================================================
# EMPLOYEE SERIALIZER
# ===============================================================
from employees.models import Employee
from employees.schemas import EmployeeSchema, CompanyAddressSchema, AllowanceSchema, DeductionSchema
from department.schemas import DepartmentDataSchema
def serialize_employee(employee: Employee):
    return EmployeeSchema(
        # Personal Info
                id=employee.id,
                full_name=employee.full_name,
                gender=employee.gender,
                date_of_birth=employee.date_of_birth,
                maternal_status=employee.maternal_status,
                nationality=employee.nationality,

                # Contact Info
                email=employee.email,
                phone_number=str(employee.phone_number),
                alternative_phone_number=str(employee.alternative_phone_number) if employee.alternative_phone_number else None,

                # Address Info
                permanent_address=employee.permanent_address,
                current_address=employee.current_address,
                city=employee.city,
                state=employee.state,
                country=employee.country,
                zip_code=employee.zip_code,

                # Emergency Contact Info
                contact_person_name=employee.contact_person_name,
                contact_person_relationship=employee.contact_person_relationship,
                contact_person_phone=str(employee.contact_person_phone),
                contact_person_alternative_phone=str(employee.contact_person_alternative_phone) if employee.contact_person_alternative_phone else None,
                contact_person_address=employee.contact_person_address,

                # Job Info
                employee_code=employee.employee_code,
                job_title=employee.job_title,
                department=DepartmentDataSchema(
                    id=employee.department.id,
                    name=employee.department.dep_name,
                    manager_name=employee.department.manager_id.full_name if employee.department.manager_id else "",
                    is_active=employee.department.is_active,
                ),
                employee_type=employee.employee_type,
                employment_shift=employee.employment_shift,
                employment_status=employee.employment_status,
                hire_date=employee.hire_date,
                work_location=CompanyAddressSchema(
                    id=employee.work_location.id,
                    branch_name=employee.work_location.branch_name,
                    branch_phone=str(employee.work_location.branch_phone),
                    branch_email=employee.work_location.branch_email,
                    branch_address=employee.work_location.branch_address,
                    is_active=employee.work_location.is_active,
                ),

                # Bank Info
                bank_account_number=employee.bank_account_number,

                # Salary Info
                basic_salary=employee.basic_salary,
                allowance=employee.allowance,
                deduction=employee.deduction,
                effective_date=employee.effective_date,
                currency_of_salary=employee.currency_of_salary,

                # Documents
                cv_file=employee.cv_file,

                # Status Information
                is_active=employee.is_active
    )

# ===============================
# HELPERS FOR SERIALIZER
# ===============================
def serialize_employee_list(employees: list[Employee]):
    return [serialize_employee(employee) for employee in employees]

def serialize_employee_single(employee: Employee):
    return serialize_employee(employee).model_dump()