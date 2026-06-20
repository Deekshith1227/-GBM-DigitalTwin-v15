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

        profile.update(
            clinical_profile
        )

        profile.update(
            gene_profile
        )

        st.success(
            "Patient profile loaded"
        )

        st.write(profile)
