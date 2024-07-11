from datetime import datetime

import pandas as pd
import streamlit as st


# Function to save patient data to a file
def save_patient_data(name, email, address):
    # Load existing data or create a new DataFrame
    try:
        df = pd.read_csv("patient_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Email", "Address"])

    # Append new data
    new_data = pd.DataFrame({"Name": [name], "Email": [email], "Address": [address]})
    df = pd.concat([df, new_data], ignore_index=True)

    # Save to CSV
    df.to_csv("patient_data.csv", index=False)


# Function to save exam data to a file
def save_exam_data(name, glucose, cholesterol, operator):
    # Load existing data or create a new DataFrame
    try:
        df = pd.read_csv("exam_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["Name", "Date", "Glucose", "Cholesterol", "Operator"]
        )

    # Append new data
    new_data = pd.DataFrame(
        {
            "Name": [name],
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Glucose": [glucose],
            "Cholesterol": [cholesterol],
            "Operator": [operator],
        }
    )
    df = pd.concat([df, new_data], ignore_index=True)

    # Save to CSV
    df.to_csv("exam_data.csv", index=False)


def render_df_with_validation(df):
    # Initialize lists to store checkbox and comment inputs
    validated = []
    comments = []

    # Iterate through DataFrame rows
    for index, row in df.iterrows():
        validated.append(st.checkbox(f"Validate {row['Name']}"))
        comments.append(st.text_area(f"Comments for {row['Name']}"))

    # Add new columns for validation and comments
    df["Validated"] = validated
    df["Comments"] = comments

    return df


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
        st.sidebar.text_input("Name", value="")
        st.sidebar.text_input("Email", value="")
        st.sidebar.text_area("Address", value="")

    # Main section for exam records
    st.header("Patient Exam Records")
    patients = pd.read_csv("patient_data.csv")
    patient_names = patients["Name"].tolist()
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
    exam_data = pd.read_csv("exam_data.csv")
    selected_patient_data = exam_data[exam_data["Name"] == selected_patient]

    validated_df = render_df_with_validation(selected_patient_data)
    st.dataframe(validated_df)
    # st.write(selected_patient_data)


if __name__ == "__main__":
    main()
