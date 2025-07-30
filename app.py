import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import folium
from utils import (
    is_admin_authenticated,
    get_location_status,
    get_current_location,
    send_otp,
    verify_otp
)

st.set_page_config(page_title="Bus Tracking", layout="wide")

# --- Header ---
st.markdown("""
    <div style='text-align: right; font-size: 16px; color: #555;'>
        Developed by <strong>Rajoli Software Team</strong>
    </div>
    <h1 style='text-align: center;'>Bus Tracking</h1>
""", unsafe_allow_html=True)

# --- Sidebar for Admin Login ---
with st.sidebar:
    selected = option_menu(
        menu_title="Menu", options=["Admin Login"],
        icons=["lock-fill"], menu_icon="list", default_index=0
    )

admin_logged_in = False
if selected == "Admin Login":
    with st.form("admin_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted and is_admin_authenticated(username, password):
        st.success("Logged in successfully as admin.")
        admin_logged_in = True
    elif submitted:
        st.error("Invalid credentials.")

if "mobile_number" not in st.session_state:
    st.session_state.mobile_number = None

# --- Admin Panel ---
if admin_logged_in:
    st.subheader("Update Mobile Number to Track")
    phone = st.text_input("Enter 10-digit Indian Mobile Number")
    if st.button("Send OTP"):
        if send_otp(phone):
            st.success("OTP sent.")
        else:
            st.error("Failed to send OTP.")
    otp_input = st.text_input("Enter OTP")
    if st.button("Verify OTP and Update"):
        if verify_otp(phone, otp_input):
            st.session_state.mobile_number = phone
            st.success("Tracking number updated.")
        else:
            st.error("Incorrect OTP.")

# --- Public View ---
st.markdown("---")
if not st.session_state.mobile_number:
    st.warning("Admin has not updated a tracking number yet.")
else:
    location_status = get_location_status(st.session_state.mobile_number)
    if location_status == "OFF":
        st.error("Location is OFF for the tracked mobile. Please ask user to enable it.")
    elif location_status == "ON":
        lat, lon = get_current_location(st.session_state.mobile_number)
        map_type = st.selectbox("Choose Map View", ["Default", "Terrain", "Satellite"])
        tiles = {
            "Default": "OpenStreetMap",
            "Terrain": "Stamen Terrain",
            "Satellite": "Stamen Toner"
        }.get(map_type, "OpenStreetMap")
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles=tiles)
        folium.Marker([lat, lon], tooltip="Bus Location", icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.warning("Unable to fetch GPS status.")
