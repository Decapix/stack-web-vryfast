import streamlit as st
import os
from components import login_ui, navigation, dashboard_page, account_page, user_management_page

# Set page config
st.set_page_config(
    page_title="MEV Form Admin",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "token" not in st.session_state:
    st.session_state.token = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Display login UI in sidebar
login_ui()

# Main content
if st.session_state.authenticated:
    # Show navigation in sidebar and get selected page
    selected_page = navigation()
    
    if selected_page:
        st.session_state.current_page = selected_page
    
    # Display the selected page
    if st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "User Management":
        user_management_page()
    elif st.session_state.current_page == "My Account":
        account_page()
else:
    # Display welcome screen for non-authenticated users
    st.title('MEV Form Admin Interface')
    st.info('Please log in to access the admin interface')
    
    # Add some information about the application
    st.markdown("""
    ### Welcome to the MEV Form Administration System
    
    This interface allows administrators to:
    - Manage users and permissions
    - Create and edit forms
    - View submissions and reports
    
    Please log in using your administrator credentials to access the system.
    """)
