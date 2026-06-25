import plotly.graph_objects as go


def create_risk_comparison(
    patient_risk,
    median_risk
):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=["Patient"],
            x=[patient_risk],
            orientation="h",
            name="Patient"
        )
    )

    fig.add_trace(
        go.Bar(
            y=["Median"],
            x=[median_risk],
            orientation="h",
            name="Cohort"
        )
    )

    fig.update_layout(
        title="Patient vs Training Cohort Risk",
        height=400
    )

    return fig