import streamlit as st

def dashboard_page():
    """Main dashboard page"""
    st.title('MEV Form Dashboard')
    
    # Dashboard content
    st.header("Welcome to the MEV Form admin interface")
    
    # Add some dashboard stats or content
    st.subheader("System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Users", value="1", delta=None)
        
    with col2:
        st.metric(label="Forms", value="0", delta=None)
    
    # Add more dashboard content as needed
    st.subheader("Recent Activity")
    st.info("No recent activity to display")