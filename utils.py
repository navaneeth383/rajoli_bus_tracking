# utils.py
import random

# Dummy OTP store and location status (replace with real device APIs later)
otp_store = {}
device_status_store = {}

def is_admin_authenticated(username, password):
    return username == "rajolibus" and password == "tracking"

def send_otp(mobile):
    otp = str(random.randint(100000, 999999))
    otp_store[mobile] = otp
    # Simulate sending OTP (in real use, integrate with SMS API)
    print(f"[DEBUG] OTP for {mobile}: {otp}")
    return True

def verify_otp(mobile, user_input):
    return otp_store.get(mobile) == user_input

def get_location_status(mobile):
    # Simulate random ON/OFF if no real data
    return device_status_store.get(mobile, "OFF")

def get_current_location(mobile):
    # Simulated GPS coordinates for demo
    # You would integrate actual mobile GPS API here
    if get_location_status(mobile) == "ON":
        return 17.385044, 78.486671  # Hyderabad coordinates
    else:
        return None, None

# For testing - simulate turning on location
device_status_store["9876543210"] = "ON"
