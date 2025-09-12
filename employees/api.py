# ===============================================================
# EMPLOYEE API
# ===============================================================
# import the necessary modules
from ninja import Router
from datetime import date
import uuid

# ===============================
# MODELS
# ===============================
from department.models import Department
from company_address.models import CompanyAddress
from allowance.models import Allowance
from deduction.models import Deduction
from employees.models import Employee

# ===============================
# SCHEMAS
# ===============================
from employees.schemas import EmployeeResponseSchema, CreateAndUpdateEmployeeRequestSchema

# ===============================
# SERIALIZERS
# ===============================
from employees.serializers import serialize_employee_list, serialize_employee_single

# ===============================
# ROUTERS
# ===============================
employee_router = Router(tags=["Employees"])


# ===============================
# EMPLOYEE API ENDPOINTS 
# ===============================
# create employee
@employee_router.post('/', response=EmployeeResponseSchema)
def create_employee(request, employee: CreateAndUpdateEmployeeRequestSchema):
    try:
        department = Department.objects.get(id=employee.department, is_deleted=False, is_active=True)
        work_location = CompanyAddress.objects.get(id=employee.work_location, is_deleted=False, is_active=True)
        allowance = Allowance.objects.filter(id__in=employee.allowance, is_deleted=False)
        deduction = Deduction.objects.filter(id__in=employee.deduction, is_deleted=False)

        employee_obj = Employee.objects.create(
            # Personal Info
            full_name=employee.full_name,
            gender=employee.gender if employee.gender else "male",
            date_of_birth=employee.date_of_birth if employee.date_of_birth else date.today(), 
            maternal_status=employee.maternal_status if employee.maternal_status else "single",
            nationality=employee.nationality if employee.nationality else "Ethiopian",

            # Contact Info
            email=employee.email,
            phone_number=employee.phone_number,
            alternative_phone_number=employee.alternative_phone_number if employee.alternative_phone_number else "+251912345678",

            # Address Info
            permanent_address=employee.permanent_address if employee.permanent_address else "123 Main St, Anytown, USA",
            current_address=employee.current_address if employee.current_address else "123 Main St, Anytown, USA",
            city=employee.city if employee.city else "Addis Ababa",
            state=employee.state if employee.state else "Addis Ababa",
            country=employee.country if employee.country else "Ethiopia",
            zip_code=employee.zip_code if employee.zip_code else "1000",

            # Emergency Contact Info
            contact_person_name=employee.contact_person_name if employee.contact_person_name else "John Doe",
            contact_person_relationship=employee.contact_person_relationship if employee.contact_person_relationship else "other",
            contact_person_phone=employee.contact_person_phone if employee.contact_person_phone else "+251912345678",
            contact_person_alternative_phone=employee.contact_person_alternative_phone if employee.contact_person_alternative_phone else "+251912345678",
            contact_person_address=employee.contact_person_address if employee.contact_person_address else "123 Main St, Anytown, USA",

            # Job Info
            employee_code=employee.employee_code if employee.employee_code else "EMP001",
            job_title=employee.job_title if employee.job_title else "Software Engineer",
            department=department,
            employee_type=employee.employee_type if employee.employee_type else "permanent",
            employment_shift=employee.employment_shift if employee.employment_shift else "full_time",
            employment_status=employee.employment_status if employee.employment_status else "on_duty",
            hire_date=employee.hire_date if employee.hire_date else date.today(),
            work_location=work_location,

            # Bank Info
            bank_account_number=employee.bank_account_number if employee.bank_account_number else "1234567890",

            # Salary Info
            basic_salary=employee.basic_salary if employee.basic_salary else 0,
            effective_date=employee.effective_date if employee.effective_date else date.today(),

            # Status Information
            is_active=employee.is_active if employee.is_active else True,

            # Currency Info
            currency_of_salary=employee.currency_of_salary if employee.currency_of_salary else "ETB",

            # Documents
            cv_file=employee.cv_file if employee.cv_file else None,
        )

        # Add allowance and deduction to the employee
        employee_obj.allowance.set(allowance)
        employee_obj.deduction.set(deduction)

        serialized_employee = serialize_employee_single(employee_obj)

        return EmployeeResponseSchema(status=True, status_code=201, message="Employee created successfully", data=[serialized_employee])
    except Department.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Department not found", data=[])
    except CompanyAddress.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Work location not found", data=[])
    except Allowance.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Allowance not found", data=[])
    except Deduction.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Deduction not found", data=[])
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])
    

# get all employees
@employee_router.get('/', response=EmployeeResponseSchema)
def get_all_employees(request):
    try:
        employees = Employee.objects.filter(is_deleted=False)
        print(employees)
        serialized_employees = serialize_employee_list(employees)
        return EmployeeResponseSchema(status=True, status_code=200, message="Employees fetched successfully", data=serialized_employees)
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])


# get all active employees
@employee_router.get('/active', response=EmployeeResponseSchema)
def get_active_employees(request):
    try:
        employees = Employee.objects.filter(is_deleted=False, is_active=True)
        serialized_employees = serialize_employee_list(employees)
        return EmployeeResponseSchema(status=True, status_code=200, message="Employees fetched successfully", data=serialized_employees)
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])
    
# get employee by id
@employee_router.get('/{id}', response=EmployeeResponseSchema)
def get_employee_by_id(request, id: uuid.UUID):
    try:
        employee = Employee.objects.get(id=id, is_deleted=False)
        serialized_employee = serialize_employee_single(employee)
        return EmployeeResponseSchema(status=True, status_code=200, message="Employee fetched successfully", data=[serialized_employee])
    except Employee.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Employee not found", data=[])
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])    
    

# update employee
@employee_router.put('/{id}', response=EmployeeResponseSchema)
def update_employee(request, id: uuid.UUID, employee_data: CreateAndUpdateEmployeeRequestSchema):
    try:
        employee = Employee.objects.get(id=id, is_deleted=False)
        
        employee.full_name = employee_data.full_name
        employee.gender = employee_data.gender
        employee.date_of_birth = employee_data.date_of_birth
        employee.maternal_status = employee_data.maternal_status
        employee.nationality = employee_data.nationality
        
        employee.email = employee_data.email
        
        employee.phone_number = employee_data.phone_number
        employee.alternative_phone_number = employee_data.alternative_phone_number
        employee.permanent_address = employee_data.permanent_address
        employee.current_address = employee_data.current_address
        employee.city = employee_data.city
        employee.state = employee_data.state
        employee.country = employee_data.country
        employee.zip_code = employee_data.zip_code
        
        employee.contact_person_name = employee_data.contact_person_name
        employee.contact_person_relationship = employee_data.contact_person_relationship
        employee.contact_person_phone = employee_data.contact_person_phone
        employee.contact_person_alternative_phone = employee_data.contact_person_alternative_phone
        employee.contact_person_address = employee_data.contact_person_address
        
        employee.employee_code = employee_data.employee_code
        employee.job_title = employee_data.job_title
        employee.employee_type = employee_data.employee_type
        employee.employment_shift = employee_data.employment_shift
        employee.employment_status = employee_data.employment_status
        employee.hire_date = employee_data.hire_date
        
        employee.bank_account_number = employee_data.bank_account_number
        employee.basic_salary = employee_data.basic_salary
        employee.effective_date = employee_data.effective_date
        employee.currency_of_salary = employee_data.currency_of_salary
        
        employee.is_active = employee_data.is_active
        employee.cv_file = employee_data.cv_file
        
        # Update employee fields
        for field, value in employee_data.dict().items():
            if hasattr(employee, field) and field not in ['department', 'work_location', 'allowance', 'deduction']:
                setattr(employee, field, value)
        
        # Handle related fields
        if employee_data.department:
            department = Department.objects.get(id=employee_data.department, is_deleted=False)
            employee.department = department
            
        if employee_data.work_location:
            work_location = CompanyAddress.objects.get(id=employee_data.work_location, is_deleted=False)
            employee.work_location = work_location
            
        if employee_data.allowance:
            allowance = Allowance.objects.filter(id__in=employee_data.allowance, is_deleted=False)
            employee.allowance.set(allowance)
            
        if employee_data.deduction:
            deduction = Deduction.objects.filter(id__in=employee_data.deduction, is_deleted=False)
            employee.deduction.set(deduction)
        
        # update employee
        employee.save()

        serialized_employee = serialize_employee_single(employee)
        return EmployeeResponseSchema(status=True, status_code=200, message="Employee updated successfully", data=[serialized_employee])
    except Employee.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Employee not found", data=[])
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])

# delete employee
@employee_router.delete('/{id}', response=EmployeeResponseSchema)
def delete_employee(request, id: uuid.UUID):
    try:
        employee = Employee.objects.get(id=id, is_deleted=False)
        employee.is_deleted = True
        employee.save()
        return EmployeeResponseSchema(status=True, status_code=200, message="Employee deleted successfully", data=[])
    except Employee.DoesNotExist:
        return EmployeeResponseSchema(status=False, status_code=404, message="Employee not found", data=[])
    except Exception as e:
        return EmployeeResponseSchema(status=False, status_code=500, message=str(e), data=[])    
    