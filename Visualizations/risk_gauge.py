import plotly.graph_objects as go

def create_risk_gauge(
    risk_score,
    median_risk
):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",

            value=risk_score,

            title={
                "text":"Risk Score"
            },

            gauge={
                "axis":{
                    "range":[0,6]
                },

                "bar":{
                    "color":"darkred"
                },

                "steps":[

                    {
                        "range":[0,2],
                        "color":"lightgreen"
                    },

                    {
                        "range":[2,3],
                        "color":"gold"
                    },

                    {
                        "range":[3,6],
                        "color":"salmon"
                    }

                ],

                "threshold":{

                    "line":{
                        "color":"black",
                        "width":4
                    },

                    "value":median_risk
                }
            }
        )
    )

    return fig