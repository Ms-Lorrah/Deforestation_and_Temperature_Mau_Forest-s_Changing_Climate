import streamlit as st
import folium
from streamlit_folium import st_folium

# Set page title
st.set_page_config(page_title="Kenya Forest Trust", page_icon="🌳")

# Set title with green font color
st.markdown("<h1 style='color: green;'>Kenya Forest Trust</h1>", unsafe_allow_html=True)

# Create dropdown placeholders
options = ["Home", "About Us", "Projects", "Donations/Support"]
selected_option = st.selectbox("Navigate", options)

# Function to create a map of Kenya with forest coverage
def create_map():
    # Initialize map centered on Kenya
    m = folium.Map(location=[0.0236, 37.9062], zoom_start=6)

    # Sample data: Coordinates of some forests in Kenya
    forests = [
        {"name": "Kakamega Forest", "location": [0.2827, 34.7519]},
        {"name": "Mau Forest", "location": [-0.5257, 35.6046]},
        {"name": "Aberdare Forest", "location": [-0.4167, 36.6833]},
        {"name": "Mt. Kenya Forest", "location": [0.1521, 37.3084]},
    ]

    # Add markers to the map
    for forest in forests:
        folium.Marker(location=forest["location"], popup=forest["name"]).add_to(m)

    return m

# Display content based on selection
if selected_option == "Home":
    st.write("Welcome to Kenya Forest Trust")
    st.write("Below is a map showing forest coverage in Kenya.")
    # Display the map
    map_object = create_map()
    st_folium(map_object, width=700, height=500)
    # Add additional text
    st.write("""
    Trees are essential to our ecosystem, providing oxygen, improving air quality, conserving water, and supporting wildlife. However, deforestation is causing severe consequences to our planet.

    Kenya Forest Fund by use Green A.I. aims to restore forest coverage and combat climate change through reforestation. Your donations help us buy and plant seedlings, allowing you to contribute to this vital cause from the comfort of your home, office, or social gathering. Join us in making a difference!
    """)
elif selected_option == "About Us":
    st.write("About Us section coming soon.")
elif selected_option == "Projects":
    st.write("Projects section coming soon.")
elif selected_option == "Donations/Support":
    st.write("Donations/Support section coming soon.")
# Add YouTube video
st.video("https://youtu.be/k7FOhuTy3RA?si=A1ZYWRdMyZ2TyMXY") 