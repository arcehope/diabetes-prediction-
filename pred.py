import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# loading the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           icons=['activity','heart','person'],
                           default_index=0)

# Example doctor database
doctor_database = {
    "Diabetes": [
        {"name": "Dr. Anshu Malli", "specialization": "Endocrinologist", "contact": "+977-9801234567"},
        {"name": "Dr. Bishnu Prasad", "specialization": "Diabetologist", "contact": "+977-9812345678"},
        {"name": "Dr. Meera Thapa", "specialization": "Internal Medicine Specialist", "contact": "+977-9841122334"},
        {"name": "Dr. Sita Ghimire", "specialization": "Endocrinologist", "contact": "+977-9807654321"},
        {"name": "Dr. Niraj Sharma", "specialization": "Diabetes Specialist", "contact": "+977-9865432109"}
    ],
    "Heart Disease": [
        {"name": "Dr. Anil K.C.", "specialization": "Cardiologist", "contact": "+977-9810123456"},
        {"name": "Dr. Uma Bhandari", "specialization": "Heart Specialist", "contact": "+977-9801234567"},
        {"name": "Dr. Binod Dahal", "specialization": "Cardiac Surgeon", "contact": "+977-9841234567"},
        {"name": "Dr. Rajendra Pokhrel", "specialization": "Cardiologist", "contact": "+977-9805432167"},
        {"name": "Dr. Sushma Aryal", "specialization": "Interventional Cardiologist", "contact": "+977-9823456710"}
    ],
    "Parkinsons": [
        {"name": "Dr. Ramesh Adhikari", "specialization": "Neurologist", "contact": "+977-9851234567"},
        {"name": "Dr. Pramila Joshi", "specialization": "Movement Disorder Specialist", "contact": "+977-9801122334"},
        {"name": "Dr. Sunita Karki", "specialization": "Neurologist", "contact": "+977-9812349876"},
        {"name": "Dr. Krishna Lamichhane", "specialization": "Parkinson’s Disease Specialist", "contact": "+977-9809876543"},
        {"name": "Dr. Bharat Regmi", "specialization": "Neurology Consultant", "contact": "+977-9843123456"}
    ]
}

def show_lifestyle_tips(disease):
    if disease == "Diabetes":
        st.subheader("Lifestyle Tips for Managing Diabetes:")
        st.write("""
            - Eat a healthy, balanced diet, rich in vegetables, fruits, and whole grains.
            - Stay active by exercising regularly (30 minutes of walking a day).
            - Monitor your blood sugar levels regularly.
            - Avoid smoking and limit alcohol consumption.
            - Keep a healthy weight and consult a dietitian.
        """)
    elif disease == "Heart Disease":
        st.subheader("Lifestyle Tips for Preventing Heart Disease:")
        st.write("""
            - Eat a heart-healthy diet (low in saturated fats and cholesterol).
            - Get regular exercise (30 minutes of cardio at least 5 days a week).
            - Quit smoking and avoid excessive alcohol consumption.
            - Manage stress through relaxation techniques.
            - Monitor your cholesterol and blood pressure regularly.
        """)
    elif disease == "Parkinson's":
        st.subheader("Lifestyle Tips for Managing Parkinson's Disease:")
        st.write("""
            - Exercise regularly to improve mobility and balance.
            - Eat a balanced diet, including plenty of fiber to prevent constipation.
            - Join a support group for emotional support and motivation.
            - Take medications as prescribed and follow up with your doctor.
            - Engage in activities that stimulate your mind (e.g., reading, puzzles).
        """)
        
        # Function for Booking Appointment
def book_appointment(doctor, date, time):
    # Placeholder for actual booking logic (e.g., storing data in a database or sending a notification)
    st.success(f"Your appointment with {doctor['name']} on {date} at {time} has been booked successfully!")
# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    # page title
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
    recommendation = ''

    # creating a button for Prediction
    if st.button('Diabetes Test Result'):
        try:
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            
            if (diab_prediction[0] == 1):
                diab_diagnosis = 'The person is diabetic'
               
                
                # Recommendation logic
                recommended_doctors = doctor_database.get("Diabetes", [])
                if recommended_doctors:
                    recommendation = "Recommended doctors:\n"
                    for doctor in recommended_doctors:
                        recommendation += f"- {doctor['name']}, {doctor['specialization']}, Contact: {doctor['contact']}\n"
                        
               
            else:
                diab_diagnosis = 'The person is not diabetic'
                
                
                
        except Exception as e:
            diab_diagnosis = f"Error: {e}"

    st.success(diab_diagnosis)
    if recommendation:
        st.info(recommendation)
        show_lifestyle_tips("Diabetes")
         # Allowing user to select doctor
        doctor_choice = st.selectbox("Select Doctor", recommended_doctors, format_func=lambda x: f"{x['name']} - {x['specialization']}")
        date = st.date_input("Select Appointment Date", min_value=datetime.today())
        time = st.time_input("Select Appointment Time", value=datetime.now().time())

        # Booking button
        if st.button("Book Appointment"):
         book_appointment(doctor_choice, date, time)
        
# Additional Features



# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''
    recommendation = ''

    # creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if (heart_prediction[0] == 1):
            heart_diagnosis = 'The person is having heart disease'
            # Recommendation logic
            recommended_doctors = doctor_database.get("Heart Disease", [])
            if recommended_doctors:
                recommendation = "Recommended doctors:\n"
                for doctor in recommended_doctors:
                    recommendation += f"- {doctor['name']}, {doctor['specialization']}, Contact: {doctor['contact']}\n"
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)
    if recommendation:
        st.info(recommendation)

# Parkinson's Prediction Page
if (selected == "Parkinsons Prediction"):
    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    park_diagnosis = ''
    recommendation = ''

    # creating a button for Prediction
    if st.button("Parkinson's Test Result"):
        park_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])

        if (park_prediction[0] == 1):
            park_diagnosis = "The person has Parkinson's disease"
            # Recommendation logic
            recommended_doctors = doctor_database.get("Parkinsons", [])
            if recommended_doctors:
                recommendation = "Recommended doctors:\n"
                for doctor in recommended_doctors:
                    recommendation += f"- {doctor['name']}, {doctor['specialization']}, Contact: {doctor['contact']}\n"
        else:
            park_diagnosis = "The person doesn't have Parkinson's disease"

    st.success(park_diagnosis)
    if recommendation:
        st.info(recommendation)
