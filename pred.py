import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
from database import load_database, save_database

# Initialize session states with cookie persistence
if 'logged_in' not in st.session_state:
    # Try to get login state from cookie
    st.session_state.logged_in = st.session_state.get('_login_cookie', False)
if 'user_role' not in st.session_state:
    st.session_state.user_role = st.session_state.get('_role_cookie', None)
if 'username' not in st.session_state:
    st.session_state.username = st.session_state.get('_username_cookie', None)
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'recommended_doctors' not in st.session_state:
    st.session_state.recommended_doctors = []
if 'diagnosis_made' not in st.session_state:
    st.session_state.diagnosis_made = False

# Login credentials with roles
USERS = {
    'admin': {'password': 'password123', 'role': 'admin'},
    'user': {'password': 'password456', 'role': 'user'}
}

# Load doctor database from file
doctor_database = load_database()

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username in USERS and USERS[username]['password'] == password:
            # Set session state
            st.session_state.logged_in = True
            st.session_state.user_role = USERS[username]['role']
            st.session_state.username = username
            
            # Set cookies for persistence
            st.session_state['_login_cookie'] = True
            st.session_state['_role_cookie'] = USERS[username]['role']
            st.session_state['_username_cookie'] = username
            
            st.success('Logged in successfully!')
            st.rerun()
        else:
            st.error('Invalid username or password')

# Main application
if not st.session_state.logged_in:
    login()
else:
    # loading the saved models
    try:
        diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
    except FileNotFoundError:
        st.error("Error: Could not find the model file 'diabetes_model.sav'. Please ensure it exists in the correct location.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()

    # Add logout button in sidebar
    with st.sidebar:
        if st.button('Logout'):
            # Clear session state and cookies
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.username = None
            # Clear cookies
            st.session_state['_login_cookie'] = False
            st.session_state['_role_cookie'] = None
            st.session_state['_username_cookie'] = None
            st.rerun()
        
        if st.session_state.user_role == 'admin':
            selected = option_menu('Admin Dashboard',
                               ['Doctor Management'],
                               icons=['hospital'],
                               default_index=0)
        else:
            selected = option_menu('Diabetes Prediction',
                               ['Diabetes Prediction'],
                               icons=['activity'],
                               default_index=0)

    # Route to appropriate interface
    if st.session_state.user_role == 'admin':
        from admin import admin_interface
        admin_interface(doctor_database)
        save_database(doctor_database)  # Save after admin makes changes
    else:
        from user import user_interface, show_lifestyle_tips, book_appointment
        user_interface(diabetes_model, doctor_database)  # Pass the model and database as parameters

def book_appointment(doctor, date, time):
    # Create appointment record
    appointment = {
        'doctor': doctor['name'],
        'specialization': doctor['specialization'],
        'date': date,
        'time': time,
        'contact': doctor['contact']
    }
    
    # Add to session state
    if 'appointments' not in st.session_state:
        st.session_state.appointments = []
    st.session_state.appointments.append(appointment)
    
    # Show success message as a popup
    st.balloons()  # Add celebratory balloons animation
    st.success(f"✅ Appointment Booked Successfully!")
    
    # Display appointment details in a highlighted box
    with st.container():
        st.markdown("### 📋 Appointment Details")
        st.markdown(f"""
        **Doctor:** {doctor['name']}
        **Specialization:** {doctor['specialization']}
        **Date:** {date.strftime('%B %d, %Y')}
        **Time:** {time.strftime('%I:%M %p')}
        **Contact:** {doctor['contact']}
        """)
