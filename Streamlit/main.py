import streamlit as st
import folium
from streamlit_folium import st_folium
from auth import login_or_sign_up, logout

# Set page title
st.set_page_config(page_title="Kenya Forest Trust", page_icon="🌳")

# Set title with green font color
st.markdown("<h1 style='color: green;'>Kenya Forest Trust</h1>", unsafe_allow_html=True)

# Create dropdown placeholders
options = ["Home", "About Us", "Projects", "Donations/Support", "Privacy Policy "]
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

    # Add PayPal donate button
    donate_button = """
    <form action="https://www.paypal.com/donate" method="post" target="_top">
    <input type="hidden" name="hosted_button_id" value="TCLMPEGDFYHQC" />
    <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
    <img alt="" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
    </form>
    """
    st.markdown(donate_button, unsafe_allow_html=True)

elif selected_option == "About Us":
    st.write("About Us section coming soon.")
elif selected_option == "Projects":
    st.write("Projects section coming soon.")
elif selected_option == "Donations/Support":
    st.write("Donations/Support section coming soon.")
elif selected_option == "Events":
    st.write("Events section coming soon.")
elif selected_option == "Privacy":
    st.write(""" We value your privacy and are committed to protecting your personal data. This privacy policy will inform you about how we look after your personal data when you visit our website or use our services, and tell you about your privacy rights and how the law protects you.

    **1. Important Information and Who We Are**

    This privacy policy aims to give you information on how Kenya Forest Trust collects and processes your personal data through your use of this website, including any data you may provide through this website when you sign up for our newsletter or make a donation.

    **2. The Data We Collect About You**

    We may collect, use, store and transfer different kinds of personal data about you which we have grouped together as follows:
    - Identity Data
    - Contact Data
    - Financial Data
    - Transaction Data
    - Technical Data
    - Profile Data
    - Usage Data
    - Marketing and Communications Data

    **3. How We Use Your Personal Data**

    We will only use your personal data when the law allows us to.

    **4. Disclosures of Your Personal Data**

    We may share your personal data with the parties set out below for the purposes set out in this policy.
    - Service providers who provide IT and system administration services.
    - Professional advisers including lawyers, bankers, auditors and insurers.
    - Government bodies that require us to report processing activities.

    **5. Data Security**

    We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed.

    **6. Your Legal Rights**

    Under certain circumstances, you have rights under data protection laws in relation to your personal data. These include the right to request access, correction, erasure, restriction, transfer, and to object to processing.

    **7. Contact Us**

    If you have any questions about this privacy policy or our privacy practices, please contact us at: privacy@kenyaforesttrust.org.
    """)

    def main():
     if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

if st.session_state['logged_in']:
        logout()
else:
        login_or_sign_up()
# Add YouTube video
st.video("https://youtu.be/k7FOhuTy3RA?si=A1ZYWRdMyZ2TyMXY")