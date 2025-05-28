import streamlit as st

def navigation():
    """Main navigation for the application"""
    
    # Only show navigation when user is authenticated
    if st.session_state.authenticated:
        st.sidebar.title("Navigation")
        
        # Create navigation menu
        options = ["Dashboard"]
        
        # Add user management option for admins
        if st.session_state.user_info.get("is_superuser", False):
            options.append("User Management")
            
        # Add My Account option for all users
        options.append("My Account")
        
        # Create the navigation selector
        selected = st.sidebar.radio("Go to", options)
        
        return selected
    
    return None