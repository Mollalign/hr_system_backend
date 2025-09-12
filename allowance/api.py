# ===============================================================
# API ENDPOINTS FOR ALLOWANCE
# ===============================================================
# import the necessary modules
from ninja import Router
import uuid
from datetime import datetime

# ===============================
# MODELS
# ===============================
from .models import Allowance

# ===============================
# SCHEMAS
# ===============================
from .schemas import AllowanceResponseSchema, CreateAndUpdateAllowanceSchema

# ===============================
# SERIALIZERS
# ===============================
from .serializer import serialize_allowance, serialize_allowance_list

# ===============================
# VALIDATION
# ===============================
from .validation import validate_allowance

# ===============================
# ROUTERS
# ===============================
allowance_router = Router("Allowance")

# ===============================
# API ENDPOINTS FOR ALLOWANCE
# ===============================
# create allowance
@allowance_router.post("/", response=AllowanceResponseSchema, description="Create allowance")
def create_allowances(request, allowance: CreateAndUpdateAllowanceSchema):
    try:

        message = validate_allowance(allowance.dict())
        if message != "":
            return AllowanceResponseSchema(status=False, status_code=400, message=message, data=[])

        # create allowance
        allowance = Allowance.objects.create(
            name=allowance.name,
            type=allowance.type,
            percentage=allowance.percentage,
            amount=allowance.amount,
            description=allowance.description,
            is_active=allowance.is_active
        )
        result = serialize_allowance(allowance)
        return AllowanceResponseSchema(status=True, status_code=200,message="Allowance created successfully",data=[result])
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404, message=str(e), data=[])

# get all allowances
@allowance_router.get("/", response=AllowanceResponseSchema, description="Get all allowances")
def get_all_allowances(request):
    try:
        allowances = Allowance.objects.filter(is_deleted=False)
        result = serialize_allowance_list(allowances)
        return AllowanceResponseSchema(status=True, status_code=200, message="Fetch All Allowances", data=result)
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404, message=str(e), data=[])
    
# get active allowances
@allowance_router.get("/active", response=AllowanceResponseSchema, description="Get all active allowances")
def get_active_allowances(request):
    try:
        allowances = Allowance.objects.filter(is_active=True, is_deleted=False)
        result = serialize_allowance_list(allowances)
        return AllowanceResponseSchema(status=True, status_code=200, message="Fetch All Active Allowances", data=result)
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404,message=str(e), data=[])

# get allowance by id
@allowance_router.get("/{id}", response=AllowanceResponseSchema, description="Get allowance by id")
def get_allowance_by_id(request, id: uuid.UUID):
    try:
        allowance = Allowance.objects.get(id=id, is_deleted=False)
        result = serialize_allowance(allowance)
        return AllowanceResponseSchema(status=True,status_code=200, message="Allowance fetched successfully", data=[result]
        )
    except Allowance.DoesNotExist:
        return AllowanceResponseSchema(status=False, status_code=404, message="Allowance not found", data=[])
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404, message=str(e), data=[])

# update allowance
@allowance_router.put("/{id}", response=AllowanceResponseSchema, description="Update allowance")
def update_allowances(request, id: uuid.UUID, allowance: CreateAndUpdateAllowanceSchema):
    try:

        message = validate_allowance(allowance.dict())
        if message != "":
            return AllowanceResponseSchema(status=False, status_code=400, message=message, data=[])

        allowance_obj = Allowance.objects.get(id=id, is_deleted=False)
        allowance_obj.name = allowance.name
        allowance_obj.type = allowance.type
        allowance_obj.percentage = allowance.percentage
        allowance_obj.amount = allowance.amount
        allowance_obj.description = allowance.description
        allowance_obj.is_active = allowance.is_active
        allowance_obj.save()
        result = serialize_allowance(allowance_obj)
        return AllowanceResponseSchema(status=True, status_code=200,message="Allowance updated successfully",data=[result])
    except Allowance.DoesNotExist:
        return AllowanceResponseSchema(status=False, status_code=404, message="Allowance not found", data=[])
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404, message=str(e), data=[])

# delete allowance
@allowance_router.delete("/{id}", response=AllowanceResponseSchema, description="Delete allowance")
def delete_allowances(request, id: uuid.UUID):
    try:
        allowance_obj = Allowance.objects.get(id=id, is_deleted=False)
        allowance_obj.is_deleted = True
        allowance_obj.deleted_at = datetime.now()
        allowance_obj.save()
        return AllowanceResponseSchema(status=True, status_code=200, message="Allowance deleted successfully", data=[])
    except Allowance.DoesNotExist:
        return AllowanceResponseSchema(status=False, status_code=404, message="Allowance not found", data=[])
    except Exception as e:
        return AllowanceResponseSchema(status=False, status_code=404, message=str(e), data=[])