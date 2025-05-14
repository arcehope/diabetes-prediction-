import streamlit as st
from datetime import datetime
from database import save_database

def admin_interface(doctor_database):
    st.title('Admin Dashboard')
    
    # Doctor Management Section
    st.header('Doctor Management')
    
    # Add New Doctor
    st.subheader('Add New Doctor')
    with st.form('add_doctor'):
        name = st.text_input('Doctor Name')
        specialization = st.text_input('Specialization')
        contact = st.text_input('Contact Number')
        start_time = st.time_input('Start Time', value=datetime.strptime('09:00', '%H:%M').time())
        end_time = st.time_input('End Time', value=datetime.strptime('17:00', '%H:%M').time())
        
        if st.form_submit_button('Add Doctor'):
            new_doctor = {
                "name": name,
                "specialization": specialization,
                "contact": contact,
                "available_hours": {
                    "start": start_time.strftime("%H:%M"),
                    "end": end_time.strftime("%H:%M")
                }
            }
            doctor_database["Diabetes"].append(new_doctor)
            save_database(doctor_database)  # Save immediately after adding
            st.success(f"Added Dr. {name} successfully!")

    # Remove/Edit Doctors
    st.subheader('Manage Existing Doctors')
    for i, doctor in enumerate(doctor_database["Diabetes"]):
        with st.expander(f"{doctor['name']} - {doctor['specialization']}"):
            st.write(f"Contact: {doctor['contact']}")
            st.write(f"Working Hours: {doctor['available_hours']['start']} - {doctor['available_hours']['end']}")
            
            # Edit working hours
            new_start = st.time_input(f'New Start Time for {doctor["name"]}', 
                                    value=datetime.strptime(doctor['available_hours']['start'], '%H:%M').time(),
                                    key=f'start_{i}')
            new_end = st.time_input(f'New End Time for {doctor["name"]}', 
                                  value=datetime.strptime(doctor['available_hours']['end'], '%H:%M').time(),
                                  key=f'end_{i}')
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Update Hours', key=f'update_{i}'):
                    doctor_database["Diabetes"][i]['available_hours']['start'] = new_start.strftime("%H:%M")
                    doctor_database["Diabetes"][i]['available_hours']['end'] = new_end.strftime("%H:%M")
                    st.success('Updated working hours successfully!')
            
            with col2:
                if st.button('Remove Doctor', key=f'remove_{i}'):
                    doctor_database["Diabetes"].pop(i)
                    save_database(doctor_database)  # Save immediately after removing
                    st.success(f"Removed {doctor['name']}")
                    st.rerun()