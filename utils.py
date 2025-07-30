import random
import time

# Mock state
enabled_numbers = {"9876543210", "9988776655", "9123456789"}
otp_store = {}

def get_mock_location_status(phone):
    return phone in enabled_numbers

def get_mock_coordinates(phone):
    random.seed(phone)
    base = (17.385044, 78.486671)
    return [base[0] + random.uniform(-0.02, 0.02), base[1] + random.uniform(-0.02, 0.02)]

# OTP simulation
def send_otp(phone):
    otp = str(random.randint(100000, 999999))
    otp_store[phone] = (otp, time.time())
    print(f"DEBUG OTP for {phone}: {otp}")  # For testing
    return otp

def verify_otp(phone, entered, sent):
    valid = otp_store.get(phone, (None,))[0] == entered
    return valid

# Real mobile GPS fetch (stub)
def fetch_real_mobile_coords(phone):
    # TODO: Replace with actual API call to your tracker backend/service
    # Return [lat, lon] or None if offline
    return None
