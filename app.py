from datetime import datetime

import firebase_admin
import pandas as pd
import streamlit as st
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate(
        "eliana-sistema-firebase-adminsdk-o60ey-8c6863f3f0.json"
    )
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Function to save patient data to a file
def save_patient_data(name, email, address):
    # # Load existing data or create a new DataFrame
    # try:
    #     df = pd.read_csv("patient_data.csv")
    # except FileNotFoundError:
    #     df = pd.DataFrame(columns=["Name", "Email", "Address"])

    # # Append new data
    # new_data = pd.DataFrame({"Name": [name], "Email": [email], "Address": [address]})
    # df = pd.concat([df, new_data], ignore_index=True)

    # # Save to CSV
    # df.to_csv("patient_data.csv", index=False)
    db.collection("patients").add({"name": name, "email": email, "address": address})


# Function to save exam data to a file
def save_exam_data(name, glucose, cholesterol, operator):
    # Load existing data or create a new DataFrame
    # try:
    #     df = pd.read_csv("exam_data.csv")
    # except FileNotFoundError:
    #     df = pd.DataFrame(
    #         columns=["Name", "Date", "Glucose", "Cholesterol", "Operator"]
    #     )

    # # Append new data
    # new_data = pd.DataFrame(
    #     {
    #         "Name": [name],
    #         "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    #         "Glucose": [glucose],
    #         "Cholesterol": [cholesterol],
    #         "Operator": [operator],
    #     }
    # )
    # df = pd.concat([df, new_data], ignore_index=True)

    # # Save to CSV
    # df.to_csv("exam_data.csv", index=False)
    db.collection("exams").add(
        {
            "name": name,
            "glucose": glucose,
            "cholesterol": cholesterol,
            "operator": operator,
            "date": firestore.SERVER_TIMESTAMP,  # Server timestamp for the current date
        }
    )


def get_patients():
    try:
        patients_ref = db.collection("patients")
        patients = patients_ref.get()
        patient_data = []
        for patient in patients:
            patient_data.append(patient.to_dict())
        return patient_data
    except Exception as e:
        print(e)


def get_exams(patient_name):
    if patient_name:
        exams_ref = db.collection("exams").where("name", "==", patient_name)
        exams = exams_ref.get()
        exam_data = []
        for exam in exams:
            exam_data.append(exam.to_dict())
        return exam_data
    else:
        return []


# Main function to run the Streamlit app
def main():

    st.title("Registro de Exames")

    # Sidebar for registration
    st.sidebar.title("Cadastro de Pacientes")
    name = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    address = st.sidebar.text_area("Address")
    if st.sidebar.button("Register"):
        save_patient_data(name, email, address)
        st.sidebar.success("Patient Registered Successfully!")

    # Main section for exam records
    st.header("Patient Exam Records")
    # patients = pd.read_csv("patient_data.csv")
    # patient_names = patients["Name"].tolist()
    patient_names = [patient["name"] for patient in get_patients()]
    selected_patient = st.selectbox("Select a Patient", patient_names)

    # Input fields for exam records
    glucose = st.number_input("Glucose Rate")
    cholesterol = st.number_input("Cholesterol Rate")
    operator = st.text_input("Operator Name")

    if st.button("Save Exam"):
        save_exam_data(selected_patient, glucose, cholesterol, operator)
        st.success("Exam Record Saved Successfully!")
        # Clear input fields after saving

    # Display exam records
    # exam_data = pd.read_csv("exam_data.csv")
    # selected_patient_data = exam_data[exam_data["Name"] == selected_patient]
    selected_patient_data = next(
        (patient for patient in get_patients() if patient["name"] == selected_patient),
        None,
    )
    # st.write(selected_patient_data)

    # Display exams for the selected patient
    exams = get_exams(selected_patient_data["name"])
    if exams:
        st.subheader("Exams")
        exam_df = pd.DataFrame(exams)
        st.dataframe(exam_df)
        # for exam in exams:
        #     st.write(f"Date: {exam['date']}")
        #     st.write(f"Glucose: {exam['glucose']}")
        #     st.write(f"Cholesterol: {exam['cholesterol']}")
        #     st.write(f"Operator: {exam['operator']}")
        #     st.write(
        #         f"Comments: {exam.get('comments', '')}"
        #     )  # Adjust as per your Firestore data model
        #     st.write("---")


if __name__ == "__main__":

    main()
