import streamlit as st

def login():
    with st.sidebar:
        st.title("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state["logged_in"] = True
                st.success("Successfully logged in!")
            else:
                st.error("Invalid username or password")

def sign_up():
    with st.sidebar:
        st.title("Sign Up")
        email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Create Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        if st.button("Create Account"):
            if new_password == confirm_password:
                st.success("Account created successfully! Please log in.")
                st.session_state["sign_up_complete"] = True
            else:
                st.error("Passwords do not match")

def login_or_sign_up():
    option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Login":
        login()
    elif option == "Sign Up":
        sign_up()

def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.success("Successfully logged out!")