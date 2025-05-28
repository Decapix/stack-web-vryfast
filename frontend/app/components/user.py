import streamlit as st
import requests
import json
import os

# Get API URL from environment variable
API_URL = os.getenv("API_URL", "http://backend:8000")

def login(email, password):
    """Handle user login"""
    # Create a container for debug info that can be expanded/collapsed
    debug_container = st.expander("Debug Information", expanded=False)
    
    try:
        # First, check if API is accessible
        try:
            health_check = requests.get(f"{API_URL}/docs")
            debug_container.write(f"API connection: {'OK' if health_check.status_code < 400 else 'Failed'}")
        except Exception as e:
            debug_container.error(f"Cannot connect to API at {API_URL}: {e}")
        
        # Attempt login
        debug_container.write(f"Attempting login for {email}")
        response = requests.post(
            f"{API_URL}/auth/jwt/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Debug info
        debug_container.write(f"Status code: {response.status_code}")
        debug_container.write(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]
            debug_container.success("Token received successfully")
            
            # Get user info
            user_response = requests.get(
                f"{API_URL}/users/me",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            debug_container.write(f"User info status: {user_response.status_code}")
            
            if user_response.status_code == 200:
                st.session_state.user_info = user_response.json()
                st.session_state.authenticated = True
                debug_container.success("Authentication successful")
                return True
            else:
                debug_container.error(f"Failed to get user info: {user_response.text}")
        else:
            st.error("Authentication failed. Please check your credentials.")
        return False
    except Exception as e:
        debug_container.error(f"Login error: {e}")
        import traceback
        debug_container.code(traceback.format_exc())
        return False

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.token = None
    st.rerun()

def create_user(email, password, is_superuser=False):
    """Create a new user (admin only)"""
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            json={
                "email": email,
                "password": password,
                "is_superuser": is_superuser,
                "is_verified": True,
            },
        )
        if response.status_code == 201:
            st.success(f"User {email} created successfully!")
            return True
        else:
            st.error(f"Error creating user: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return False

def update_user_profile(email=None, password=None):
    """Update the current user's profile"""
    try:
        # Prepare update data
        update_data = {}
        
        # Update email if provided
        if email and email != st.session_state.user_info['email']:
            update_data["email"] = email
        
        # Update password if provided
        if password:
            update_data["password"] = password
        
        # Only send request if there's data to update
        if update_data:
            response = requests.patch(
                f"{API_URL}/users/me",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                json=update_data
            )
            
            if response.status_code == 200:
                # Update session state with new user info
                st.session_state.user_info = response.json()
                st.success("Profile updated successfully!")
                return True
            else:
                st.error(f"Failed to update profile: {response.text}")
                return False
        return True
    except Exception as e:
        st.error(f"Error updating profile: {e}")
        import traceback
        st.error(traceback.format_exc())
        return False

def login_ui():
    """Display login UI in sidebar"""
    with st.sidebar:
        if not st.session_state.authenticated:
            st.header("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="login_button"):
                if login(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        else:
            st.header(f"Welcome, {st.session_state.user_info['email']}")
            if st.button("Logout", key="logout_button"):
                logout()

def account_page():
    """My Account page"""
    st.title("My Account")
    
    # Display current user info
    st.subheader("Profile Information")
    
    # Create tabs for profile sections
    profile_tab, email_tab, password_tab = st.tabs(["Profile Overview", "Update Email", "Update Password"])
    
    with profile_tab:
        st.write(f"**Email**: {st.session_state.user_info['email']}")
        st.write(f"**User ID**: {st.session_state.user_info['id']}")
        st.write(f"**Admin Status**: {'Administrator' if st.session_state.user_info.get('is_superuser', False) else 'Regular User'}")
        st.write(f"**Account Status**: {'Active' if st.session_state.user_info.get('is_active', False) else 'Inactive'}")
        st.write(f"**Email Verified**: {'Yes' if st.session_state.user_info.get('is_verified', False) else 'No'}")
    
    # Update email section
    with email_tab:
        st.subheader("Update Email Address")
        current_email = st.session_state.user_info['email']
        new_email = st.text_input("New Email Address", value=current_email, key="new_email")
        
        if st.button("Update Email", key="update_email"):
            if not new_email or new_email == current_email:
                st.warning("Please enter a new email address")
            else:
                if update_user_profile(email=new_email):
                    st.success("Email updated successfully!")
    
    # Update password section
    with password_tab:
        st.subheader("Update Password")
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        password_requirements = """
        Password should:
        - Be at least 8 characters long
        - Include at least one uppercase letter
        - Include at least one number
        - Include at least one special character
        """
        st.info(password_requirements)
        
        if st.button("Update Password", key="update_password"):
            if not new_password:
                st.warning("Please enter a new password")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                if update_user_profile(password=new_password):
                    st.success("Password updated successfully!")

def user_management_page():
    """User Management page (admin only)"""
    st.title("User Management")
    
    # Only superusers can create new users
    if st.session_state.user_info.get("is_superuser", False):
        st.subheader("Create New User")
        new_email = st.text_input("New User Email", key="new_user_email")
        new_password = st.text_input("New User Password", type="password", key="new_user_password")
        is_admin = st.checkbox("Admin User", key="new_user_is_admin")
        
        if st.button("Create User", key="create_user"):
            if create_user(new_email, new_password, is_admin):
                st.success(f"User {new_email} created successfully!")
            else:
                st.error("Failed to create user")
    else:
        st.info("Only admin users can create new accounts")