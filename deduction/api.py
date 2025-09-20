# ===============================================================
# API ENDPOINTS FOR DEDUCTION 
# ===============================================================
# import the necessary modules
from ninja import Router
from ninja.errors import ValidationError
import uuid

# ===============================
# MODELS
# ===============================
from .models import Deduction

# ===============================
# SCHEMAS
# ===============================
from .schemas import DeductionResponseSchema, DeductionCreateAndUpdateRequestSchema

# ===============================
# SERIALIZERS
# ===============================
from .serializer import serialize_deduction_list, serialize_deduction_single  

# ===============================
# VALIDATION
# ===============================
from .validation import validate_deduction

# ===============================
# ROUTERS
# ===============================
deduction_router = Router(tags=["Deduction"])

# ===============================
# API ENDPOINTS FOR DEDUCTION
# ===============================
# create deduction
@deduction_router.post("/", response=DeductionResponseSchema, description="Create deduction")
def create_deduction(request, deduction: DeductionCreateAndUpdateRequestSchema):
    try:

        # check if deduction category exists
        category_obj = Deduction.objects.get(type=deduction.type)
        data = deduction.data

        message = validate_deduction(data, category_obj.type)
        if message != "":
            return DeductionResponseSchema(status_code=400, success=False, message=message, data=[])

        data =  [t for t in data]
        for item in data:
            if "id" not in item or not item["id"]: 
                item["id"] = str(uuid.uuid4())

        # Update deduction
        category_obj.data.extend(data)   # use extend instead of append to add all new deductions
        category_obj.save()
        result = serialize_deduction_single(category_obj)
        return DeductionResponseSchema(status_code=200, success=True, message="Deduction created successfully", data=[result])
    except Deduction.DoesNotExist:
        return DeductionResponseSchema(status_code=404, success=False, message="Deduction Type not found in Tax, Pension or Other", data=[])
    except ValidationError as e:
        return DeductionResponseSchema(status_code=500, success=False, message=str(e), data=[])
    except Exception as e:
        return DeductionResponseSchema(status_code=500, success=False, message=str(e), data=[])

# get all deductions
@deduction_router.get("/", response=DeductionResponseSchema, description="Get all deductions")
def get_all_deductions(request):
    try:
        deductions = Deduction.objects.all()
        result = serialize_deduction_list(deductions)
        print(result)
        return DeductionResponseSchema(status_code=200, success=True, message="All Deductions fetched successfully", data=result)
    except Exception as e:
        return DeductionResponseSchema(status_code=500, success=False, message=str(e), data=[])

# get deduction by id
@deduction_router.get("/{category}", response=DeductionResponseSchema, description="Get deduction by id")
def get_deduction_by_id(request, category: str):
    try:
        deduction = Deduction.objects.get(type=category)
        result = serialize_deduction_single(deduction)
        return DeductionResponseSchema(status_code=200, success=True, message="Deduction fetched successfully", data=[result])
    except Deduction.DoesNotExist:
        return DeductionResponseSchema(status_code=404, success=False, message="Deduction not found", data=[])
    except Exception as e:
        return DeductionResponseSchema(status_code=404, success=False, message=str(e), data=[])


# update deduction
@deduction_router.put("/update/{id}", response=DeductionResponseSchema, description="Update deduction")
def update_deduction(request, id: uuid.UUID, deduction: DeductionCreateAndUpdateRequestSchema):
    try:
        # check if deduction category exists
        category_obj = Deduction.objects.get(type=deduction.type)
        data = deduction.data

        message = validate_deduction(data, category_obj.type)
        if message != "":
            return DeductionResponseSchema(status_code=400, success=False, message=message, data=[])

        data =  [t.dict() for t in data]
        for data in data:
            if "id" not in data or not data["id"]: # check if id is not in data or id is not valid
                data["id"] = str(uuid.uuid4())

        data =  [t.dict() for t in data]
        for index, existing_data in enumerate(category_obj.data):
            if existing_data['id'] == str(id):
                updated_data = {**existing_data, **data[0]}
                category_obj.data[index] = updated_data
                category_obj.save()
                result = serialize_deduction_single(category_obj)
                return DeductionResponseSchema(status_code=200, success=True, message="Deduction updated successfully", data=[result])
        return DeductionResponseSchema(status=False, status_code=404, message="Deduction not found on this category", data=[])
    except Deduction.DoesNotExist:
        return DeductionResponseSchema(status_code=404, success=False, message="Deduction not found", data=[])   
    except ValidationError as e:
        return DeductionResponseSchema(status_code=400, success=False, message=str(e), data=[])
    except Exception as e:
        return DeductionResponseSchema(status_code=500, success=False, message=str(e), data=[])


# delete deduction
@deduction_router.delete("/{category}/{id}", response=DeductionResponseSchema, description="Delete deduction")
def delete_deduction(request, category: str, id: uuid.UUID):
    try:
        deduction_obj = Deduction.objects.get(type=category)
        deduction_obj.data = [item for item in deduction_obj.data if item['id'] != str(id)]
        deduction_obj.save()
        result = serialize_deduction_single(deduction_obj)
        return DeductionResponseSchema(status_code=200, success=True, message="Deduction deleted successfully", data=[result])
    except Deduction.DoesNotExist:
        return DeductionResponseSchema(status_code=404, success=False, message="Deduction not found", data=[])
    except Exception as e:
        return DeductionResponseSchema(status_code=500, success=False, message=str(e), data=[])