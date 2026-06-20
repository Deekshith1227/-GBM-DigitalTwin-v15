
import joblib

model = joblib.load(
    r"C:\Users\ROHITH\DigitalTwin_v1_Model.pkl"
)

def predict_patient(
    OSMR,
    TMEM171,
    GJB2,
    VILL,
    SHISA6,
    SCN9A,
    GPR157,
    RPL39L,
    PKD2L1,
    IGFBP6
):
    coef = model["coefficients"]

    risk_score = (
        coef["OSMR"] * OSMR +
        coef["TMEM171"] * TMEM171 +
        coef["GJB2"] * GJB2 +
        coef["VILL"] * VILL +
        coef["SHISA6"] * SHISA6 +
        coef["SCN9A"] * SCN9A +
        coef["GPR157"] * GPR157 +
        coef["RPL39L"] * RPL39L +
        coef["PKD2L1"] * PKD2L1 +
        coef["IGFBP6"] * IGFBP6
    )

    risk_group = (
        "High"
        if risk_score > model["median_risk_score"]
        else "Low"
    )

    return {
        "Risk Score": risk_score,
        "Risk Group": risk_group
    }
