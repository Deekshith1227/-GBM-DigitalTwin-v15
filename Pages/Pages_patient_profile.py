import streamlit as st

def show_patient_profile():

    st.title("👤 Patient Profile")

    input_method = st.radio(
        "Select Input Method",
        [
            "Manual Entry",
            "Clinical + RNA-seq Upload",
            "CSV Upload",
            "Excel Upload",
            "Patient Matrix Upload"
        ]
    )

    st.session_state["input_method"] = input_method

    st.write("Selected Input:", input_method)