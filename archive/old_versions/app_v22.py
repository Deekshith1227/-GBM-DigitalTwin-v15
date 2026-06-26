import streamlit as st
import pandas as pd
import joblib
import tempfile

from gene_extractor import extract_genes
from clinical_loader import *
from pdf_report import create_report
from patient_matrix_extractor import (
    extract_patient_profile,
    get_patient_ids
)
from Drug_Response_Module.treatment_simulator import (
    load_models,
    predict_drug_response,
    predict_drug_resistance,
    generate_treatment_ranking
)

st.title("GBM Digital Twin v2.1")
response_model, resistance_model, resistance_features = (
    load_models()
)

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

if input_method == "Manual Entry":

    profile = {}

    st.subheader("Patient Information")

    profile["Patient_ID"] = st.text_input(
        "Patient ID",
        value="GBM-001"
    )

    profile["Patient_Name"] = st.text_input(
        "Patient Name (Optional)"
    )

    st.subheader("Clinical Inputs")

    profile["Age"] = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=50
    )

    profile["Grade"] = st.selectbox(
        "Grade",
        [2, 3, 4]
    )

    profile["IDH"] = st.selectbox(
        "IDH Status",
        [0, 1]
    )

    profile["MGMT_Status"] = st.selectbox(
        "MGMT Status",
        [0, 1]
    )

    st.subheader("Gene Expression Inputs")

    profile["OSMR"] = st.number_input(
        "OSMR",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["TMEM171"] = st.number_input(
        "TMEM171",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["GJB2"] = st.number_input(
        "GJB2",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["VILL"] = st.number_input(
        "VILL",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["SHISA6"] = st.number_input(
        "SHISA6",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["SCN9A"] = st.number_input(
        "SCN9A",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["GPR157"] = st.number_input(
        "GPR157",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["RPL39L"] = st.number_input(
        "RPL39L",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["PKD2L1"] = st.number_input(
        "PKD2L1",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    profile["IGFBP6"] = st.number_input(
        "IGFBP6",
        min_value=0.0,
        value=1.0,
        step=0.01
    )

    
    st.subheader(
        "Drug Response Biomarkers"
    )

    profile["EGFR"] = st.number_input(
        "EGFR",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    profile["PDGFRA"] = st.number_input(
        "PDGFRA",
        min_value=0.0,
        value=20.0,
        step=1.0
    )

    profile["MET"] = st.number_input(
        "MET",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    profile["MGMT"] = st.number_input(
        "MGMT Expression",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    profile["IDH1"] = st.number_input(
        "IDH1 Expression",
        min_value=0.0,
        value=80.0,
        step=0.1
    )





    with st.expander(
        "View Manual Patient Profile"
    ):
        st.json(profile)

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

        patient_ids = clinical_df[
            "CGGA_ID"
        ].astype(str).tolist()

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

        # Standardize biomarker names

        if "MGMT_expr" in profile:
            profile["MGMT"] = profile["MGMT_expr"]

        if "IDH1_expr" in profile:
            profile["IDH1"] = profile["IDH1_expr"]
        
        st.write("PROFILE KEYS")
        st.write(profile.keys())

        st.write("FULL PROFILE")
        st.json(profile)


        st.success(
            "Patient profile loaded"
        )
        
        with st.expander(
            "View Extracted Patient Profile "
        ):
            st.json(profile)


elif input_method == "CSV Upload":

    csv_file = st.file_uploader(
        "Upload Patient CSV",
        type=["csv"]
    )

    if csv_file:

        df = pd.read_csv(csv_file)

        st.success(
            f"{len(df)} patients loaded"
        )

        patient_ids = df["Patient_ID"].tolist()

        selected_patient = st.selectbox(
            "Select Patient",
            patient_ids
        )

        row = df[
            df["Patient_ID"] == selected_patient
        ].iloc[0]

        profile = {

            "Patient_ID": str(row["Patient_ID"]),

            "Age": int(row["Age"]),
            "Grade": int(row["Grade"]),

            "IDH": int(row["IDH"]),
            "MGMT_Status": int(row["MGMT"]),

            "OSMR": float(row["OSMR"]),
            "TMEM171": float(row["TMEM171"]),
            "GJB2": float(row["GJB2"]),
            "VILL": float(row["VILL"]),
            "SHISA6": float(row["SHISA6"]),
            "SCN9A": float(row["SCN9A"]),
            "GPR157": float(row["GPR157"]),
            "RPL39L": float(row["RPL39L"]),
            "PKD2L1": float(row["PKD2L1"]),
            "IGFBP6": float(row["IGFBP6"]),
            

            "EGFR": float(row["EGFR"]),
            "PDGFRA": float(row["PDGFRA"]),
            "MET": float(row["MET"]),
            "MGMT": float(row["MGMT"]),
            "IDH1": float(row["IDH1"])


        }

        with st.expander(
            "View Extracted Patient Profile"
        ):
            st.json(profile) 
 


elif input_method == "Excel Upload":

    excel_file = st.file_uploader(
        "Upload Patient Excel",
        type=["xlsx", "xls"]
    )

    if excel_file:

        df = pd.read_excel(excel_file)

        st.success(
            f"{len(df)} patients loaded"
        )

        patient_ids = df["Patient_ID"].tolist()

        selected_patient = st.selectbox(
            "Select Patient",
            patient_ids
        )

        row = df[
            df["Patient_ID"] == selected_patient
        ].iloc[0]

        profile = {

            "Patient_ID": str(row["Patient_ID"]),

            "Patient_Name": str(
                row.get(
                    "Patient_Name",
                    ""
                )
            ),

            "Age": int(row["Age"]),
            "Grade": int(row["Grade"]),

            "IDH": int(row["IDH"]),
            "MGMT_Status": int(row["MGMT"]),

            "OSMR": float(row["OSMR"]),
            "TMEM171": float(row["TMEM171"]),
            "GJB2": float(row["GJB2"]),
            "VILL": float(row["VILL"]),
            "SHISA6": float(row["SHISA6"]),
            "SCN9A": float(row["SCN9A"]),
            "GPR157": float(row["GPR157"]),
            "RPL39L": float(row["RPL39L"]),
            "PKD2L1": float(row["PKD2L1"]),
            "IGFBP6": float(row["IGFBP6"]),

           "EGFR": float(row.get("EGFR", 0)),
           "PDGFRA": float(row.get("PDGFRA", 0)),
           "MET": float(row.get("MET", 0)),
           "MGMT": float(row.get("MGMT", 0)),
           "IDH1": float(row.get("IDH1", 0))
        }

        with st.expander(
            "View Extracted Patient Profile"
        ):
            st.json(profile)




elif input_method == "Patient Matrix Upload":

    matrix_file = st.file_uploader(
        "Upload Patient Matrix CSV",
        type=["csv"]
    )

    if matrix_file:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as tmp:

            tmp.write(
                matrix_file.getvalue()
            )

            matrix_path = tmp.name

        patient_ids = get_patient_ids(
            matrix_path
        )

        st.success(
            f"{len(patient_ids)} patients loaded"
        )

        selected_patient = st.selectbox(
            "Select Patient",
            patient_ids
        )

        gene_profile = extract_patient_profile(
            matrix_path,
            selected_patient
        )

        
        profile = {
            "Patient_ID": selected_patient,
            "Patient_Name": selected_patient,

            "Age": 50,
            "Grade": 4,
            "IDH": 0,
            "MGMT_Status": 0
        }

        profile.update(gene_profile)

        with st.expander("View Matrix Patient Profile"):
            st.json(profile)

        if profile is not None:

            if "MGMT_expr" in profile:
                profile["MGMT"] = profile["MGMT_expr"]

            if "IDH1_expr" in profile:
                profile["IDH1"] = profile["IDH1_expr"]
       


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
            "MGMTp_methylation_status": profile.get(
                "MGMT_Status",
                0
            ),
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

       

        MEDIAN_RISK = 2.722561579039131

        risk_difference = risk_score - MEDIAN_RISK

        st.info(
            f"Training Cohort Median Risk: {MEDIAN_RISK:.4f}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Patient ID",
                profile["Patient_ID"]
            )

            if "Patient_Name" in profile:
               st.caption(
                   profile["Patient_Name"]
               )


        with col2:
            st.metric(
                "Risk Score",
                f"{risk_score:.4f}"
            )

        with col3:
            st.metric(
                "Risk Difference",
                f"{risk_difference:.4f}"
            )


        if risk_score > MEDIAN_RISK:

            risk_group = "HIGH RISK"

        else:

            risk_group = "LOW RISK"





        drug_recommendations = recommend_drugs(
            profile,
            risk_group
        )
        
        response_patient = {
            "EGFR": profile.get("EGFR", 0),
            "PDGFRA": profile.get("PDGFRA", 0),
            "MET": profile.get("MET", 0),
            "MGMT": profile.get("MGMT", 0),
            "IDH1": profile.get("IDH1", 0)
        }

        response_df = predict_drug_response(
            response_patient,
            response_model
        )

       


        

        if risk_group == "HIGH RISK":

            st.error(
                "🔴 HIGH RISK"
            )

        else:

            st.success(
                "🟢 LOW RISK"
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


        st.subheader("Drug Recommendations")

        if len(drug_recommendations) == 0:

            st.info(
                "No biomarker-driven recommendations identified."
            )

        else:

            drug_df = pd.DataFrame(
                drug_recommendations,
                columns=[
                    "Drug",
                    "Reason"
                ]
            )

            st.table(drug_df)

        

        # -----------------------------
        # PATIENT SUMMARY
        # -----------------------------

      
        summary_df = pd.DataFrame({
            "Feature":
                [
                    "Patient_ID",
                    "Patient_Name"
                ] +
                list(patient.columns),

            "Value":
                [
                    profile["Patient_ID"],
                    profile.get(
                        "Patient_Name",
                        ""
                    )
                ] +
                list(patient.iloc[0].values)
        })



        clinical_df = summary_df.iloc[:6]
        gene_df = summary_df.iloc[6:]

        st.subheader("Patient Information")
        st.table(clinical_df)

        st.subheader("Gene Expression Signature")
        st.table(gene_df)
      
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
            profile["Patient_ID"],
            profile.get(
                "Patient_Name",
                "Not Provided"
            ),
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

        st.table(
            pd.DataFrame({
                "Parameter":[
                    "Model",
                    "Training Cohort",
                    "External Validation",
                    "Training C-index",
                    "External C-index"
                ],
                "Value":[
                    "GBM Digital Twin v2.1",
                    "CGGA-693",
                    "CGGA-325",
                    "0.7331",
                    "0.7471"
                ]
            })
        )

   