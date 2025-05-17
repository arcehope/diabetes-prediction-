import streamlit as st
from datetime import datetime
from database import save_database
from appointment_database import load_appointments, save_appointments

def admin_interface(doctor_database):
    st.title('Admin Dashboard')
    
    # Sidebar for navigation
    with st.sidebar:
        selected = st.radio(
            "Select Section",
            ["Doctor Management", "Appointment Management"]
        )
    
    if selected == "Doctor Management":
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
                        save_database(doctor_database)  # Add this line
                        st.success('Updated working hours successfully!')
                
                with col2:
                    if st.button('Remove Doctor', key=f'remove_{i}'):
                        doctor_database["Diabetes"].pop(i)
                        save_database(doctor_database)  # Save immediately after removing
                        st.success(f"Removed {doctor['name']}")
                        st.rerun()
    else:
        # Appointment Management Section
        st.header('Appointment Management')
        
        # Load appointments from database
        appointments = load_appointments()
        
        if appointments:
            for idx, apt in enumerate(appointments):
                with st.expander(f"Appointment #{idx + 1} - {apt['doctor']}"):
                    st.write(f"**Patient**: {apt.get('patient', 'Unknown')}")
                    st.write(f"**Doctor**: {apt['doctor']}")
                    st.write(f"**Specialization**: {apt['specialization']}")
                    st.write(f"**Date**: {apt['date']}")
                    st.write(f"**Time**: {apt['time']}")
                    st.write(f"**Contact**: {apt['contact']}")
                    st.write(f"**Status**: {apt.get('status', 'Scheduled')}")
                    
                    # Add status management
                    new_status = st.selectbox(
                        "Update Appointment Status",
                        ["Scheduled", "Completed", "Cancelled"],
                        index=["Scheduled", "Completed", "Cancelled"].index(apt.get('status', 'Scheduled')),
                        key=f"status_{idx}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update Status", key=f"update_status_{idx}"):
                            appointments[idx]['status'] = new_status
                            save_appointments(appointments)
                            st.success(f"Updated appointment status to {new_status}")
                    
                    with col2:
                        if st.button("Delete Appointment", key=f"delete_{idx}"):
                            appointments.pop(idx)
                            save_appointments(appointments)
                            st.success("Appointment deleted successfully")
                            st.rerun()
        else:
            st.info("No appointments found in the system.")