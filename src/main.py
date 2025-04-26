# map_input_streamlit.py
import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

st.title("RoboRide: Location Selector")

st.markdown("Click on the map to choose **Start** and **Destination** points.")

# Create empty session state
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# Create a folium map
m = folium.Map(location=[30.8269, 31.5987], zoom_start=15)    #30.826905,31.598732

# Add markers if already selected
if st.session_state.start:
    folium.Marker(
        [st.session_state.start['lat'], st.session_state.start['lng']],
        tooltip="Start",
        icon=folium.Icon(color='green')
).add_to(m)
if st.session_state.end:
    folium.Marker(
        [st.session_state.end['lat'], st.session_state.end['lng']],
        tooltip="End",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Capture map click
map_data = st_folium(m, width=700, height=500)

# Update session state with clicks
if map_data and map_data["last_clicked"]:
    if not st.session_state.start:
        st.session_state.start = map_data["last_clicked"]
    elif not st.session_state.end:
        st.session_state.end = map_data["last_clicked"]

# Display coordinates
if st.session_state.start:
    st.success(f"Start Location: {st.session_state.start}")
if st.session_state.end:
    st.success(f"Destination: {st.session_state.end}")

# Button to send coordinates
if st.session_state.start and st.session_state.end:
    if st.button("Send to RoboRide"):
        data = {
            "start": st.session_state.start,
            "end": st.session_state.end
        }
        try:
            # Replace this with your Raspberry Pi's IP
            raspberry_pi_url = "http://192.168.1.100:5000/move"
            response = requests.post(raspberry_pi_url, json=data)
            st.success(f"Data sent! Raspberry Pi responded: {response.text}")
        except Exception as e:
            st.error(f"Failed to send data: {e}")
