import streamlit as st
import folium
from streamlit_folium import folium_static
import ee
import geemap

# Initialize Earth Engine
ee.Initialize()

# Sidebar
st.sidebar.title("Kenya Forest Trust")
st.sidebar.info("Support reforestation efforts by donating via Mpesa or PayPal.")

# Main Title
st.title("Kenya Forest Trust")

# Section 1: Importance of Trees
st.header("Why Trees Are Important")
st.write("""
Trees are vital to our ecosystem. They provide oxygen, improve air quality, conserve water, preserve soil, and support wildlife. 
Deforestation, the large-scale removal of trees, has severe consequences, including climate change, habitat destruction, 
loss of biodiversity, and soil erosion. Reforestation is necessary to restore these benefits, combat climate change, 
and protect our planet for future generations.
""")

# Section 2: Interactive Map
st.header("Interactive Map")

# Create a map centered on Kenya
Map = geemap.Map(center=[0.0236, 37.9062], zoom=6)

# Add geographical image of Kenya
kenya_image = ee.Image("LANDSAT/LC08/C01/T1_SR").select(['B4', 'B3', 'B2']).clip(ee.Geometry.Rectangle([33.501, -5.202, 41.885, 5.419]))
Map.addLayer(kenya_image, {'bands': ['B4', 'B3', 'B2'], 'min': 500, 'max': 15000}, "Kenya Geographical Image")

# Add deforestation layer (example)
deforestation = ee.Image("UMD/hansen/global_forest_change_2020_v1_8").select('loss')
Map.addLayer(deforestation, {"palette": "red"}, "Deforestation in Kenya")

# Show the map
folium_static(Map)

# Section 3: Types of Trees or Seedlings
st.header("Types of Trees or Seedlings to Choose From")
st.write("""
1. **Acacia** - Drought-resistant and good for soil fertility.
2. **Cedar** - Excellent for timber and windbreaks.
3. **Bamboo** - Fast-growing and good for erosion control.
4. **Neem** - Known for its medicinal properties and pest resistance.
5. **Moringa** - Highly nutritious and fast-growing.
""")

# Section 4: Donate
st.header("Support Reforestation")

# Mpesa Donation
st.markdown(
    """
    ### Donate via Mpesa
    <div style="display: flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/M-PESA_LOGO-01.png" alt="Mpesa" style="width: 50px; height: 50px; margin-right: 10px;">
        <span>Mpesa: Paybill 123456, Account: MauForest</span>
    </div>
    """,
    unsafe_allow_html=True
)

# PayPal Donation
st.markdown(
    """
    ### Donate via PayPal
    <div style="display: flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" alt="PayPal" style="width: 50px; height: 50px; margin-right: 10px;">
        <a href="https://www.paypal.com/donate?hosted_button_id=YOUR_BUTTON_ID">Donate via PayPal</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Donation Amounts
st.sidebar.title("Donate Now")
donation_amount = st.sidebar.selectbox(
    "Select Donation Amount",
    ["$30", "$50", "$100", "$500", "$1000", "Ksh. 200", "Ksh. 500", "Ksh. 1000", "Ksh. 5000", "Ksh. 10,000"]
)

st.sidebar.write(f"Thank you for your support! Your selected donation amount is {donation_amount}.")

# Run the Streamlit app
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Kenya Forest Trust")
