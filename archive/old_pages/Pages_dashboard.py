import streamlit as st

def show_dashboard():

    st.title("Dashboard")
    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Patients Analysed",
        "1000+"
    )

    c2.metric(
        "Genes Profiled",
        "20,000+"
    )

    c3.metric(
        "Drugs Screened",
        "250+"
    )

    c4.metric(
        "C-Index",
        "0.747"
    )