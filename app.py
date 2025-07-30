import streamlit as st
import folium
from streamlit_folium import st_folium
from utils import (
    get_mock_location_status,
    get_mock_coordinates,
    send_otp,
    verify_otp,
    fetch_real_mobile_coords,
)

# Page config
st.set_page_config(page_title="Bus Tracking", layout="wide")

# Drawer control
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False

# Toggle drawer
if st.button("☰ Menu"):
    st.session_state.drawer_open = not st.session_state.drawer_open

# Drawer content
if st.session_state.drawer_open:
    with st.sidebar:
        st.header("🔐 Login Panel")
        login_mode = st.radio("Login as:", ["Admin", "User"])

        if login_mode == "Admin":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login as Admin"):
                if username == "rajolibus" and password == "tracking":
                    st.session_state.is_admin = True
                    st.session_state.is_user = False
                    st.success("Admin logged in")
                else:
                    st.error("Admin credentials invalid")

        else:  # User OTP login
            phone_input = st.text_input("Your Mobile Number (+91...)")
            if st.button("Send OTP"):
                st.session_state.sent_otp = send_otp(phone_input)
                st.session_state.user_phone = phone_input
                st.success("OTP sent to your mobile number")
            otp_input = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if verify_otp(st.session_state.user_phone, otp_input, st.session_state.sent_otp):
                    st.session_state.is_user = True
                    st.session_state.is_admin = False
                    st.success("User login successful")
                else:
                    st.error("Invalid OTP")

# Title
st.markdown("<h2 style='text-align:center;'>Bus Tracking</h2>", unsafe_allow_html=True)

# Top-right credit
st.markdown(
    "<div style='text-align:right; font-weight:bold; color:#555;'>Developed by Rajoli Software Team</div>",
    unsafe_allow_html=True,
)

# Session state defaults
if "tracked_number" not in st.session_state:
    st.session_state.tracked_number = None

if "map_type" not in st.session_state:
    st.session_state.map_type = "Default"

# Admin panel actions
if st.session_state.get("is_admin"):
    st.sidebar.markdown("---")
    new_number = st.sidebar.text_input("Enter phone number to track (+91...)")
    st.sidebar.selectbox("Select Map Type", ["Default", "Terrain", "Satellite"], key="map_type")
    if st.sidebar.button("Update and Fetch Location"):
        st.session_state.tracked_number = new_number
        # optionally reset OTP/user flags
        st.session_state.is_user = False

# Determine what to show
phone = st.session_state.tracked_number

if phone:
    enabled = get_mock_location_status(phone)
    if enabled:
        coords = fetch_real_mobile_coords(phone) or get_mock_coordinates(phone)
        status = "✅ Location is ON"
        status_color = "green"
    else:
        coords = None
        status = "🔴 Location is OFF"
        status_color = "red"
else:
    coords = get_mock_coordinates("placeholder")
    status = None
    status_color = None

# Public view
if not st.session_state.get("is_admin"):
    st.markdown("---")
    if phone and not enabled:
        st.error("Admin needs to enable tracking for this device.")
    if not phone:
        st.info("Tracking not started. Random placeholder location shown.")
    if status:
        st.markdown(f"<h4 style='color:{status_color};'>{status}</h4>", unsafe_allow_html=True)

    m = folium.Map(location=coords, zoom_start=13)
    if st.session_state.map_type == "Terrain":
        folium.TileLayer("Stamen Terrain").add_to(m)
    elif st.session_state.map_type == "Satellite":
        folium.TileLayer("Esri.WorldImagery").add_to(m)
    else:
        folium.TileLayer("OpenStreetMap").add_to(m)

    folium.Marker(coords, tooltip=f"+91-{phone or '???'}").add_to(m)
    st_folium(m, width=900, height=500)

# Admin sees same but with extra info
if st.session_state.get("is_admin"):
    st.markdown("---")
    st.markdown(f"### Admin Tracking: +91-{phone}")
    if status:
        st.markdown(f"<h4 style='color:{status_color};'>{status}</h4>", unsafe_allow_html=True)
