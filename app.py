import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data
@st.cache_data
def load_data():
    encounters = pd.read_csv('encounters_cleaned.csv')
    payers = pd.read_csv('payers_cleaned.csv')
    organizations = pd.read_csv('organizations_cleaned.csv')
    patients = pd.read_csv('patients_cleaned.csv')
    procedures = pd.read_csv('procedures_cleaned.csv')
    return encounters, payers, organizations, patients, procedures

# Function to display visualizations for a selected patient
def patient_visualizations(patient_id, encounters, payers, organizations, patients, procedures):
    st.title(f"Visualizations for Patient ID: {patient_id}")

    # Filter data for the selected patient
    patient_data = patients[patients['Id'] == patient_id]
    patient_encounters = encounters[encounters['PATIENT'] == patient_id]
    patient_procedures = procedures[procedures['PATIENT'] == patient_id]

    # Display personal information
    st.subheader("Personal Information")
    st.write(patient_data[['FIRST', 'LAST', 'GENDER', 'BIRTHDATE', 'RACE', 'ETHNICITY', 'MARITAL', 'ADDRESS', 'CITY', 'STATE', 'ZIP']])

    # Chart: Number of Encounters Over Time
    st.subheader("Number of Encounters Over Time")
    if not patient_encounters.empty:
        patient_encounters['START'] = pd.to_datetime(patient_encounters['START'])
        encounters_over_time = patient_encounters.groupby(patient_encounters['START'].dt.to_period('M')).size().reset_index(name='count')
        encounters_over_time['START'] = encounters_over_time['START'].astype(str)  # Convert Period to string
        fig = px.line(encounters_over_time, x='START', y='count', title='Number of Encounters Over Time')
        st.plotly_chart(fig)

    # Chart: Distribution of Encounter Classes
    st.subheader("Distribution of Encounter Classes")
    if not patient_encounters.empty:
        encounter_class_dist = patient_encounters['ENCOUNTERCLASS'].value_counts().reset_index()
        encounter_class_dist.columns = ['Encounter Class', 'Count']
        fig = px.bar(encounter_class_dist, x='Encounter Class', y='Count', title='Distribution of Encounter Classes')
        st.plotly_chart(fig)

    # Chart: Number of Procedures by Type
    st.subheader("Number of Procedures by Type")
    if not patient_procedures.empty:
        procedure_type_dist = patient_procedures['DESCRIPTION'].value_counts().reset_index()
        procedure_type_dist.columns = ['Procedure Type', 'Count']
        fig = px.bar(procedure_type_dist, x='Procedure Type', y='Count', title='Number of Procedures by Type')
        st.plotly_chart(fig)

    # Patient Demographics
    st.subheader("Patient Demographics")
    if not patients.empty:
        patient_gender_dist = patients['GENDER'].value_counts().reset_index()
        patient_gender_dist.columns = ['Gender', 'Count']
        fig = px.pie(patient_gender_dist, names='Gender', values='Count', title='Patient Gender Distribution')
        st.plotly_chart(fig)

        patient_race_dist = patients['RACE'].value_counts().reset_index()
        patient_race_dist.columns = ['Race', 'Count']
        fig = px.pie(patient_race_dist, names='Race', values='Count', title='Patient Race Distribution')
        st.plotly_chart(fig)

# Function to generate a report for the selected patient
def patient_report(patient_id, encounters, patients, procedures):
    report_text = ""

    # Filter data for the selected patient
    patient_data = patients[patients['Id'] == patient_id]
    patient_encounters = encounters[encounters['PATIENT'] == patient_id]
    patient_procedures = procedures[procedures['PATIENT'] == patient_id]

    # Generate report content
    if not patient_data.empty:
        report_text += f"**Personal Information**:\n\n"
        report_text += f"Name: {patient_data['FIRST'].values[0]} {patient_data['LAST'].values[0]}\n\n"
        report_text += f"Gender: {patient_data['GENDER'].values[0]}\n\n"
        report_text += f"Date of Birth: {patient_data['BIRTHDATE'].values[0]}\n\n"
        report_text += f"Race: {patient_data['RACE'].values[0]}\n\n"
        report_text += f"Ethnicity: {patient_data['ETHNICITY'].values[0]}\n\n"
        report_text += f"Marital Status: {patient_data['MARITAL'].values[0]}\n\n"
        report_text += f"Address: {patient_data['ADDRESS'].values[0]}, {patient_data['CITY'].values[0]}, {patient_data['STATE'].values[0]} {patient_data['ZIP'].values[0]}\n\n"

    if not patient_encounters.empty:
        report_text += f"**Encounters**:\n"
        report_text += f"Total Encounters: {len(patient_encounters)}\n\n"

    if not patient_procedures.empty:
        report_text += f"**Procedures**:\n"
        report_text += f"Total Procedures: {len(patient_procedures)}\n\n"

    return report_text

# Function to display patient information
def patient_info_page(encounters, payers, organizations, patients, procedures):
    st.title("Patient Health Information")

    # Sidebar for filtering
    st.sidebar.header("Filters")

    # Patient name filter
    patient_list = patients['FIRST'] + " " + patients['LAST']
    selected_patient_name = st.sidebar.selectbox("Select Patient", ["All"] + list(patient_list))

    # Get the patient ID based on the selected patient name
    if selected_patient_name != "All":
        patient_id = patients[patient_list == selected_patient_name]['Id'].values[0]
    else:
        patient_id = "All"

    # Encounter class filter
    encounter_class = st.sidebar.selectbox("Select Encounter Class", ["All"] + list(encounters['ENCOUNTERCLASS'].unique()))

    # Procedure code filter
    procedure_code = st.sidebar.selectbox("Select Procedure Code", ["All"] + list(procedures['CODE'].unique()))

    # Payer filter
    payer_id = st.sidebar.selectbox("Select Payer ID", ["All"] + list(payers['Id'].unique()))

    # Payer name filter
    payer_name = st.sidebar.selectbox("Select Payer Name", ["All"] + list(payers['NAME'].unique()))

    # Organization filter
    organization_id = st.sidebar.selectbox("Select Organization ID", ["All"] + list(organizations['Id'].unique()))

    # City filter
    city = st.sidebar.selectbox("Select City", ["All"] + list(patients['CITY'].unique()))

    # State filter
    state = st.sidebar.selectbox("Select State", ["All"] + list(patients['STATE'].unique()))

    # Race filter
    race = st.sidebar.selectbox("Select Race", ["All"] + list(patients['RACE'].unique()))

    # Filter data for the selected patient
    if patient_id != "All":
        patient_data = patients[patients['Id'] == patient_id]
    else:
        patient_data = patients

    patient_encounters = encounters[encounters['PATIENT'] == patient_id] if patient_id != "All" else encounters
    patient_procedures = procedures[procedures['PATIENT'] == patient_id] if patient_id != "All" else procedures

    # Apply additional filters
    if encounter_class != "All":
        patient_encounters = patient_encounters[patient_encounters['ENCOUNTERCLASS'] == encounter_class]

    if procedure_code != "All":
        patient_procedures = patient_procedures[patient_procedures['CODE'] == procedure_code]

    if payer_id != "All":
        patient_encounters = patient_encounters[patient_encounters['PAYER'] == payer_id]

    if payer_name != "All":
        patient_encounters = patient_encounters[patient_encounters['PAYER'].isin(payers[payers['NAME'] == payer_name]['Id'])]

    if organization_id != "All":
        patient_encounters = patient_encounters[patient_encounters['ORGANIZATION'] == organization_id]

    if city != "All":
        patient_data = patient_data[patient_data['CITY'] == city]

    if state != "All":
        patient_data = patient_data[patient_data['STATE'] == state]

    if race != "All":
        patient_data = patient_data[patient_data['RACE'] == race]

    # Display patient information
    st.subheader("Patient Information")
    st.write(patient_data)

    # Display encounters
    st.subheader("Encounters")
    st.write(patient_encounters)

    # Display procedures
    st.subheader("Procedures")
    st.write(patient_procedures)

# Main function to run the Streamlit app
def main():
    st.title("Patient Health Information System")

    # Load data
    encounters, payers, organizations, patients, procedures = load_data()

    # Sidebar for navigation
    st.sidebar.header("Navigation")

    # Buttons for changing pages
    page = st.sidebar.radio("Go to", ["Patient Info", "Visualizations", "Patient Report"])

    if page == "Patient Info":
        patient_info_page(encounters, payers, organizations, patients, procedures)
    elif page == "Visualizations":
        st.sidebar.header("Select Patient for Visualizations")
        patient_list = patients['FIRST'] + " " + patients['LAST']
        selected_patient_name = st.sidebar.selectbox("Select Patient", patient_list)

        if selected_patient_name:
            patient_id = patients[patient_list == selected_patient_name]['Id'].values[0]
            patient_visualizations(patient_id, encounters, payers, organizations, patients, procedures)
    elif page == "Patient Report":
        st.sidebar.header("Generate Patient Report")
        patient_list = patients['FIRST'] + " " + patients['LAST']
        selected_patient_name = st.sidebar.selectbox("Select Patient", patient_list)

        if selected_patient_name:
            patient_id = patients[patient_list == selected_patient_name]['Id'].values[0]
            report = patient_report(patient_id, encounters, patients, procedures)
            st.subheader(f"Patient Report for {selected_patient_name}")
            st.write(report)

if __name__ == "__main__":
    main()
