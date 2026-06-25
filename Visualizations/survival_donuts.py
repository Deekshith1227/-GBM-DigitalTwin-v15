import plotly.graph_objects as go


def create_survival_donut(
    value,
    title
):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,

            number={
                "suffix":"%"
            },

            title={
                "text":title
            },

            gauge={
                "axis":{
                    "range":[0,100]
                },

                "bar":{
                    "thickness":0.35
                },

                "bgcolor":"white"
            }
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig