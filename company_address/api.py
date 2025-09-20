from ninja import Router
from .schemas import (
    CompanyAddressDataSchema,
    CompanyAddressResponse,
    CompanyAddressResponseMessage,
    UpdateCompanyAddressRequest,
    CreateCompanyAddressRequest,
)
from typing import Union
from .models import CompanyAddress
from ninja.errors import ValidationError
import uuid


company_address_router = Router(tags=["Company address"])

# ===============================
# API ENDPOINTS FOR COMPANY ADDRESS
# ===============================
# CREATE COMPANY ADDRESS
@company_address_router.post("/", response=Union[CompanyAddressResponse, CompanyAddressResponseMessage],description="Create company address")
def create_company_address(request, company_address: CreateCompanyAddressRequest):
    try:
        # if company address already exists
        if CompanyAddress.objects.filter(branch_name=company_address.branch_name).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch name already exists use other name")
        
        if CompanyAddress.objects.filter(branch_phone=company_address.branch_phone).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch phone already exists use other phone")
        
        if CompanyAddress.objects.filter(branch_email=company_address.branch_email).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch email already exists use other email")
        
        if CompanyAddress.objects.filter(branch_address=company_address.branch_address).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch address already exists use other address")

        company_address_obj = CompanyAddress.objects.create(
            branch_name=company_address.branch_name,
            branch_phone=company_address.branch_phone,
            branch_email=company_address.branch_email,
            branch_address=company_address.branch_address,
            is_active=company_address.is_active
        )

        return CompanyAddressResponse(
            status_code=200,
            success=True,
            message="Company address created successfully",
            data=[CompanyAddressDataSchema(
                id=company_address_obj.id,
                branch_name=company_address_obj.branch_name,
                branch_phone=str(company_address_obj.branch_phone),
                branch_email=company_address_obj.branch_email,
                branch_address=company_address_obj.branch_address,
                is_active=company_address_obj.is_active
            )]
        )
    except ValidationError as e:
        return CompanyAddressResponseMessage(status_code=400, success=False, message=str(e))
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))


# GET ALL COMPANY ADDRESSES
@company_address_router.get("/", response=Union[CompanyAddressResponse, CompanyAddressResponseMessage],description="Get all company addresses")
def get_all_company_addresses(request):
    try:
        company_addresses = CompanyAddress.objects.filter(is_deleted=False)
        result = []
        for company_address in company_addresses:
            result.append(CompanyAddressDataSchema(
                id=company_address.id,
                branch_name=company_address.branch_name,
                branch_phone=str(company_address.branch_phone),
                branch_email=company_address.branch_email,
                branch_address=company_address.branch_address,
                is_active=company_address.is_active
                )
            )
        return CompanyAddressResponse(
            status_code=200,
            success=True,
            message="All Company addresses fetched successfully",
            data=result
        )
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))

# GET ALL ACTIVE COMPANY ADDRESSES
@company_address_router.get("/active", response=Union[CompanyAddressResponse, CompanyAddressResponseMessage],description="Get all active company addresses")
def get_all_active_company_addresses(request):
    try:
        company_addresses = CompanyAddress.objects.filter(is_active=True,is_deleted=False)
        result = []
        for company_address in company_addresses:
            result.append(CompanyAddressDataSchema(
                    id=company_address.id,
                    branch_name=company_address.branch_name,
                    branch_phone=str(company_address.branch_phone),
                    branch_email=company_address.branch_email,
                    branch_address=company_address.branch_address,
                    is_active=company_address.is_active
                )
            )
        
        return CompanyAddressResponse(
            status_code=200,
            success=True,
            message="Active Company addresses fetched successfully",
            data=result
        )
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))


# GET COMPANY ADDRESS BY ID
@company_address_router.get("/{id}", response=Union[CompanyAddressResponse, CompanyAddressResponseMessage],description="Get company address by id")
def get_company_address_by_id(request, id: uuid.UUID):
    try:
        company_address = CompanyAddress.objects.get(id=id, is_deleted=False)
        return CompanyAddressResponse(
            status_code=200,
            success=True,
            message="Company address fetched successfully",
            data=[CompanyAddressDataSchema(
                id=company_address.id,
                branch_name=company_address.branch_name,
                branch_phone=str(company_address.branch_phone),
                branch_email=company_address.branch_email,
                branch_address=company_address.branch_address,
                is_active=company_address.is_active
            )]
        )
    except CompanyAddress.DoesNotExist:
        return CompanyAddressResponseMessage(status_code=404, success=False, message="Company address not found")
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))    


# UPDATE COMPANY ADDRESS
@company_address_router.put("/{id}", response=Union[CompanyAddressResponse, CompanyAddressResponseMessage],description="Update company address")
def update_company_address(request, id: uuid.UUID, company_address: UpdateCompanyAddressRequest):
    try:
        company_address_obj = CompanyAddress.objects.get(id=id, is_deleted=False)
        # if company address already exists
        if CompanyAddress.objects.filter(branch_name=company_address.branch_name).exclude(id=id).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch name already exists use other name")
        
        if CompanyAddress.objects.filter(branch_phone=company_address.branch_phone).exclude(id=id).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch phone already exists use other phone")
        
        if CompanyAddress.objects.filter(branch_email=company_address.branch_email).exclude(id=id).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch email already exists use other email")
        
        if CompanyAddress.objects.filter(branch_address=company_address.branch_address).exclude(id=id).exists():
            return CompanyAddressResponseMessage(status_code=400, success=False, message="Company branch address already exists use other address")

        company_address_obj.branch_name = company_address.branch_name
        company_address_obj.branch_phone = company_address.branch_phone
        company_address_obj.branch_email = company_address.branch_email
        company_address_obj.branch_address = company_address.branch_address
        company_address_obj.is_active = company_address.is_active
        company_address_obj.save()

        return CompanyAddressResponse(
            status_code=200,
            success=True,
            message="Company address updated successfully",
            data=[CompanyAddressDataSchema(
                id=company_address_obj.id,
                branch_name=company_address_obj.branch_name,
                branch_phone=str(company_address_obj.branch_phone),
                branch_email=company_address_obj.branch_email,
                branch_address=company_address_obj.branch_address,
                is_active=company_address_obj.is_active
            )]
        )
    except ValidationError as e:
        return CompanyAddressResponseMessage(status_code=400, success=False, message=str(e))
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))

# DELETE COMPANY ADDRESS
@company_address_router.delete("/{id}", response=Union[CompanyAddressResponseMessage, CompanyAddressResponseMessage],description="Delete company address")
def delete_company_address(request, id: uuid.UUID):
    try:
        company_address = CompanyAddress.objects.get(id=id, is_deleted=False)
        company_address.is_deleted = True
        company_address.save()
        return CompanyAddressResponseMessage(status_code=200, success=True, message="Company address deleted successfully")
    except CompanyAddress.DoesNotExist:
        return CompanyAddressResponseMessage(status_code=404, success=False, message="Company address not found")
    except Exception as e:
        return CompanyAddressResponseMessage(status_code=500, success=False, message=str(e))