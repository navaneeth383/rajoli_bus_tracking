import random

# Mock location database: Simulates enabled/disabled GPS
enabled_numbers = {"9876543210", "9988776655", "9123456789"}

# Simulated GPS check
def get_mock_location_status(phone_number: str) -> bool:
    return phone_number in enabled_numbers

# Simulated coordinates for testing
def get_mock_coordinates(phone_number: str):
    random.seed(phone_number)
    base_lat, base_lon = 17.385044, 78.486671  # Hyderabad coordinates
    return [base_lat + random.uniform(-0.01, 0.01), base_lon + random.uniform(-0.01, 0.01)]
