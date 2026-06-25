import streamlit as st


def premium_kpi_cards(
    patient_id,
    risk_score,
    risk_difference,
    risk_group,
    surv_1y,
    surv_3y,
    surv_5y
):

    st.markdown("## 📊 Patient Survival Summary")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Patient",
        patient_id
    )

    c2.metric(
        "Risk Score",
        f"{risk_score:.2f}"
    )

    c3.metric(
        "Risk Difference",
        f"{risk_difference:.2f}"
    )

    c4.metric(
        "Risk Group",
        risk_group
    )

    st.markdown("---")

    c5,c6,c7 = st.columns(3)

    c5.metric(
        "1Y Survival",
        f"{surv_1y:.1f}%"
    )

    c6.metric(
        "3Y Survival",
        f"{surv_3y:.1f}%"
    )

    c7.metric(
        "5Y Survival",
        f"{surv_5y:.1f}%"
    )