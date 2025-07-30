import random

# Dummy OTP storage
otp_store = {}

def send_otp(mobile_number):
    otp = "1234"  # Simulate OTP
    otp_store[mobile_number] = otp
    print(f"OTP sent to {mobile_number}: {otp}")
    return True

def verify_otp(mobile_number, otp_input):
    return otp_store.get(mobile_number) == otp_input

def get_location_from_device(mobile_number):
    # Simulate real GPS fetch based on mobile number
    # In actual app, call the mobile app API endpoint
    location_enabled = random.choice([True, False])  # Simulated toggle
    if location_enabled:
        return (17.385, 78.4867, True)  # (lat, lon, location_status)
    else:
        return (None, None, False)
