import streamlit as st
import joblib
import pandas as pd

from gene_extractor import extract_genes
from patient_matrix_extractor import extract_patient_profile
from pdf_report import create_report

# -----------------------------
# TITLE
# -----------------------------

st.title("GBM Digital Twin v2.0")

# -----------------------------
# INPUT METHOD
# -----------------------------

st.header("Input Method")

input_method = st.radio(
    "Choose Input Method",
    [
        "Manual Entry",
        "CSV Upload",
        "Excel Upload",
        "Patient Matrix Upload",
        "RNA-seq Matrix Upload"
    ]
)
uploaded_file = None

if input_method != "Manual Entry":

   uploaded_file = st.file_uploader(
    "Upload Gene Expression File",
    type=["csv", "xlsx", "txt"]
)

# -----------------------------
# CLINICAL INPUTS
# -----------------------------

st.header("Clinical Inputs")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=100,
    value=50
)

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

# -----------------------------
# GENE INPUTS
# -----------------------------

# -----------------------------
# GENE INPUTS
# -----------------------------

default_values = {
    "OSMR": 1.0,
    "TMEM171": 1.0,
    "GJB2": 1.0,
    "VILL": 1.0,
    "SHISA6": 1.0,
    "SCN9A": 1.0,
    "GPR157": 1.0,
    "RPL39L": 1.0,
    "PKD2L1": 1.0,
    "IGFBP6": 1.0
}

if uploaded_file is not None:

    try:

        # -----------------------------
        # CSV Upload
        # -----------------------------

        if input_method == "CSV Upload":

            df = pd.read_csv(uploaded_file)

            gene_dict = dict(
                zip(
                    df["Gene"],
                    df["Expression"]
                )
            )

            for gene in default_values:

                if gene in gene_dict:

                    default_values[gene] = float(
                        gene_dict[gene]
                    )

        # -----------------------------
        # Excel Upload
        # -----------------------------

        elif input_method == "Excel Upload":

            df = pd.read_excel(
                uploaded_file
            )

            gene_dict = dict(
                zip(
                    df["Gene"],
                    df["Expression"]
                )
            )

            for gene in default_values:

                if gene in gene_dict:

                    default_values[gene] = float(
                        gene_dict[gene]
                    )

        # -----------------------------
        # Patient Matrix Upload
        # -----------------------------

        elif input_method == "Patient Matrix Upload":

            matrix_df = pd.read_csv(
                uploaded_file
            )

            patient_ids = (
                matrix_df["CGGA_ID"]
                .tolist()
            )

            selected_patient = st.selectbox(
                "Select Patient ID",
                patient_ids
            )

            patient_row = matrix_df[
                matrix_df["CGGA_ID"]
                == selected_patient
            ]

            for gene in default_values:

                default_values[gene] = float(
                    patient_row.iloc[0][gene]
                )

        # -----------------------------
        # RNA-seq Matrix Upload
        # -----------------------------

        elif input_method == "RNA-seq Matrix Upload":

            import tempfile

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt"
            ) as tmp:

                tmp.write(
                    uploaded_file.getvalue()
                )

                temp_path = tmp.name

            patient_id = st.text_input(
                "Patient ID",
                "CGGA_1002"
            )

            gene_values = extract_genes(
                temp_path,
                patient_id
            )

            st.write(gene_values)

            for gene in default_values:

                if gene in gene_values:

                    default_values[gene] = float(
                        gene_values[gene]
                    )

        st.success(
            "Gene expression values loaded successfully"
        )

    except Exception as e:

        st.error(
            f"Upload Error: {e}"
        )
# -----------------------------
# GENE EXPRESSION INPUTS
# -----------------------------

st.header("Gene Expression Inputs")

OSMR = st.number_input(
    "OSMR",
    value=float(default_values["OSMR"])
)

TMEM171 = st.number_input(
    "TMEM171",
    value=float(default_values["TMEM171"])
)

GJB2 = st.number_input(
    "GJB2",
    value=float(default_values["GJB2"])
)

VILL = st.number_input(
    "VILL",
    value=float(default_values["VILL"])
)

SHISA6 = st.number_input(
    "SHISA6",
    value=float(default_values["SHISA6"])
)

SCN9A = st.number_input(
    "SCN9A",
    value=float(default_values["SCN9A"])
)

GPR157 = st.number_input(
    "GPR157",
    value=float(default_values["GPR157"])
)

RPL39L = st.number_input(
    "RPL39L",
    value=float(default_values["RPL39L"])
)

PKD2L1 = st.number_input(
    "PKD2L1",
    value=float(default_values["PKD2L1"])
)

IGFBP6 = st.number_input(
    "IGFBP6",
    value=float(default_values["IGFBP6"])
)

# -----------------------------
# PREDICTION
# -----------------------------

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

    risk_score = model.predict(
        patient
    )[0]

    surv = model.predict_survival_function(
        patient
    )

    sf = surv[0]

    surv_1y = sf(365) * 100
    surv_3y = sf(1095) * 100
    surv_5y = sf(1825) * 100

    MEDIAN_RISK = 2.722561579039131

    st.success(
        f"Predicted Risk Score: {risk_score:.4f}"
    )

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

    # -----------------------------
    # SURVIVAL
    # -----------------------------

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

    # -----------------------------
    # INTERPRETATION
    # -----------------------------

    st.subheader(
        "Clinical Interpretation"
    )

    if risk_group == "HIGH RISK":

        st.warning(
            "This patient has a higher predicted mortality risk compared with the reference GBM cohort."
        )

    else:

        st.info(
            "This patient has a lower predicted mortality risk compared with the reference GBM cohort."
        )

    # -----------------------------
    # PATIENT SUMMARY
    # -----------------------------

    st.subheader(
        "Patient Summary"
    )

    st.dataframe(
        patient
    )

    # -----------------------------
    # PDF REPORT
    # -----------------------------

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

    # -----------------------------
    # MODEL INFO
    # -----------------------------

    st.subheader(
        "Model Information"
    )

    st.write({
        "Model":
        "GBM Digital Twin v2.0",

        "Training Cohort":
        "CGGA-693",

        "External Validation":
        "CGGA-325",

        "Training C-index":
        0.7331,

        "External C-index":
        0.7471
    })