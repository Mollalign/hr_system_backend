# ===============================================================
# ATTENDANCE UTILS
# ===============================================================
from datetime import datetime
# ===============================================================
# HARCODE FOR ATTENDANCE CHECK IN AND CHECK OUT
# ===============================================================
CHECK_IN_TIME = datetime.strptime("08:30:00", "%H:%M:%S").time()
CHECK_OUT_TIME = datetime.strptime("16:30:00", "%H:%M:%S").time()

# ===============================================================
# VALIDATION FOR ATTENDANCE
# ===============================================================
def check_in_status(data: datetime):
    if data > CHECK_IN_TIME:
        status = {
            "late_in": True,
            "on_time_in": False,
        }
    else:
        status = {
            "late_in": False,
            "on_time_in": True,
        }

    return status

def check_out_status(data: datetime):
    if data > CHECK_OUT_TIME:
        status = {
            "early_out": True,
            "on_time_out": False,
        }
    else:
        status = {
            "early_out": False,
            "on_time_out": True,
        }

    return status