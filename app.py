import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import requests
import json
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import uuid
import hashlib
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from PIL import Image

mau1 = Image.open("images/mau1.jpg")
mau2 = Image.open("images/mau2.jpeg")
mau3 = Image.open("images/mau3.jpg")
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Set page config
st.set_page_config(page_title="Mau Forest Reforestation", layout="wide")

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    color: #1e8449;
}
.stButton>button {
    background-color: #1e8449;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)


class Donation(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class ForumPost(Base):
    __tablename__ = 'forum_posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# User authentication
def authenticate(email, password):
    with get_session() as session:
        user = session.query(User).filter_by(email=email).first()
        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            return user
    return None


# User registration
def register_user(email, password, name):
    with get_session() as session:
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(email=email, password=hashed_password, name=name)
        session.add(new_user)
    return True


# CSRF token generation
def generate_csrf_token():
    return str(uuid.uuid4())


# Sidebar
st.sidebar.title("Navigation")

# User authentication in sidebar
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Register"])

    if auth_option == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = authenticate(email, password)
            if user:
                st.session_state.user = user
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Invalid credentials")
    else:
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        name = st.sidebar.text_input("Full Name")
        if st.sidebar.button("Register"):
            if register_user(email, password, name):
                st.sidebar.success("Registration successful! Please log in.")
            else:
                st.sidebar.error("Email already exists. Please use a different email.")
else:
    st.sidebar.write(f"Logged in as {st.session_state.user.name}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None

# Navigation
page = st.sidebar.radio("Go to", ["Home", "Statistics", "Donate", "Impact Calculator", "Community", "Newsletter"])

# Home Page
if page == "Home":
    st.title("Reforesting the Mau Forest Region in Kenya")

    col1, col2 = st.columns(2)

    with col1:
        st.image(mau1, caption="Mau Forest Region")

    with col2:
        st.markdown("<p class='big-font'>Help us restore the Mau Forest!</p>", unsafe_allow_html=True)
        st.write("The Mau Forest is crucial for Kenya's ecosystem and water supply.")
        st.button("Learn More")

# Statistics Page
elif page == "Statistics":
    st.title("Reforestation Statistics")

    with get_session() as session:
        donations = session.query(Donation).all()
        total_donations = sum(d.amount for d in donations)
        total_trees = int(total_donations / 10)  # Assuming each tree costs $10 to plant

    data = {
        'Year': [2018, 2019, 2020, 2021, 2022],
        'Trees Planted': [10000, 25000, 50000, 75000, total_trees]
    }
    df = pd.DataFrame(data)

    # Create chart
    fig = px.bar(df, x='Year', y='Trees Planted', title='Trees Planted per Year')
    st.plotly_chart(fig)

    # Create map
    m = folium.Map(location=[-0.3817, 35.2962], zoom_start=7)
    folium.Marker([-0.3817, 35.2962], tooltip="Mau Forest").add_to(m)
    folium_static(m)

# Donation Page
elif page == "Donate":
    st.title("Donate to Reforestation Efforts")

    if st.session_state.user:
        col1, col2 = st.columns(2)

        with col1:
            st.write("Your donation helps plant trees in the Mau Forest region.")
            amount = st.number_input("Donation Amount (KES)", min_value=100, value=1000)
            payment_method = st.selectbox("Payment Method", ["Card", "Mpesa"])

            # Generate CSRF token
            if "csrf_token" not in st.session_state:
                st.session_state.csrf_token = generate_csrf_token()

            if st.button("Donate Now"):
                # Paystack API endpoint
                url = "https://api.paystack.co/transaction/initialize"

                # Paystack secret key
                secret_key = os.getenv("PAYSTACK_SECRET_KEY")

                # Request headers
                headers = {
                    "Authorization": f"Bearer {secret_key}",
                    "Content-Type": "application/json"
                }

                # Request payload
                payload = {
                    "email": st.session_state.user.email,
                    "amount": amount * 100,  # Amount in kobo
                    "currency": "KES",
                    "channels": ["card", "mobile_money"],
                    "metadata": {
                        "payment_method": payment_method,
                        "csrf_token": st.session_state.csrf_token
                    }
                }

                # Make API request
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    response.raise_for_status()

                    # Extract payment URL from response
                    data = response.json()
                    payment_url = data['data']['authorization_url']

                    # Save donation to database
                    with get_session() as session:
                        new_donation = Donation(user_id=st.session_state.user.id, amount=amount)
                        session.add(new_donation)

                    # Redirect user to payment page
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={payment_url}">', unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    logging.error(f"Payment error: {str(e)}")
                    st.error("An error occurred while processing your payment. Please try again later.")

        with col2:
            st.image(mau2,
                     caption="Your donation makes a difference")
    else:
        st.info("Please log in to make a donation.")

# Impact Calculator
elif page == "Impact Calculator":
    st.title("Environmental Impact Calculator")

    trees_planted = st.number_input("Number of trees planted", min_value=1, value=10)
    years = st.number_input("Years of growth", min_value=1, value=5)

    # Simplified impact calculations (replace with more accurate models)
    co2_absorbed = trees_planted * years * 22  # kg of CO2
    oxygen_produced = trees_planted * years * 117  # kg of oxygen

    st.write(f"Estimated impact over {years} years:")
    st.write(f"CO2 absorbed: {co2_absorbed} kg")
    st.write(f"Oxygen produced: {oxygen_produced} kg")

# Community Forum
elif page == "Community":
    st.title("Community Forum")

    with get_session() as session:
        posts = session.query(ForumPost).order_by(ForumPost.date.desc()).all()

    for post in posts:
        st.write(f"**{post.user_id}** - {post.date}")
        st.write(post.content)
        st.write("---")

    if st.session_state.user:
        new_post = st.text_area("Share your thoughts")
        if st.button("Post"):
            with get_session() as session:
                new_forum_post = ForumPost(user_id=st.session_state.user.id, content=new_post)
                session.add(new_forum_post)
            st.success("Post added successfully!")
    else:
        st.info("Please log in to post in the forum.")

# Newsletter Signup
elif page == "Newsletter":
    st.title("Sign up for our Newsletter")

    email = st.text_input("Email Address")
    if st.button("Subscribe"):
        # Add email to newsletter list (implement actual subscription logic)
        st.success("Thank you for subscribing to our newsletter!")

# Footer
st.markdown("---")
st.write("© 2024 Mau Forest Reforestation Project")

# Add a custom favicon
st.markdown(
    f"""
    <link rel="shortcut icon" href="{mau3}">
    """,
    unsafe_allow_html=True,
)