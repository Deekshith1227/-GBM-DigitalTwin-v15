import streamlit as st

st.set_page_config(
    page_title="GBM Digital Twin",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>

/* MAIN APP */

.stApp{
    background:
    linear-gradient(
        135deg,
        #eef2ff 0%,
        #e0e7ff 25%,
        #ede9fe 60%,
        #f5d0fe 100%
    );
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #0f172a,
        #1e1b4b
    );
}

/* HEADER */

.main-header{
    background:
    linear-gradient(
        90deg,
        #0ea5e9,
        #4f46e5,
        #d946ef
    );

    padding:35px;
    border-radius:25px;

    color:white;

    box-shadow:
    0px 10px 40px rgba(79,70,229,0.3);

    margin-bottom:25px;
}

/* Sidebar text */

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Radio button labels */

section[data-testid="stSidebar"] label {
    color: white !important;
}

/* Navigation title */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* CARDS */

div[data-testid="metric-container"]{

    background:rgba(255,255,255,0.85);

    border-radius:20px;

    padding:20px;

    border:1px solid rgba(255,255,255,0.4);

    box-shadow:
    0px 8px 25px rgba(0,0,0,0.08);

    transition:all 0.3s ease;
}

div[data-testid="metric-container"]:hover{

    transform:translateY(-5px);

    box-shadow:
    0px 15px 35px rgba(79,70,229,0.25);
}

/* TABLES */

[data-testid="stTable"]{

    background:white;

    border-radius:20px;

    padding:10px;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.08);
}

/* DATAFRAME */

[data-testid="stDataFrame"]{

    background:white;

    border-radius:20px;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.08);
}

/* PLOTLY */

.js-plotly-plot{

    background:white;

    border-radius:20px;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.08);
}

/* INPUT BOXES */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"]{
    border-radius:15px !important;
    border:2px solid #dbeafe !important;
    background:white !important;
    box-shadow:0px 3px 10px rgba(0,0,0,0.05);
}

/* BUTTONS */

.stButton > button{

    background:
    linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color:white;

    border:none;

    border-radius:15px;

    font-weight:bold;
}

/* SIDEBAR MENU */

.stRadio label {
    font-size:16px !important;
    font-weight:600 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.3);
}

/* SUBHEADERS */

h1,h2,h3{

    color:#1e293b;
}

</style>
""", unsafe_allow_html=True)

import pandas as pd
import joblib
import tempfile

from Visualizations.risk_gauge import (
    create_risk_gauge
)
from Visualizations.survival_curve import (
    create_survival_curve
)
from Visualizations.premium_kpi_cards import (
    premium_kpi_cards
)
from Visualizations.drug_ranking_chart import (
    create_drug_ranking_chart
)
from Visualizations.scatter_plot import (
    create_response_resistance_scatter
)
from Visualizations.biomarker_heatmap import (
    create_biomarker_heatmap
)
from Visualizations.gene_radar_chart import (
    create_gene_radar_chart
)
from Visualizations.drug_ranking_chart import (
    create_drug_ranking_chart
)
from Visualizations.risk_comparison import (
    create_risk_comparison
)
from Visualizations.survival_donuts import (
    create_survival_donut
)
from gene_extractor import (
    extract_genes,
    extract_full_transcriptome
)
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
from drug_recommendation import recommend_drugs

st.markdown("""
<div class="main-header">

<h1 style="font-size:55px;">
🧠 GBM Digital Twin
</h1>

<h3>
AI-Powered Precision Oncology Platform
</h3>

</div>
""", unsafe_allow_html=True)

response_model, resistance_model, resistance_features = (
    load_models()
)
with st.sidebar:

    st.markdown("""
    <div style='text-align:center;padding-top:20px;'>
    <h1 style='color:white;'>🧠</h1>
    <h2 style='color:white;'>GBM Digital Twin</h2>
    <p style='color:#cbd5e1;'>Precision Oncology Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 GBM Digital Twin")
    st.info("Version 2.3 - Clinical Decision Support")

    st.divider()
    st.markdown("### 📁 Input Method")

    input_method = st.radio(
        "",
        [
            "Manual Entry",
            "Clinical + RNA-seq Upload",
            "CSV Upload",
            "Excel Upload",
            "Patient Matrix Upload"
        ],
        key="input_method"
    )

    
    

profile = None
full_expr = None

input_method = st.session_state.get(
    "input_method",
    "Manual Entry"
)

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


    full_expr = pd.Series(profile)


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


        full_expr = extract_full_transcriptome(
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
            

            "EGFR": float(row.get("EGFR", 0)),
            "PDGFRA": float(row.get("PDGFRA", 0)),
            "MET": float(row.get("MET", 0)),
            "MGMT": float(row.get("MGMT", 0)),
            "IDH1": float(row.get("IDH1", 0))

        }
         
        full_expr = pd.Series(profile)

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
        
        full_expr = pd.Series(profile)

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

        full_expr = pd.Series(profile)

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

        with st.spinner("🧠 Building Digital Twin..."):

            from huggingface_hub import hf_hub_download

            MODEL_PATH = hf_hub_download(
                repo_id="Deekshith1204/gbm-digital-twin-models",
                filename="DigitalTwin_v15_Model.pkl"
            )

            model = joblib.load(MODEL_PATH)

            # keep ALL remaining prediction code here

    
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
        

        if risk_score > MEDIAN_RISK:

            risk_group = "HIGH RISK"

        else:

            risk_group = "LOW RISK"
        
        



        st.markdown(
            """
            <style>

            div[data-testid="metric-container"] {
                background-color:#f8f9fa;
                border:1px solid #dce3ea;
                padding:15px;
                border-radius:15px;
                box-shadow:0px 4px 12px rgba(0,0,0,0.08);
            }

            </style>
            """,
            unsafe_allow_html=True
        )
        




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

        resistance_df = None
        combined_df = None

        if full_expr is not None:

            resistance_df = predict_drug_resistance(
                full_expr,
                resistance_model,
                resistance_features
            )
        if resistance_df is not None:
            combined_df = generate_treatment_ranking(
                response_df,
                resistance_df
            )
        else:
            combined_df = None 

        
       


        

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

        
        
        with st.container():

            premium_kpi_cards(
                patient_id=profile["Patient_ID"],
                risk_score=risk_score,
                risk_difference=risk_difference,
                risk_group=risk_group,
                surv_1y=surv_1y,
                surv_3y=surv_3y,
                surv_5y=surv_5y
            )
        
        c1, c2, c3 = st.columns(3)

        with c1:
            donut1 = create_survival_donut(
                surv_1y,
                "1-Year Survival"
            )

            st.plotly_chart(
                donut1,
                use_container_width=True
            )

        with c2:
            donut3 = create_survival_donut(
                surv_3y,
                "3-Year Survival"
            )

            st.plotly_chart(
                donut3,
                use_container_width=True
            )

        with c3:
            donut5 = create_survival_donut(
                surv_5y,
                "5-Year Survival"
            )

            st.plotly_chart(
                donut5,
                use_container_width=True
            )

        risk_compare_fig = create_risk_comparison(
            risk_score,
            MEDIAN_RISK
        )

        with st.container(border=True):

            st.plotly_chart(
                risk_compare_fig,
                use_container_width=True
            )

        gauge = create_risk_gauge(
            risk_score,
            MEDIAN_RISK
        )

        with st.container(border=True):

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

        


        survival_fig = create_survival_curve(
            surv_1y,
            surv_3y,
            surv_5y
        )

        
        with st.container(border=True):

            st.plotly_chart(
                survival_fig,
                use_container_width=True
            )
        
        st.subheader("💊 Drug Recommendations")

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
            st.subheader(
                "Drug Response Predictions"
            )

            st.dataframe(
                response_df.head(20)
            )
        if resistance_df is not None:

            st.subheader(
                "Final Treatment Ranking"
            )

            ranking_fig = create_drug_ranking_chart(
                combined_df
            )

            with st.container(border=True):

                st.plotly_chart(
                    ranking_fig,
                    use_container_width=True
                )

            scatter_fig = (
                create_response_resistance_scatter(
                    combined_df
                )
            )

            with st.container(border=True):

                st.plotly_chart(
                    scatter_fig,
                    use_container_width=True
                )
            st.dataframe(
                combined_df.head(20)
            )

        # -----------------------------
        # PATIENT SUMMARY
        # -----------------------------

      
        summary_df = pd.DataFrame({
            "Feature":
                [
                    "Patient_ID",
                    "Patient_Name"
                ] + list(patient.columns),

            "Value":
                [
                    str(profile["Patient_ID"]),
                    str(profile.get("Patient_Name", ""))
                ] + [str(v) for v in patient.iloc[0].values]
        })

        summary_df["Feature"] = summary_df["Feature"].astype(str)
        summary_df["Value"] = summary_df["Value"].astype(str)

        clinical_df = summary_df.iloc[:6]
        gene_df = summary_df.iloc[6:]



        clinical_df = summary_df.iloc[:6]
        gene_df = summary_df.iloc[6:]

        with st.container(border=True):

            st.subheader("👤 Patient Information")

            st.table(clinical_df)

        with st.container(border=True):

            st.subheader("🧬 Gene Expression Signature")

            st.table(gene_df)

        heatmap_fig = create_biomarker_heatmap(
            profile
        )

        with st.container(border=True):

            st.plotly_chart(
                heatmap_fig,
                use_container_width=True
            )

        st.subheader("Gene Expression Radar Chart")

        radar_fig = create_gene_radar_chart(
            profile
        )

        with st.container():

            st.plotly_chart(
                radar_fig,
                use_container_width=True
            )
      
        # -----------------------------
        # CLINICAL INTERPRETATION
        # -----------------------------

        st.subheader(
            "📊 Clinical Interpretation"
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
            "⚙️ Model Information"
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
 
        st.markdown("---")

        st.markdown(
        """
        <center>

        ### 🧠 GBM Digital Twin v2.3

        Built by Deekshith MM

        M.Pharm (Pharmaceutical Biotechnology)

        JSS College of Pharmacy, Ooty

        Powered by AI, Bioinformatics & Precision Oncology

        </center>
        """,
        unsafe_allow_html=True
        )


        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Patients Analyzed",
            "1,000+"
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
            "Model Accuracy",
            "87%"
        )
   