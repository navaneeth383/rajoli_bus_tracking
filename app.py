import streamlit as st
import random
from utils import (
    send_otp, verify_otp, get_location_from_device
)
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Bus Tracking", layout="wide")

# --- HEADER ---
st.markdown("""
    <style>
    .css-18e3th9 {padding-top: 0rem;}
    .css-1dp5vir {padding-top: 2rem;}
    .top-right {
        position: fixed;
        top: 10px;
        right: 20px;
        font-weight: bold;
        font-size: 16px;
        color: #555;
    }
    </style>
    <div class="top-right">Developed by Rajoli Software Team</div>
""", unsafe_allow_html=True)

st.title("🚌 Bus Tracking")

# --- SESSION STATE ---
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'mobile_number' not in st.session_state:
    st.session_state.mobile_number = None
if 'location_data' not in st.session_state:
    st.session_state.location_data = None

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("🔐 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if username == "rajolibus" and password == "tracking":
        st.success("Login Successful")

        mobile_number = st.text_input("Enter mobile number (India only)", max_chars=10)
        if st.button("Send OTP"):
            if len(mobile_number) == 10:
                st.session_state.otp_sent = send_otp(mobile_number)
                st.session_state.mobile_number = mobile_number
                st.success("OTP sent successfully")
            else:
                st.error("Enter valid 10-digit mobile number")

        if st.session_state.otp_sent:
            otp = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if verify_otp(mobile_number, otp):
                    st.session_state.authenticated = True
                    st.success("OTP Verified!")
                    loc = get_location_from_device(mobile_number)
                    st.session_state.location_data = loc
                else:
                    st.error("Invalid OTP")

        if st.session_state.authenticated:
            st.info(f"Tracking: {mobile_number}")
            if st.session_state.location_data:
                st.success("Real-time location updated.")
            else:
                st.error("Unable to fetch location. Please enable location on the device.")

# --- MAP SECTION (PUBLIC VIEW) ---
st.divider()
st.subheader("🗺️ Live Bus Location")

map_type = st.selectbox("Choose map type", ["Default", "Satellite", "Terrain"])

# If location exists
if st.session_state.location_data:
    lat, lon, status = st.session_state.location_data
    color = "green" if status else "red"
    status_text = "Location is ON" if status else "Location is OFF"
    st.markdown(f"**Status:** :{color}[{status_text}]")

    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup="Bus Location", tooltip="Bus", icon=folium.Icon(color=color)).add_to(m)
else:
    # No updated location yet
    lat, lon = random.uniform(12.5, 22.5), random.uniform(75, 85)
    st.warning("Admin needs to update location.")
    m = folium.Map(location=[lat, lon], zoom_start=6)

# Apply selected map tile
tile_layer = {
    "Default": "OpenStreetMap",
    "Satellite": "Stamen Terrain",
    "Terrain": "Stamen Toner"
}
folium.TileLayer(tile_layer[map_type]).add_to(m)
st_folium(m, width=700, height=500)
