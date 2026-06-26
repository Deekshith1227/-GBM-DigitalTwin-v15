import pandas as pd

SIGNATURE_GENES = [
    "OSMR",
    "TMEM171",
    "GJB2",
    "VILL",
    "SHISA6",
    "SCN9A",
    "GPR157",
    "RPL39L",
    "PKD2L1",
    "IGFBP6"
]

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

        profile[gene] = float(
            patient.iloc[0][gene]
        )

    return profile