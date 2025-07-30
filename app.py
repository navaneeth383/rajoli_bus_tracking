import streamlit as st
from streamlit_folium import st_folium
import folium
from utils import get_mock_location_status, get_mock_coordinates

# -------------------- Config -------------------- #
st.set_page_config(page_title="Rajoli Bus Tracker", layout="wide")

# -------------------- UI: Top Bar -------------------- #
st.markdown(
    "<div style='text-align:right; font-weight:bold; color:#555;'>Developed by Rajoli Software Team</div>",
    unsafe_allow_html=True,
)

st.title("📍 Phone Location Tracker for Bus Service")

# -------------------- Session State -------------------- #
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "tracked_number" not in st.session_state:
    st.session_state.tracked_number = None

# -------------------- Sidebar (Admin Login) -------------------- #
with st.sidebar:
    st.header("🔐 Admin Panel")
    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "rajolibus" and password == "tracking":
                st.session_state.authenticated = True
                st.success("Login successful")
            else:
                st.error("Invalid credentials")
    else:
        st.success("Logged in as Admin ✅")
        st.markdown("---")
        phone_input = st.text_input("📱 Enter phone number to track (India only)", max_chars=10)
        map_type = st.selectbox("🗺 Select Map View", ["Default", "Terrain", "Satellite"])

        if st.button("Update Number for Tracking Status"):
            st.session_state.tracked_number = phone_input

# -------------------- Logic to Display Location -------------------- #
phone = st.session_state.tracked_number
if phone:
    is_enabled = get_mock_location_status(phone)  # Simulated GPS status

    if is_enabled:
        st.markdown("### ✅ Location is ON")
        st.markdown(f"Tracking Phone Number: **+91-{phone}**")
        coords = get_mock_coordinates(phone)

        map_obj = folium.Map(location=coords, zoom_start=14)

        if map_type == "Terrain":
            folium.TileLayer('Stamen Terrain').add_to(map_obj)
        elif map_type == "Satellite":
            folium.TileLayer('Esri.WorldImagery').add_to(map_obj)
        else:
            folium.TileLayer('OpenStreetMap').add_to(map_obj)

        folium.Marker(location=coords, popup=f"+91-{phone}", tooltip="Current Location",
                      icon=folium.Icon(color='green', icon='bus', prefix='fa')).add_to(map_obj)

        st_data = st_folium(map_obj, width=1000, height=500)
    else:
        st.error("📴 Location is OFF (Red)")
        st.warning("Please enable the phone's location service to track it.")
else:
    st.info("🔍 Enter a phone number in the admin panel to start tracking.")
