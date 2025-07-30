import streamlit as st
import folium
from streamlit_folium import folium_static

# Mock data for demo
tracked_number = "9876543210"
location_enabled = True
phone_location = (17.385044, 78.486671)  # Default coordinates (e.g., Hyderabad)

# --- UI Setup ---
st.set_page_config(layout="wide")
st.markdown("<h3 style='text-align: right; color: gray;'>Developed by Rajoli Software Team</h3>", unsafe_allow_html=True)

# --- Sidebar login ---
st.sidebar.title("Admin Login")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

with st.sidebar:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "rajolibus" and password == "tracking":
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# --- Main View ---
st.title("📍 Phone Location Tracker")

if location_enabled:
    color_status = "green"
    status_text = "Location is ON"
else:
    color_status = "red"
    status_text = "Location is OFF"

st.markdown(f"<p style='color:{color_status};font-size:20px;'><strong>{status_text}</strong></p>", unsafe_allow_html=True)

if not location_enabled:
    st.warning("Location tracking is disabled for this phone. Please enable location services.")
else:
    # Show map with location
    m = folium.Map(location=phone_location, zoom_start=15)
    folium.Marker(phone_location, popup=f"Tracked Number: {tracked_number}").add_to(m)
    folium_static(m)

# --- Admin Panel ---
if st.session_state.authenticated:
    st.subheader("🔒 Admin Panel")
    new_number = st.text_input("Enter new number to track", value=tracked_number)
    enable = st.checkbox("Enable location tracking", value=location_enabled)
    update_btn = st.button("Update Number and Tracking Status")

    if update_btn:
        # Here you can add actual logic to update DB / file / API
        st.success(f"Tracking updated for: {new_number}")
        st.info(f"Tracking status set to: {'ON' if enable else 'OFF'}")

    st.caption("Note: OTP verification not implemented in this version.")
