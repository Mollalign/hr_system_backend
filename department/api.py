from ninja import Router
from .models import Department
from employees.models import Employee
import uuid
from .schemas import (
    GetAllDepartmentsResponseSchema,
    DepartmentDataSchema, 
    DepartmentResponseMessageSchema,
    CreateDepartmentRequestSchema,
    UpdateDepartmentRequestSchema
)
from typing import Union
from ninja.errors import ValidationError


department_router = Router(tags=["Departments"])

# ===============================
# DEPARTMENT API ENDPOINTS
# ===============================
# CREATE DEPARTMENT
@department_router.post('/', response=Union[GetAllDepartmentsResponseSchema, DepartmentResponseMessageSchema])
def create_department(request, department: CreateDepartmentRequestSchema):
    try:
        if Department.objects.filter(dep_name=department.name).exists():
            return DepartmentResponseMessageSchema(status_code=400, success=False, message="Department already exists")
        
        manager = Employee.objects.get(id=department.manager_id, is_deleted=False) if department.manager_id else None
        dep_obj = Department.objects.create(
            dep_name=department.name,
            manager=manager,
            is_active=department.is_active
        )

        manager_name = manager.full_name if manager else ""
        return GetAllDepartmentsResponseSchema(
            status_code=200,
            success=True,
            message="Department created successfully",
            data=[DepartmentDataSchema(
                id=dep_obj.id,
                name=dep_obj.dep_name,
                manager_name=manager_name,
                is_active=dep_obj.is_active
            )]
        )
    
    except ValidationError as e:
        return DepartmentResponseMessageSchema(status_code=400, success=False, message=str(e))
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))


# GET ALL DEPARTMENTS
@department_router.get('/', response=Union[GetAllDepartmentsResponseSchema, DepartmentResponseMessageSchema])
def get_all_departments(request):
    try:
        departments = Department.objects.select_related('manager').filter(is_deleted=False)
        result = []

        for dep in departments:
            manager_name = dep.manager.full_name if dep.manager else ""
            result.append(DepartmentDataSchema(
                id=dep.id,
                name=dep.dep_name,
                manager_name=manager_name,
                is_active=dep.is_active
            )) 

        return GetAllDepartmentsResponseSchema(
            status_code=200,
            success=True,
            message="All Departments fetched successfully",
            data=result
        )    
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))
    

# GET ACTIVE DEPARTMENTS
@department_router.get('/active', response=Union[GetAllDepartmentsResponseSchema, DepartmentResponseMessageSchema])
def get_active_departments(request):
    try:
        departments = Department.objects.select_related('manager').filter(is_deleted=False, is_active=True)
        result = []
        for dep in departments:
            manager_name = dep.manager.full_name if dep.manager else ""
            result.append(DepartmentDataSchema(
                id=dep.id,
                name=dep.dep_name,
                manager_name=manager_name,
                is_active=dep.is_active
            ))

        return GetAllDepartmentsResponseSchema(
            status_code=200,
            success=True,
            message="Active Departments fetched successfully",
            data=result
        )
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))


# GET DEPARTMENT BY ID      
@department_router.get('/{id}', response=Union[GetAllDepartmentsResponseSchema, DepartmentResponseMessageSchema])
def get_department_by_id(request, id: uuid.UUID):
    try:
        department = Department.objects.select_related('manager').get(id=id, is_deleted=False)
        if department is None:
            raise Department.DoesNotExist
        else:
            manager_name = department.manager.full_name if department.manager else ""
            data = DepartmentDataSchema(
                id=department.id,
                name=department.dep_name,
                manager_name=manager_name,
                is_active=department.is_active
            )
            return GetAllDepartmentsResponseSchema(
                status_code=200,
                success=True,
                message="Department fetched successfully",
                data=[data]
            )
              
    except Department.DoesNotExist:
        return DepartmentResponseMessageSchema(status_code=404, success=False, message="Department not found")
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))
    

# UPDATE DEPARTMENT
@department_router.put('/{id}', response=Union[GetAllDepartmentsResponseSchema])
def update_department(request, id: uuid.UUID, department: UpdateDepartmentRequestSchema):
    try:
        department_obj = Department.objects.select_related('manager').get(id=id, is_deleted=False)
        manager = Employee.objects.get(id=department.manager_id, is_deleted=False) if department.manager_id else None

        # check if name is exists
        if Department.objects.filter(dep_name=department.name).exclude(id=id).exists():
            return DepartmentResponseMessageSchema(status_code=400, success=False, message="Department name already exists")
        
        # update department 
        department_obj.dep_name = department.name
        department_obj.manager = manager
        department_obj.is_active = department.is_active
        department_obj.save()

        manager_name = manager.full_name if manager else ""
        return GetAllDepartmentsResponseSchema(
            status_code=200,
            success=True,
            message="Department updated successfully",
            data=[DepartmentDataSchema(
                id=department_obj.id,
                name=department_obj.dep_name,
                manager_name=manager_name,
                is_active=department_obj.is_active
            )]
        )
    except Department.DoesNotExist:
        return DepartmentResponseMessageSchema(status_code=404, success=False, message="Department not found")
    except ValidationError as e:
        return DepartmentResponseMessageSchema(status_code=400, success=False, message=str(e))
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))
    

# DELETE DEPARTMENT
@department_router.delete('/{id}', response=Union[DepartmentResponseMessageSchema, DepartmentResponseMessageSchema])
def delete_department(request, id: uuid.UUID):  
    try:
        department_obj = Department.objects.get(id=id, is_deleted=False)
        department_obj.is_deleted = True
        department_obj.save()
        return DepartmentResponseMessageSchema(message="Department deleted successfully", status_code=200, success=True)
    except Department.DoesNotExist:
        return DepartmentResponseMessageSchema(status_code=404, success=False, message="Department not found")
    except Exception as e:
        return DepartmentResponseMessageSchema(status_code=500, success=False, message=str(e))
    