import streamlit as st
import joblib
import pandas as pd
from pdf_report import create_report

st.title("GBM Digital Twin v1.5")

st.header("Clinical Inputs")

age = st.number_input("Age", 1, 100, 50)

grade = st.selectbox(
    "Grade",
    [2, 3, 4]
)

idh = st.selectbox(
    "IDH Status",
    [0, 1, -1]
)

mgmt = st.selectbox(
    "MGMT Status",
    [0, 1, -1]
)

st.header("Gene Expression Inputs")

OSMR = st.number_input("OSMR", value=1.0)
TMEM171 = st.number_input("TMEM171", value=1.0)
GJB2 = st.number_input("GJB2", value=1.0)
VILL = st.number_input("VILL", value=1.0)
SHISA6 = st.number_input("SHISA6", value=1.0)
SCN9A = st.number_input("SCN9A", value=1.0)
GPR157 = st.number_input("GPR157", value=1.0)
RPL39L = st.number_input("RPL39L", value=1.0)
PKD2L1 = st.number_input("PKD2L1", value=1.0)
IGFBP6 = st.number_input("IGFBP6", value=1.0)

if st.button("Predict"):

    model = joblib.load(
        "DigitalTwin_v15_Model.pkl"
    )

    patient = pd.DataFrame([{
        "Age": age,
        "Grade": grade,
        "IDH_mutation_status": idh,
        "MGMTp_methylation_status": mgmt,
        "OSMR": OSMR,
        "TMEM171": TMEM171,
        "GJB2": GJB2,
        "VILL": VILL,
        "SHISA6": SHISA6,
        "SCN9A": SCN9A,
        "GPR157": GPR157,
        "RPL39L": RPL39L,
        "PKD2L1": PKD2L1,
        "IGFBP6": IGFBP6
    }])

    # Risk Score
    risk_score = model.predict(patient)[0]

    # Survival Prediction
    surv = model.predict_survival_function(patient)

    sf = surv[0]

    surv_1y = sf(365) * 100
    surv_3y = sf(1095) * 100
    surv_5y = sf(1825) * 100

    # Risk Threshold
    MEDIAN_RISK = 2.722561579039131

    st.success(
        f"Predicted Risk Score: {risk_score:.4f}"
    )

    st.info(
        f"Training Cohort Median Risk: {MEDIAN_RISK:.4f}"
    )

    # Risk Classification
    if risk_score > MEDIAN_RISK:
        risk_group = "HIGH RISK"
        st.error(
            f"Risk Group: {risk_group}"
        )
    else:
        risk_group = "LOW RISK"
        st.success(
            f"Risk Group: {risk_group}"
        )

    # Survival Probabilities
    st.subheader(
        "Survival Probabilities"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "1-Year Survival",
            f"{surv_1y:.2f}%"
        )

    with col2:
        st.metric(
            "3-Year Survival",
            f"{surv_3y:.2f}%"
        )

    with col3:
        st.metric(
            "5-Year Survival",
            f"{surv_5y:.2f}%"
        )

    # Clinical Interpretation
    st.subheader(
        "Clinical Interpretation"
    )

    if risk_group == "HIGH RISK":

        st.warning(
            """
            This patient has a higher
            predicted mortality risk
            compared with the reference
            GBM cohort.

            Consider closer clinical
            monitoring and aggressive
            treatment strategies.
            """
        )

    else:

        st.info(
            """
            This patient has a lower
            predicted mortality risk
            compared with the reference
            GBM cohort.

            Prognosis is relatively
            favorable within the model.
            """
        )

    # Patient Summary
    st.subheader(
        "Patient Summary"
    )

    st.dataframe(patient)

    # PDF Report Section
    st.subheader(
        "Clinical Report"
    )

    pdf_file = (
        "GBM_DigitalTwin_Report.pdf"
    )

    create_report(
        pdf_file,
        age,
        grade,
        risk_score,
        risk_group,
        surv_1y,
        surv_3y,
        surv_5y
    )

    with open(
        pdf_file,
        "rb"
    ) as pdf:

        st.download_button(
            label="📄 Download Clinical PDF Report",
            data=pdf,
            file_name="GBM_DigitalTwin_Report.pdf",
            mime="application/pdf"
        )

    # Model Information
    st.subheader(
        "Model Information"
    )

    st.write({
        "Model":
        "GBM Digital Twin v1.5",

        "Training Cohort":
        "CGGA-693",

        "External Validation":
        "CGGA-325",

        "Training Median Risk":
        2.722561579039131,

        "Training C-index":
        0.7331,

        "External C-index":
        0.7471
    })