import pandas as pd
import plotly.express as px


def create_gene_radar_chart(profile):

    genes = [
        "OSMR",
        "TMEM171",
        "GJB2",
        "VILL",
        "SHISA6",
        "SCN9A",
        "GPR157",
        "RPL39L",
        "PKD2L1",
        "IGFBP6"
    ]

    values = []

    for gene in genes:
        values.append(float(profile[gene]))

    radar_df = pd.DataFrame({
        "Gene": genes,
        "Expression": values
    })

    fig = px.line_polar(
        radar_df,
        r="Expression",
        theta="Gene",
        line_close=True
    )

    fig.update_traces(fill="toself")

    fig.update_layout(
        title="Gene Expression Radar Chart",
        height=600
    )

    return fig