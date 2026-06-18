import pandas as pd


def load_clinical_file(file_path):

    df = pd.read_table(file_path)

    return df


def get_patient_ids(df):

    return sorted(
        df["CGGA_ID"].tolist()
    )


def get_clinical_profile(
    df,
    patient_id
):

    row = df[
        df["CGGA_ID"] == patient_id
    ].iloc[0]

    # Age
    age = int(row["Age"])

    # Grade conversion
    grade_text = str(
        row["Grade"]
    ).upper()

    if "IV" in grade_text:
        grade = 4

    elif "III" in grade_text:
        grade = 3

    elif "II" in grade_text:
        grade = 2

    else:
        grade = 4

    # IDH conversion
    idh_text = str(
        row["IDH_mutation_status"]
    )

    if idh_text.lower() == "mutant":
        idh = 1

    elif idh_text.lower() == "wildtype":
        idh = 0

    else:
        idh = -1

    # MGMT conversion
    mgmt_text = str(
        row["MGMTp_methylation_status"]
    )

    if "methylated" in mgmt_text.lower():
        mgmt = 1

    elif "un-methylated" in mgmt_text.lower():
        mgmt = 0

    else:
        mgmt = -1

    return {
        "Age": age,
        "Grade": grade,
        "IDH": idh,
        "MGMT": mgmt
    }