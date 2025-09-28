from .schemas import TaxCreateAndUpdateRequestSchema, PensionCreateAndUpdateRequestSchema, OtherDeductionCreateAndUpdateRequestSchema
from ninja.errors import ValidationError

def validate_tax(data: list[dict]):
    errors = {}
    validated_items = []

    for index, item in enumerate(data):
        try:
            # Validate schema types (field existence + types)
            valid_data = TaxCreateAndUpdateRequestSchema(**item)

            # Name validation
            if not valid_data.name or valid_data.name.strip() == "":
                errors[f"{index}.name"] = "Name is required and must be a string"

            # Min salary validation
            if valid_data.min_salary < 0:
                errors[f"{index}.min_salary"] = "Minimum salary must be >= 0 and a number"

            # Max salary normalization
            if isinstance(valid_data.max_salary, str) and valid_data.max_salary.lower() in ["UNLIMITED"]:
                valid_data.max_salary = None

            # Max salary validation (only if it's a number)
            if valid_data.max_salary is not None:
                if not isinstance(valid_data.max_salary, (int, float)):
                    errors[f"{index}.max_salary"] = "Maximum salary must be a number or 'unlimited'"
                elif valid_data.max_salary <= 0:
                    errors[f"{index}.max_salary"] = "Maximum salary must be > 0"
                elif valid_data.max_salary < valid_data.min_salary:
                    errors[f"{index}.max_salary"] = "Maximum salary must be >= minimum salary"

            # Rate and deduction validation
            if valid_data.rate < 0:
                errors[f"{index}.rate"] = "Rate must be >= 0 and a number"
            if valid_data.deduction < 0:
                errors[f"{index}.deduction"] = "Deduction must be >= 0 and a number"

            validated_items.append(valid_data)

        except Exception as e:
            errors[f"the error at index {index}"] = str(e)

    if errors:
        raise ValidationError(errors)

    return validated_items

def validate_pension(data: list[dict]):
    errors = {}
    validated_items = []

    for index, item in enumerate(data):
        try:
            # Validate schema types (field existence + types)
            valid_data = PensionCreateAndUpdateRequestSchema(**item)

            if valid_data.percentage <= 0:
                errors[f"{index}.percentage"] = "Percentage must be greater than 0 and must be a number"

            validated_items.append(valid_data)

        except Exception as e:
            errors[f"the error at index {index}"] = str(e)

    if errors:
        raise ValidationError(errors)

    return validated_items

def validate_other_deduction(data: list[dict]):
    errors = {}
    validated_items = []    

    for index, item in enumerate(data):
        try:
            # Validate schema types (field existence + types)
            valid_data = OtherDeductionCreateAndUpdateRequestSchema(**item)

            # Business rules validation
            if not valid_data.name or valid_data.name.strip() == "":
                errors[f"{index}.name"] = "Name is required and must be a string"
            if valid_data.type not in ['percentage', 'fixed']:
                errors[f"{index}.type"] = "Type must be either percentage or fixed"
            if valid_data.type == 'percentage' and valid_data.percentage <= 0:
                errors[f"{index}.percentage"] = "Percentage must be greater than 0 and must be a number"
            if valid_data.type == 'fixed' and valid_data.amount <= 0:
                errors[f"{index}.amount"] = "Amount must be greater than 0 and must be a number"
            if valid_data.description.strip() == "":
                errors[f"{index}.description"] = "Description must be a string"

            validated_items.append(valid_data)

        except Exception as e:
            errors[f"the error at index {index}"] = str(e)

    if errors:
        raise ValidationError(errors)

    return validated_items

# validate for deduction
def validate_deduction(data: list[dict], type: str):

    message = ""

    if type == 'Tax':
        try:
            validated_data = validate_tax(data)
        except ValidationError as e:
            return str(e)
    elif type == 'Pension':
        try:
            validated_data = validate_pension(data)
        except ValidationError as e:
            return str(e)
    elif type == 'Other':
        try:
            validated_data = validate_other_deduction(data)
        except ValidationError as e:
            return str(e)

    return message

