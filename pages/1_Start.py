# ==========================================
# Health Tracker - Streamlit Version
# Pages 1 and 2
# ==========================================

import streamlit as st


# ==========================================
# Session State Initialization
# This keeps data saved while app runs
# ==========================================

if "account_created" not in st.session_state:
    st.session_state.account_created = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {}


# ==========================================
# Validation Functions
# ==========================================

def is_valid_name(name):
    """Check if name is valid"""
    
    if name.strip() == "":
        return False
    
    # must contain at least one letter
    for char in name:
        if char.isalpha():
            return True
    
    return False


def is_valid_email(email):
    """Check if email contains @"""
    
    return email != "" and "@" in email and len(email) >= 3


def is_valid_password(password):
    """Password must be at least 6 characters"""
    
    return len(password) >= 6


def is_valid_age(age):
    """Age must be between 5 and 120"""
    
    return age >= 5 and age <= 120


# ==========================================
# PAGE 1 + PAGE 2 : Create Account Page
# ==========================================

if st.session_state.account_created == False:

    st.title("Health Tracker")

    st.subheader("Create Your Account")


    # Input fields
    name_input = st.text_input("Name")

    email_input = st.text_input("Email")

    password_input = st.text_input("Password", type="password")

    age_input = st.number_input(
        "Age",
        min_value=5,
        max_value=120,
        step=1
    )

    gender_input = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )


    # Create button
    if st.button("Create Account"):

        # Validation checks
        
        if not is_valid_name(name_input):
            st.error("Please enter a valid name.")

        elif not is_valid_email(email_input):
            st.error("Email must contain '@'.")

        elif not is_valid_password(password_input):
            st.error("Password must be at least 6 characters.")

        elif not is_valid_age(age_input):
            st.error("Invalid age.")

        else:
            # Save user data
            
            st.session_state.user_data = {
                "name": name_input,
                "email": email_input,
                "password": password_input,
                "age": age_input,
                "gender": gender_input
            }

            st.session_state.account_created = True

            st.success("Account created successfully!")

            st.rerun()


# ==========================================
# PAGE 3 : Dashboard (Preview)
# ==========================================

else:

    # حفظ البيانات في session_state بشكل منفصل
    st.session_state.user_name = st.session_state.user_data["name"]
    st.session_state.age = st.session_state.user_data["age"]
    st.session_state.gender = st.session_state.user_data["gender"]

    # الانتقال للصفحة الرئيسية
    st.switch_page("Main.py")

    # Logout button
    if st.button("Logout"):

        st.session_state.account_created = False
        st.session_state.user_data = {}

        st.rerun()