import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

# Set Streamlit page config
st.set_page_config(
    page_title="RoboRide Controller",
    page_icon="🚗",
    layout="centered",
)

st.title("RoboRide: Destination Selector")

st.markdown("Click on the map to choose the **Destination** point.")

with st.sidebar:
    st.header("🧭 RoboRide Guide")
    st.image("src/assets/images/smart_car_tesla.jpg")
    st.markdown("""
    1. **Click on the map** to select your destination.
    2. Choose your **Drive Mode**.
    3. Confirm and **Send** the destination to RoboRide.
    
    ---
    """)

# Session State
if "destination" not in st.session_state:
    st.session_state.destination = None
if "drive_mode" not in st.session_state:
    st.session_state.drive_mode = "Normal"

# Input for ngrok URL
ngrok_url = st.text_input("Enter ngrok URL",)

# Create folium map
m = folium.Map(location=[30.586241, 31.482737], zoom_start=15)

# Add destination marker if selected
if st.session_state.destination:
    folium.Marker(
        [st.session_state.destination['lat'], st.session_state.destination['lng']],
        tooltip="Destination",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Capture click and update session state
map_data = st_folium(m, height=600, width=800)

if map_data and map_data.get('last_clicked'):
    clicked_lat = map_data['last_clicked']['lat']
    clicked_lng = map_data['last_clicked']['lng']
    st.session_state.destination = {'lat': clicked_lat, 'lng': clicked_lng}

# Reset button
if st.sidebar.button("🔄 Reset Destination"):
    st.session_state.destination = None

# Drive mode selection
st.subheader("Choose Drive Mode")
st.session_state.drive_mode = st.selectbox(
    "Select a driving mode:",
    options=["Normal", "Sport", "Eco"],
    index=["Normal", "Sport", "Eco"].index(st.session_state.drive_mode)
)

# Form for confirmation and sending
with st.form(key="destination_form"):
    # Checkbox for confirmation
    confirm = st.checkbox("✅ Confirm sending destination and drive mode")
    
    # Submit button inside the form
    submit_button = st.form_submit_button(label="Confirm and Send Destination to RoboRide")

# If form is submitted and checkbox is confirmed
if submit_button:
    if st.session_state.destination:
        if confirm:
            with st.spinner("Sending data to RoboRide..."):
                data = {
                    "destination": st.session_state.destination,
                    "drive_mode": st.session_state.drive_mode
                }
                try:
                    # Using the ngrok URL provided by the user
                    raspberry_pi_url = f"{ngrok_url}/move"
                    response = requests.post(raspberry_pi_url, json=data, timeout=5)
                    st.success(f"Destination sent! Raspberry Pi responded: {response.text}")
                except Exception as e:
                    st.error(f"Failed to send destination: {e}")
        else:
            st.warning("Please confirm before sending.")
    else:
        st.warning("Please select a destination on the map before sending.")
