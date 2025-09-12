# ===============================================================
# VALIDATION FOR ALLOWANCE
# ===============================================================
from .models import Allowance

def validate_allowance(data: dict):
    message = ""
    
    # check if allowance already exists
    if Allowance.objects.filter(name=data['name'], is_deleted=False).exists():
        message = "Allowance already exists"
        return message
    
    # check if allowance type is valid
    if data['type'] not in ['percentage', 'fixed']:
        message = "Invalid allowance type"
        return message
    
    # check if percentage is valid
    if data['type'] == 'percentage' and (data['percentage'] is None or data['percentage'] <= 0):
        message = "Percentage is required"
        return message
    
    # check if amount is valid
    if data['type'] == 'fixed' and (data['amount'] is None or data['amount'] <= 0):
        message = "Amount is required"
        return message

    return message
