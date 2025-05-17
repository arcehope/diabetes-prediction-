import streamlit as st
from datetime import datetime, timedelta
import pickle
from appointment_database import load_appointments, save_appointments

def show_lifestyle_tips(disease):
    if disease == "Diabetes":
        st.subheader("Lifestyle Tips for Managing Diabetes:")
        st.write("""
        🥗 Diet Tips:
        - Eat a balanced diet rich in whole grains, lean proteins, and healthy fats
        - Control portion sizes
        - Limit sugary foods and drinks
        - Include plenty of vegetables and fruits
        
        💪 Exercise Tips:
        - Aim for 30 minutes of moderate exercise daily
        - Include both aerobic and strength training exercises
        - Take regular walking breaks during the day
        
        📊 Monitoring:
        - Check blood sugar levels regularly
        - Keep track of your meals and exercise
        - Monitor your weight
        
        🏥 General Health:
        - Take medications as prescribed
        - Get regular check-ups
        - Maintain good foot care
        - Get adequate sleep
        
        ⚠️ Lifestyle Changes:
        - Quit smoking if you smoke
        - Limit alcohol consumption
        - Manage stress through relaxation techniques
        - Stay hydrated
        """)

def check_appointment_conflict(doctor_name, new_date, new_time, existing_appointments):
    # Convert new_time to comparable format
    new_datetime = datetime.combine(new_date, new_time)
    
    # Check each existing appointment for conflicts
    for apt in existing_appointments:
        if apt['doctor'] == doctor_name:
            # Convert stored date and time strings to datetime objects
            apt_date = datetime.strptime(apt['date'], '%B %d, %Y')
            apt_time = datetime.strptime(apt['time'], '%I:%M %p').time()
            apt_datetime = datetime.combine(apt_date, apt_time)
            
            # If it's the same date, check time slots
            if apt_date.date() == new_date:
                # Convert times to minutes for easier comparison
                new_time_mins = new_time.hour * 60 + new_time.minute
                apt_time_mins = apt_time.hour * 60 + apt_time.minute
                
                # Check if appointments overlap (assuming 15-minute duration)
                if abs(new_time_mins - apt_time_mins) < 15:
                    return True
    return False

def book_appointment(doctor, date, time):
    # Load existing appointments
    appointments = load_appointments()
    
    # Check for conflicts
    if check_appointment_conflict(doctor['name'], date, time, appointments):
        st.error("❌ This time slot is already booked. Please select a different time.")
        return
    
    # Create appointment record
    appointment = {
        'patient': st.session_state.username,
        'doctor': doctor['name'],
        'specialization': doctor['specialization'],
        'date': date.strftime('%B %d, %Y'),
        'time': time.strftime('%I:%M %p'),
        'contact': doctor['contact'],
        'status': 'Scheduled'
    }
    
    # Add new appointment
    appointments.append(appointment)
    save_appointments(appointments)
    
    # Show success message as a popup
    st.balloons()
    st.success(f"✅ Appointment Booked Successfully!")
    
    # Display appointment details
    with st.container():
        st.markdown("### 📋 Appointment Details")
        st.markdown(f"""
        **Doctor:** {doctor['name']}
        **Specialization:** {doctor['specialization']}
        **Date:** {date.strftime('%B %d, %Y')}
        **Time:** {time.strftime('%I:%M %p')}
        **Contact:** {doctor['contact']}
        **Status:** Scheduled
        """)

def user_interface(diabetes_model, doctor_database):
    st.title('Diabetes Prediction using ML')
    
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
        
    with col2:
        Glucose = st.text_input('Glucose Level')
    
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    
    with col2:
        Insulin = st.text_input('Insulin Level')
    
    with col3:
        BMI = st.text_input('BMI value')
    
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    
    with col2:
        Age = st.text_input('Age of the Person')

    # code for Prediction
    diab_diagnosis = ''
    
    # creating a button for Prediction
    if st.button('Diabetes Test Result'):
        if not all([Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]):
            diab_diagnosis = "Please enter the missing data"
            st.session_state.diagnosis_made = False
            st.session_state.recommended_doctors = []
        else:
            try:
                input_data = [
                    float(Pregnancies or 0),
                    float(Glucose or 0),
                    float(BloodPressure or 0),
                    float(SkinThickness or 0),
                    float(Insulin or 0),
                    float(BMI or 0),
                    float(DiabetesPedigreeFunction or 0),
                    float(Age or 0)
                ]
                
                diab_prediction = diabetes_model.predict([input_data])
                
                if (diab_prediction[0] == 1):
                    diab_diagnosis = 'The person is diabetic'
                    st.session_state.diagnosis_made = True
                    st.session_state.recommended_doctors = doctor_database.get("Diabetes", [])
                else:
                    diab_diagnosis = 'The person is not diabetic'
                    st.session_state.diagnosis_made = False
                    st.session_state.recommended_doctors = []
                    
            except ValueError as e:
                diab_diagnosis = "Error: Please ensure all fields contain valid numbers"
            except Exception as e:
                diab_diagnosis = f"Error: {str(e)}"

        st.success(diab_diagnosis)

    # Display doctor recommendations and booking interface if diabetic
    if st.session_state.diagnosis_made and st.session_state.recommended_doctors:
        recommendation = "Recommended doctors:\n"
        for doctor in st.session_state.recommended_doctors:
            recommendation += f"- {doctor['name']}, {doctor['specialization']}, Contact: {doctor['contact']}\n"
        st.info(recommendation)
        show_lifestyle_tips("Diabetes")
        
        doctor_choice = st.selectbox("Select Doctor", 
                                   st.session_state.recommended_doctors, 
                                   format_func=lambda x: f"{x['name']} - {x['specialization']} ({x['available_hours']['start']} - {x['available_hours']['end']})")
        
        start_time = datetime.strptime(doctor_choice['available_hours']['start'], "%H:%M").time()
        end_time = datetime.strptime(doctor_choice['available_hours']['end'], "%H:%M").time()
        
        min_date = datetime.today()
        max_date = min_date + timedelta(days=30)
        date = st.date_input("Select Appointment Date", 
                           min_value=min_date,
                           max_value=max_date,
                           value=min_date)
        
        # Time selection defaulting to doctor's start time
        time = st.time_input("Select Appointment Time", 
                           value=start_time,
                           help=f"Choose a time between {doctor_choice['available_hours']['start']} and {doctor_choice['available_hours']['end']}")
        
        # Booking button
        if st.button("Book Appointment"):
            # Convert time to comparable format
            appointment_time = datetime.strptime(time.strftime("%H:%M"), "%H:%M").time()
            start = datetime.strptime(doctor_choice['available_hours']['start'], "%H:%M").time()
            end = datetime.strptime(doctor_choice['available_hours']['end'], "%H:%M").time()
            
            if start <= appointment_time <= end:
                book_appointment(doctor_choice, date, time)
            else:
                st.error(f"Please select a time between {doctor_choice['available_hours']['start']} and {doctor_choice['available_hours']['end']}")

        # Display appointment history
        if st.session_state.get('appointments'):
            st.markdown("---")
            st.markdown("### 📅 Your Appointment History")
            for idx, apt in enumerate(st.session_state.appointments, 1):
                with st.container():
                    st.markdown(f"""
                    **Appointment #{idx}**
                    - Doctor: {apt['doctor']}
                    - Specialization: {apt['specialization']}
                    - Date: {apt['date'].strftime('%B %d, %Y')}
                    - Time: {apt['time'].strftime('%I:%M %p')}
                    ---
                    """)

    # Display appointment history from database
    appointments = load_appointments()
    user_appointments = [apt for apt in appointments if apt.get('patient') == st.session_state.username]
    
    if user_appointments:
        st.markdown("---")
        st.markdown("### 📅 Your Appointment History")
        for idx, apt in enumerate(user_appointments, 1):
            with st.container():
                st.markdown(f"""
                **Appointment #{idx}**
                - Doctor: {apt['doctor']}
                - Specialization: {apt['specialization']}
                - Date: {apt['date']}
                - Time: {apt['time']}
                - Status: {apt.get('status', 'Scheduled')}
                ---
                """)