import streamlit as st

def show_patient_profile():

    st.title("👤 Patient Profile")

    st.subheader("📁 Input Method")

    input_method = st.radio(
        "Select Input Method",
        [
            "Manual Entry",
            "Clinical + RNA-seq Upload",
            "CSV Upload",
            "Excel Upload",
            "Patient Matrix Upload"
        ],
        horizontal=True,
        key="input_method"
    )

    st.write("Selected Input:", input_method)