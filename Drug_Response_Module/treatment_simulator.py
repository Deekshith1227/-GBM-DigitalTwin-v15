import joblib
import pandas as pd

from huggingface_hub import hf_hub_download

REPO_ID = "Deekshith1204/gbm-digital-twin-models"

def load_models():

    response_model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="drug_response_rf.pkl"
    )

    resistance_model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="drug_resistance_rf.pkl"
    )

    resistance_features_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="drug_resistance_features.pkl"
    )

    response_model = joblib.load(
        response_model_path
    )

    resistance_model = joblib.load(
        resistance_model_path
    )

    resistance_features = joblib.load(
        resistance_features_path
    )

    return (
        response_model,
        resistance_model,
        resistance_features
    )


def predict_drug_response(
    patient_profile,
    response_model
):

    feature_names = list(
        response_model.feature_names_in_
    )

    drug_list = sorted([
        x.replace("drug_", "")
        for x in feature_names
        if x.startswith("drug_")
    ])

    results = []

    for drug in drug_list:

        row = pd.DataFrame(
            0,
            index=[0],
            columns=feature_names
        )

        row["EGFR"] = patient_profile["EGFR"]
        row["PDGFRA"] = patient_profile["PDGFRA"]
        row["MET"] = patient_profile["MET"]
        row["MGMT"] = patient_profile["MGMT"]
        row["IDH1"] = patient_profile["IDH1"]

        row[f"drug_{drug}"] = 1

        pred = response_model.predict(
            row
        )[0]

        results.append(
            [drug, pred]
        )

    results_df = pd.DataFrame(
        results,
        columns=[
            "Drug",
            "Predicted_LN_IC50"
        ]
    )

    results_df["Response_Score"] = (
        -results_df["Predicted_LN_IC50"]
    )

    return results_df.sort_values(
        "Response_Score",
        ascending=False
    )

def predict_drug_resistance(
    patient_expression,
    resistance_model,
    resistance_features
):

    drug_list = sorted([
        x.replace("drug_", "")
        for x in resistance_features
        if x.startswith("drug_")
    ])

    results = []

    base_row = pd.DataFrame(
        0.0,
        index=[0],
        columns=resistance_features
    )

    for gene in patient_expression.index:

        if gene in base_row.columns:

            base_row.at[0, gene] = (
                patient_expression[gene]
            )

    for drug in drug_list:

        row = base_row.copy()

        drug_col = f"drug_{drug}"

        if drug_col in row.columns:

            row.at[0, drug_col] = 1

            prob = (
                resistance_model
                .predict_proba(row)[0, 1]
            )

            results.append(
                [drug, prob]
            )

    resistance_df = pd.DataFrame(
        results,
        columns=[
            "Drug",
            "Resistance_Probability"
        ]
    )

    return resistance_df.sort_values(
        "Resistance_Probability"
    )


def generate_treatment_ranking(
    response_df,
    resistance_df
):

    combined = response_df.merge(
        resistance_df,
        on="Drug"
    )

    combined["Final_Score"] = (
        combined["Response_Score"]
        *
        (
            1
            - combined[
                "Resistance_Probability"
            ]
        )
    )

    combined = combined.sort_values(
        "Final_Score",
        ascending=False
    )

    return combined