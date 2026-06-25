import streamlit as st

def show_kpi_cards(
    patient_id,
    risk_score,
    risk_group,
    risk_difference,
    surv_1y,
    surv_3y,
    surv_5y
):

    st.markdown("## 📊 Patient Survival Summary")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "🧑 Patient",
            patient_id
        )

    with col2:
        st.metric(
            "⚠ Risk Score",
            f"{risk_score:.2f}"
        )

    with col3:
        st.metric(
            "📈 Risk Difference",
            f"{risk_difference:.2f}"
        )

    with col4:
        st.metric(
            "🎯 Risk Group",
            risk_group
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "1-Year Survival",
            f"{surv_1y:.1f}%"
        )

    with col2:
        st.metric(
            "3-Year Survival",
            f"{surv_3y:.1f}%"
        )

    with col3:
        st.metric(
            "5-Year Survival",
            f"{surv_5y:.1f}%"
        )