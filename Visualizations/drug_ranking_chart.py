import plotly.express as px


def create_drug_ranking_chart(
    treatment_df
):

    top10 = treatment_df.head(10)

    fig = px.bar(
        top10,
        x="Final_Score",
        y="Drug",
        orientation="h",
        color="Final_Score",
        color_continuous_scale="RdYlGn"
    )

    fig.update_layout(
        title="Top Personalized Treatment Options",
        height=600,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    return fig