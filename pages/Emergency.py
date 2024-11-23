import streamlit as st
from geopy.geocoders import Nominatim
import requests
import folium
from streamlit_folium import st_folium

st.title("Locate Nearby Help")

# Load custom styles
try:
    with open('styles.css', "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom styles.css file not found. Using default styling.")

# Input location
location_input = st.text_input("Enter your location (City or Address):")

if location_input:
    with st.spinner("Processing your request... Please wait."):
        geolocator = Nominatim(user_agent="emergency-assistant")
        location = geolocator.geocode(location_input)
        
        if location:
            latitude, longitude = location.latitude, location.longitude
            st.subheader(f"Location found: {location.address}")
            st.subheader(f"Coordinates: {latitude}, {longitude}")
            
            # Google API request
            API_KEY = st.secrets["API_KEY"]
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=hospital&key={API_KEY}"
            response = requests.get(url).json()
            
            if "results" in response and response["results"]:
                st.success("Nearby Hospitals:")
                for place in response["results"]:
                    st.write(place["name"], "-", place.get("vicinity", "Address not available"))
                
                # Create map
                map = folium.Map(location=[latitude, longitude], zoom_start=13)
                for place in response["results"]:
                    hospital_name = place["name"]
                    hospital_lat = place["geometry"]["location"]["lat"]
                    hospital_lng = place["geometry"]["location"]["lng"]
                    folium.Marker([hospital_lat, hospital_lng], popup=hospital_name).add_to(map)
                
                st_folium(map, width=700, height=500)
            else:
                st.warning("No hospitals found nearby or an error occurred.")
        else:
            st.error("Could not find the location. Please try entering a valid city or address.")
