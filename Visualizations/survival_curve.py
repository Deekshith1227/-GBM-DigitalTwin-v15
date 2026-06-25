import plotly.graph_objects as go

def create_survival_curve(
    surv_1y,
    surv_3y,
    surv_5y
):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=[
                1,
                3,
                5
            ],

            y=[
                surv_1y,
                surv_3y,
                surv_5y
            ],

            mode="lines+markers",

            line={
                "width":4
            }
        )
    )

    fig.update_layout(

        title=
        "Predicted Survival Curve",

        xaxis_title=
        "Years",

        yaxis_title=
        "Survival Probability (%)"
    )

    return fig