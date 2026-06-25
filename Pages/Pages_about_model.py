import streamlit as st

def show_about_model():

    st.title("About Model")
    st.write("""
    GBM Digital Twin v2.3

    Training Cohort:
    CGGA-693

    Validation Cohort:
    CGGA-325

    Algorithm:
    Random Survival Forest

    Training C-index:
    0.7331

    External C-index:
    0.7471
    """)