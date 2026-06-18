import streamlit as st
import pandas as pd
import joblib
import tempfile

from gene_extractor import extract_genes
from clinical_loader import *
from pdf_report import create_report




st.title("GBM Digital Twin v2.1")

input_method = st.radio(
    "Choose Input Method",
    [
        "Manual Entry",
        "Clinical + RNA-seq Upload",
        "CSV Upload",
        "Excel Upload",
        "Patient Matrix Upload"
    ]
)


profile = None

if input_method == "Clinical + RNA-seq Upload":

    clinical_file = st.file_uploader(
        "Upload Clinical File",
        type=["txt"],
        key="clinical"
    )

    rnaseq_file = st.file_uploader(
        "Upload RNA-seq File",
        type=["txt"],
        key="rnaseq"
    )

    if clinical_file and rnaseq_file:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        ) as tmp1:

            tmp1.write(
                clinical_file.getvalue()
            )

            clinical_path = tmp1.name

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        ) as tmp2:

            tmp2.write(
                rnaseq_file.getvalue()
            )

            rnaseq_path = tmp2.name

        clinical_df = load_clinical_file(
            clinical_path
        )

        patient_ids = get_patient_ids(
            clinical_df
        )

        selected_patient = st.selectbox(
            "Select Patient",
            patient_ids
        )

        clinical_profile = (
            get_clinical_profile(
                clinical_df,
                selected_patient
            )
        )

        gene_profile = extract_genes(
            rnaseq_path,
            selected_patient
        )
        
        profile = {}

        profile["Patient_ID"] = selected_patient

        profile.update(
            clinical_profile
        )

        profile.update(
            gene_profile
        )

        st.success(
            "Patient profile loaded"
        )
        
        with st.expander(
            "View Extracted Patient Profile (Debug)"
        ):
            st.json(profile)

if st.button("Predict Patient Outcome"):

    if profile is None:

        st.error(
            "Please load a patient first."
        )

    else:

        model = joblib.load(
            "DigitalTwin_v15_Model.pkl"
        )

        patient = pd.DataFrame([{
            "Age": profile["Age"],
            "Grade": profile["Grade"],
            "IDH_mutation_status": profile["IDH"],
            "MGMTp_methylation_status": profile["MGMT"],
            "OSMR": profile["OSMR"],
            "TMEM171": profile["TMEM171"],
            "GJB2": profile["GJB2"],
            "VILL": profile["VILL"],
            "SHISA6": profile["SHISA6"],
            "SCN9A": profile["SCN9A"],
            "GPR157": profile["GPR157"],
            "RPL39L": profile["RPL39L"],
            "PKD2L1": profile["PKD2L1"],
            "IGFBP6": profile["IGFBP6"]
        }])

        risk_score = model.predict(
            patient
        )[0]

        st.success(
            f"Risk Score: {risk_score:.4f}"
        )
        
        MEDIAN_RISK = 2.722561579039131

        st.info(
            f"Training Cohort Median Risk: {MEDIAN_RISK:.4f}"
        )

        

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

        surv = model.predict_survival_function(
            patient
        )

        sf = surv[0]

        surv_1y = sf(365) * 100
        surv_3y = sf(1095) * 100
        surv_5y = sf(1825) * 100

        st.subheader(
            "Survival Probabilities"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "1-Year",
                f"{surv_1y:.2f}%"
            )

        with c2:
            st.metric(
                "3-Year",
                f"{surv_3y:.2f}%"
            )

        with c3:
            st.metric(
                "5-Year",
                f"{surv_5y:.2f}%"
            )



              # -----------------------------
        # PATIENT SUMMARY
        # -----------------------------

        st.subheader("Patient Summary")

        summary_df = pd.DataFrame({
            "Feature":
                ["Patient_ID"] +
                list(patient.columns),

            "Value":
                [profile["Patient_ID"]] +
                list(patient.iloc[0].values)
        })
            
        st.dataframe(
            summary_df,
            use_container_width=True
        )

        

        # -----------------------------
        # CLINICAL INTERPRETATION
        # -----------------------------

        st.subheader(
            "Clinical Interpretation"
        )

        if risk_group == "HIGH RISK":

            st.warning(
                "This patient has a higher predicted mortality risk compared with the reference GBM cohort."
            )

        else:

            st.success(
                "This patient has a lower predicted mortality risk compared with the reference GBM cohort."
            )

        # -----------------------------
        # PDF REPORT
        # -----------------------------

        pdf_file = (
            "GBM_DigitalTwin_Report.pdf"
        )

        create_report(
            pdf_file,
            profile["Patient ID"],
            patient["Age"].iloc[0],
            patient["Grade"].iloc[0],
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
                label="📄 Download Clinical Report",
                data=pdf,
                file_name="GBM_DigitalTwin_Report.pdf",
                mime="application/pdf"
            )

        # -----------------------------
        # MODEL INFORMATION
        # -----------------------------

        st.subheader(
            "Model Information"
        )

        st.json({
            "Model":
            "GBM Digital Twin v2.1",

            "Training Cohort":
            "CGGA-693",

            "External Validation":
            "CGGA-325",

            "Training C-index":
            0.7331,

            "External C-index":
            0.7471
        })
