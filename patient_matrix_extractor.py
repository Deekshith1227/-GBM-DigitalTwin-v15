import pandas as pd

SIGNATURE_GENES = [

    # Survival Model
    "OSMR",
    "TMEM171",
    "GJB2",
    "VILL",
    "SHISA6",
    "SCN9A",
    "GPR157",
    "RPL39L",
    "PKD2L1",
    "IGFBP6",

    # Drug Response Biomarkers
    "EGFR",
    "PDGFRA",
    "MET",
    "MGMT",
    "IDH1"
]

def get_patient_ids(file_path):

    df = pd.read_csv(file_path)

    return (
        df["CGGA_ID"]
        .astype(str)
        .tolist()
    )


def extract_patient_profile(
    file_path,
    patient_id
):

    df = pd.read_csv(file_path)

    patient = df[
        df["CGGA_ID"] == patient_id
    ]

    if len(patient) == 0:

        raise ValueError(
            "Patient not found"
        )

    profile = {}

    for gene in SIGNATURE_GENES:

        if gene in patient.columns:

            profile[gene] = float(
                patient.iloc[0][gene]
            )

        else:

            profile[gene] = None

    return profile